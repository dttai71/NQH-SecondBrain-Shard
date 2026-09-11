#!/usr/bin/env python3
"""
meeting-notes — transcribe audio/video via an OpenAI-style voice STT gateway.

Python 3.9+, standard library only. Requires ffmpeg + ffprobe on PATH.

Endpoint contract (same shape as common whisper gateways):
    POST {VOICE_STT_GATEWAY_URL}/api/v1/voice/stt/transcribe
    Headers: X-API-Key: $VOICE_STT_API_KEY
    Body: multipart/form-data
        file=<16k mono wav>, word_timestamps="true", language=<e.g. "vi">
    Response JSON: { text, language, segments: [{ start, end, text,
        words: [{ word, start, end }, ...] }, ...], fallback_used? }

Long audio is sliced into fixed windows (default 5 min) when it exceeds the
chunk threshold (default 8 min), each window transcribed separately, then
merged with offset timestamps — long single requests time out at gateways.
"""

import argparse
import json
import math
import os
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.request
import urllib.error
import uuid

DEFAULT_MAX_MEDIA_S = 5400          # 90 min hard cap
DEFAULT_CHUNK_THRESHOLD_S = 480     # 8 min
DEFAULT_CHUNK_LENGTH_S = 300        # 5 min
CHUNK_TIMEOUT_S = 600               # 10 min per chunk
SINGLE_TIMEOUT_S = 1800             # 30 min
CHUNK_RETRIES = 2
CHUNK_RETRY_DELAY_S = 3
MONOTONIC_TOLERANCE_S = 0.5


def die(msg, code=1):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(code)


def run(cmd, timeout_s=300):
    try:
        proc = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout_s
        )
    except subprocess.TimeoutExpired:
        die(f"command timed out: {' '.join(cmd[:2])} ...")
    if proc.returncode != 0:
        die(f"command failed ({proc.returncode}): {' '.join(cmd[:2])}\n{proc.stderr.strip()[:400]}")
    return proc.stdout


def find_bin(name):
    path = shutil.which(name)
    if not path:
        die(f"{name} not found on PATH — install ffmpeg (e.g. brew install ffmpeg)")
    return path


def probe_duration(path):
    ffprobe = find_bin("ffprobe")
    out = run([
        ffprobe, "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", path,
    ])
    try:
        return float(out.strip())
    except ValueError:
        die(f"could not probe duration of {path}")


def to_wav(src, dst):
    ffmpeg = find_bin("ffmpeg")
    run([ffmpeg, "-y", "-v", "error", "-i", src, "-ac", "1", "-ar", "16000", dst])


def slice_wav(src, dst, start, duration):
    ffmpeg = find_bin("ffmpeg")
    run([ffmpeg, "-y", "-v", "error", "-ss", str(start), "-t", str(duration),
         "-i", src, "-ac", "1", "-ar", "16000", dst])


def multipart_body(fields, file_field, filename, data, mime):
    boundary = f"----mn-{uuid.uuid4().hex}"
    parts = []
    for key, value in fields.items():
        parts.append(
            f"--{boundary}\r\nContent-Disposition: form-data; name=\"{key}\"\r\n\r\n{value}\r\n".encode()
        )
    parts.append(
        f"--{boundary}\r\nContent-Disposition: form-data; name=\"{file_field}\"; "
        f"filename=\"{filename}\"\r\nContent-Type: {mime}\r\n\r\n".encode()
    )
    parts.append(data)
    parts.append(f"\r\n--{boundary}--\r\n".encode())
    return boundary, b"".join(parts)


def stt_transcribe(wav_path, gateway, api_key, language, timeout_s):
    url = f"{gateway}/api/v1/voice/stt/transcribe"
    with open(wav_path, "rb") as fh:
        data = fh.read()
    boundary, body = multipart_body(
        {"word_timestamps": "true", "language": language},
        "file", "audio.wav", data, "audio/wav",
    )
    req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("X-API-Key", api_key)
    req.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")
    try:
        with urllib.request.urlopen(req, timeout=timeout_s) as res:
            payload = json.loads(res.read().decode())
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"STT gateway returned {exc.code}: {exc.read().decode(errors='replace')[:300]}")
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"STT request failed: {exc}")

    segments = payload.get("segments")
    if not isinstance(segments, list) or not segments:
        raise RuntimeError("STT response has no segments")
    for i, seg in enumerate(segments):
        if not isinstance(seg.get("words"), list):
            raise RuntimeError(f"STT segment {i} has no words[] (word_timestamps not honored)")
    return payload


def offset_segments(segments, offset_s, chunk_duration_s):
    def clamp(t):
        return min(max(0.0, float(t)), chunk_duration_s) + offset_s
    out = []
    for seg in segments:
        out.append({
            **seg,
            "start": clamp(seg["start"]),
            "end": clamp(seg["end"]),
            "words": [{**w, "start": clamp(w["start"]), "end": clamp(w["end"])}
                      for w in seg["words"]],
        })
    return out


def merge_chunk_results(results, chunk_length_s):
    segments, texts = [], []
    nudged = seam_fixes = mid_chunk_fixes = 0
    boundaries = [b for r in results for b in (r["chunk_start"], r["chunk_end"])]
    fallback_used = False
    for r in results:
        segments.extend(r["segments"])
        texts.append(str(r.get("text", "")).strip())
        fallback_used = fallback_used or bool(r.get("fallback_used"))

    def dist_boundary(t):
        return min((abs(t - b) for b in boundaries), default=math.inf)

    for i in range(1, len(segments)):
        prev, seg = segments[i - 1], segments[i]
        if seg["start"] < prev["start"]:
            inversion = prev["start"] - seg["start"]
            if inversion > chunk_length_s:
                die(f"merged transcript not monotonic at segment {i}: inversion "
                    f"{inversion:.2f}s exceeds one chunk length — suspected offset "
                    "mis-application, not repairable")
            for w in seg["words"]:
                w["start"] += inversion
                w["end"] += inversion
            seg["start"] += inversion
            seg["end"] += inversion
            seam_dist = min(dist_boundary(prev["start"]), dist_boundary(seg["start"]))
            if inversion <= MONOTONIC_TOLERANCE_S:
                nudged += 1
            elif seam_dist <= 5:
                seam_fixes += 1
            else:
                mid_chunk_fixes += 1
    return {
        "segments": segments,
        "text": "\n".join(t for t in texts if t),
        "fallback_used": fallback_used,
        "nudged": nudged,
        "seam_fixes": seam_fixes,
        "mid_chunk_fixes": mid_chunk_fixes,
    }


def format_ts(seconds):
    seconds = max(0, int(seconds))
    return f"{seconds // 3600:02d}:{(seconds % 3600) // 60:02d}:{seconds % 60:02d}"


def plain_transcript(segments):
    return "\n".join(
        f"[{format_ts(s['start'])}] {str(s.get('text', '')).strip()}"
        for s in segments if str(s.get("text", "")).strip()
    )


def doctor():
    ok = True
    for name in ("ffmpeg", "ffprobe"):
        found = shutil.which(name)
        print(f"{name}: {found or 'MISSING'}")
        ok = ok and bool(found)
    if shutil.which("ffmpeg"):
        proc = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True)
        if proc.returncode == 0:
            print(f"ffmpeg version: {proc.stdout.splitlines()[0] if proc.stdout else '?'}")
        else:
            print(f"ffmpeg version: BROKEN — {proc.stderr.splitlines()[0] if proc.stderr else 'unknown error'}")
            ok = False
    gateway = os.environ.get("VOICE_STT_GATEWAY_URL", "")
    key = os.environ.get("VOICE_STT_API_KEY", "")
    print(f"VOICE_STT_GATEWAY_URL: {'set' if gateway else 'MISSING'}")
    print(f"VOICE_STT_API_KEY: {'set' if key else 'MISSING'}")
    sys.exit(0 if ok and gateway and key else 1)


def main():
    ap = argparse.ArgumentParser(description="meeting-notes transcription via voice STT gateway")
    ap.add_argument("input", nargs="?", help="audio/video file (m4a/mp3/wav/mp4...)")
    ap.add_argument("--language", default="vi")
    ap.add_argument("--out", help="write transcript JSON here")
    ap.add_argument("--text-out", help="write plain [hh:mm:ss] transcript here")
    ap.add_argument("--probe-only", action="store_true", help="only print duration, no STT")
    ap.add_argument("--doctor", action="store_true", help="check dependencies + env, then exit")
    ap.add_argument("--max-media-s", type=float, default=DEFAULT_MAX_MEDIA_S)
    ap.add_argument("--chunk-threshold-s", type=float, default=DEFAULT_CHUNK_THRESHOLD_S)
    ap.add_argument("--chunk-length-s", type=float, default=DEFAULT_CHUNK_LENGTH_S)
    args = ap.parse_args()

    if args.doctor:
        doctor()
    if not args.input:
        ap.error("input file required (or use --doctor)")
    if not os.path.isfile(args.input):
        die(f"file not found: {args.input}")

    duration = probe_duration(args.input)
    print(f"duration: {duration:.1f}s ({format_ts(duration)})")
    if args.probe_only:
        return
    if duration > args.max_media_s:
        die(f"audio exceeds the {int(args.max_media_s // 60)}-minute hard cap — split the file first")

    gateway = os.environ.get("VOICE_STT_GATEWAY_URL", "").rstrip("/")
    api_key = os.environ.get("VOICE_STT_API_KEY", "")
    if not gateway or not api_key:
        die("VOICE_STT_GATEWAY_URL and VOICE_STT_API_KEY must be set in the environment")

    workdir = tempfile.mkdtemp(prefix="meeting-notes-")
    try:
        wav = os.path.join(workdir, "audio.wav")
        print("converting to 16k mono wav ...")
        to_wav(args.input, wav)

        if duration <= args.chunk_threshold_s:
            print("transcribing (single request) ...")
            payload = stt_transcribe(wav, gateway, api_key, args.language, SINGLE_TIMEOUT_S)
            result = {
                "segments": payload["segments"],
                "text": payload.get("text", ""),
                "fallback_used": bool(payload.get("fallback_used")),
            }
            stats = {"chunks": 1}
        else:
            chunk_len = args.chunk_length_s
            windows = []
            start, idx = 0.0, 0
            while start < duration:
                windows.append({"index": idx, "start": start,
                                "duration": min(chunk_len, duration - start)})
                start += chunk_len
                idx += 1
            print(f"transcribing in {len(windows)} chunks of {int(chunk_len)}s ...")
            results = []
            for w in windows:
                chunk_path = os.path.join(workdir, f"chunk-{w['index']:03d}.wav")
                slice_wav(wav, chunk_path, w["start"], w["duration"])
                last_err = None
                payload = None
                for attempt in range(1, 1 + 1 + CHUNK_RETRIES):
                    try:
                        payload = stt_transcribe(chunk_path, gateway, api_key,
                                                 args.language, CHUNK_TIMEOUT_S)
                        last_err = None
                        break
                    except SystemExit:
                        raise
                    except Exception as exc:  # noqa: BLE001
                        last_err = exc
                        print(f"  chunk {w['index'] + 1}/{len(windows)} attempt {attempt} "
                              f"failed: {exc}", file=sys.stderr)
                        if attempt <= CHUNK_RETRIES:
                            time.sleep(CHUNK_RETRY_DELAY_S)
                if payload is None:
                    die(f"STT chunk {w['index'] + 1}/{len(windows)} failed after "
                        f"{1 + CHUNK_RETRIES} attempts: {last_err}")
                results.append({
                    "segments": offset_segments(payload["segments"], w["start"], w["duration"]),
                    "text": payload.get("text", ""),
                    "fallback_used": bool(payload.get("fallback_used")),
                    "chunk_start": w["start"],
                    "chunk_end": w["start"] + w["duration"],
                })
                os.remove(chunk_path)
                print(f"  chunk {w['index'] + 1}/{len(windows)} done")
            result = merge_chunk_results(results, chunk_len)
            stats = {
                "chunks": len(windows),
                "nudged": result["nudged"],
                "seam_fixes": result["seam_fixes"],
                "mid_chunk_fixes": result["mid_chunk_fixes"],
            }

        out_payload = {
            "source": os.path.abspath(args.input),
            "duration_s": round(duration, 2),
            "language": args.language,
            "text": result["text"],
            "segments": result["segments"],
            "stats": stats,
        }
        if args.out:
            with open(args.out, "w", encoding="utf-8") as fh:
                json.dump(out_payload, fh, ensure_ascii=False, indent=2)
            print(f"JSON: {args.out}")
        else:
            print(json.dumps(out_payload, ensure_ascii=False)[:2000])
        if args.text_out:
            with open(args.text_out, "w", encoding="utf-8") as fh:
                fh.write(plain_transcript(result["segments"]) + "\n")
            print(f"text: {args.text_out}")
    finally:
        shutil.rmtree(workdir, ignore_errors=True)


if __name__ == "__main__":
    main()
