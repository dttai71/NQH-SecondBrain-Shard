---
name: meeting-notes
description: Transcribe meeting/interview audio (m4a/mp3/wav/mp4) via an OpenAI-style voice gateway STT endpoint, then draft vault-standard meeting minutes (decisions, action items #task, owners, deadlines). Use for "ghi chep cuoc hop", "transcribe file ghi am", "bien ban hop" requests. NOT for video editing or TTS/dubbing.
---

# Meeting Notes (STT → vault minutes)

## When to use

- User drops an audio/video file path and asks for ghi chú / biên bản / transcript.
- Meeting recordings, interview recordings, voice memos → structured vault notes.

## When NOT to use

- Video/audio editing (captions, cuts, overlays) — use an ffmpeg skill instead.
- Audio leaves the machine (sent to a configured STT gateway). Recordings
  containing salary/HR/contract or otherwise confidential content must NOT be
  processed with this skill unless your organization explicitly allows it.
- `.env` files: never read them. The API key must come from the process env.

## Workflow (fixed order)

1. **Probe** — run `scripts/transcribe.py <file> --probe-only` to get duration.
   - Longer than the configured cap (default 90 min) → refuse; suggest
     splitting the file first.
2. **Confirm destination** — ask (or infer from the request) where the minutes
   belong: `01 - Projects/<project>/`, `02 - Areas/`, or `05 - Daily Notes/`.
3. **Transcribe** — `scripts/transcribe.py <file> --language vi --out <tmpdir>/transcript.json`.
   - Audio over the chunk threshold (default 8 min) is auto-sliced into 5-min
     windows, transcribed per window, and merged with offset timestamps —
     long single requests time out at typical gateways.
   - Progress prints per chunk; a 30-min recording takes several minutes.
4. **Draft minutes** — read the transcript JSON, write a Vietnamese note:
   - Frontmatter: `tags: [bien-ban]`, `date: YYYY-MM-DD`, `status: draft`,
     `type: meeting-notes`.
   - Sections: **Thông tin** (source file, duration, date) → **Tóm tắt** →
     **Quyết định** → **Action items** in vault task syntax:
     `- [ ] Mô tả #task 👤[[Tên NV]] 📅 YYYY-MM-DD` → **Transcript**
     (collapse or split into a separate `.md` when > ~500 lines; keep
     `[hh:mm:ss]` timestamps).
   - Wikilink attendees `[[Tên]]`; unknown speakers → `Speaker 1/2` (no
     diarization — state that limitation honestly).
5. **Save + report** — write the note, report its path, list open questions
   (unclear names, uncertain deadlines) for the user to correct.

## Environment (required)

- `VOICE_STT_API_KEY` — API key for the STT gateway. If unset, tell the user
  to export it. NEVER print or log the key.
- `VOICE_STT_GATEWAY_URL` — base URL of the STT gateway (no default; the
  script fails with a clear message when unset).
- `ffmpeg` + `ffprobe` on PATH. Check with `--doctor`.
- Python ≥ 3.9, standard library only.

## Commands

```bash
python3 .claude/skills/meeting-notes/scripts/transcribe.py --doctor
python3 .claude/skills/meeting-notes/scripts/transcribe.py meeting.m4a --probe-only
python3 .claude/skills/meeting-notes/scripts/transcribe.py meeting.m4a \
  --language vi --out /tmp/mn/transcript.json --text-out /tmp/mn/transcript.txt
```

`--language` defaults to `vi`. Output JSON:
`{ text, language, segments[] (with words[] + timestamps), stats }`.

## Pitfalls (learned from production incidents)

- **Never** send long audio in one request — gateways time out. Chunking is
  built in; don't bypass it.
- Word timestamps are requested in the multipart form body; the script aborts
  if the response lacks `segments[].words[]` (guards against gateway
  regressions).
- ASR timestamp jitter at chunk seams is repaired during merge; a huge
  inversion means real corruption — the script fails loud. Keep the error.
- Each chunk is retried (2 retries, 3s backoff). If all retries fail the whole
  run aborts — no partial transcripts.
