#!/usr/bin/env python3
"""Phản biện đa-model cho nhân viên NQH — qua LiteLLM gateway công ty.

Gọi ĐÍCH DANH nhiều hãng khác nhau (Claude/Anthropic · Kimi/Moonshot · Qwen/Alibaba)
để có nhiều góc nhìn thật sự, thay vì hỏi một model nhiều lần.

Usage:
  consult-litellm.py "<câu hỏi + bối cảnh>"                  # cả 3 hãng
  consult-litellm.py "<câu hỏi>" kimi qwen                   # chọn tập con

Key: NQH_AI_KEY trong .env của vault (IT cấp qua Portal). KHÔNG hardcode key.
KHÔNG gửi dữ liệu nhạy cảm (lương, đánh giá cá nhân, dữ liệu khách, hợp đồng)
— gateway là của NQH nhưng nó CHUYỂN TIẾP tới Anthropic/Moonshot/Alibaba.
"""
import os, sys, json, urllib.request, urllib.error, pathlib
import concurrent.futures as cf

BASE = os.environ.get("LITELLM_BASE", "https://litellm.nhatquangholding.com/v1")
SYSTEM = ("Bạn là chuyên gia phản biện. Nêu rủi ro, điểm mù, giả định chưa kiểm chứng, "
          "và phương án khác. Ngắn gọn, thẳng thắn, tiếng Việt. Không nịnh.")

# Đích danh từng hãng — KHÔNG dùng alias 'auto' cho việc này.
# 'auto' tự chuyển hãng khi nghẽn, nên 3 lời gọi 'auto' có thể ra cùng một model:
# hỏi 3 lần một model không phải là ba ý kiến độc lập.
EXPERTS = {
    "claude": ("Claude (Anthropic)", "claude"),
    "kimi":   ("Kimi (Moonshot)",    "kimi"),
    "qwen":   ("Qwen (Alibaba)",     "qwen"),
}

def load_env():
    """Đọc .env ở gốc vault (đi ngược lên từ .claude/scripts/)."""
    for parent in pathlib.Path(__file__).resolve().parents:
        f = parent / ".env"
        if f.exists():
            for line in f.read_text().splitlines():
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip())
            return

def ask(label, model, prompt):
    key = os.environ.get("NQH_AI_KEY")
    if not key or key.startswith("<"):
        return (label, None, "NQH_AI_KEY chưa set trong .env — lấy tại portal.nhatquangholding.com/my-ai-key")
    body = json.dumps({"model": model, "messages": [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": prompt}]}).encode()
    req = urllib.request.Request(BASE.rstrip("/") + "/chat/completions", data=body,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    try:
        r = json.load(urllib.request.urlopen(req, timeout=180))
        text = r["choices"][0]["message"].get("content")
        if not text:
            fin = r["choices"][0].get("finish_reason")
            return (label, None, f"trả lời rỗng (finish_reason={fin}) — thử lại")
        return (label, text, None)
    except urllib.error.HTTPError as e:
        detail = e.read()[:300].decode(errors="ignore")
        hint = " — cổng đang nghẽn, chờ chút rồi chạy lại" if e.code == 429 else ""
        return (label, None, f"HTTP {e.code}{hint}: {detail}")
    except Exception as e:
        return (label, None, str(e)[:200])

def main():
    if len(sys.argv) < 2:
        print('Usage: consult-litellm.py "<câu hỏi>" [claude|kimi|qwen ...]'); sys.exit(1)
    load_env()
    prompt = sys.argv[1]
    asked = sys.argv[2:]
    bad = [a for a in asked if a not in EXPERTS]
    if bad:  # gõ sai tên mà lọc im lặng = chạy khác ý người gọi, không ai biết
        print(f"✗ không có chuyên gia: {', '.join(bad)} (có: {', '.join(EXPERTS)})", file=sys.stderr)
        sys.exit(2)
    want = asked or list(EXPERTS)

    with cf.ThreadPoolExecutor(max_workers=len(want)) as ex:
        results = list(ex.map(lambda k: ask(EXPERTS[k][0], EXPERTS[k][1], prompt), want))

    failed = []
    for label, text, err in results:
        print(f"\n===== {label} =====")
        if text:
            print(text)
        else:
            print(f"[KHÔNG TRẢ LỜI ĐƯỢC] {err}")
            failed.append(label)

    if failed:
        # Thiếu ý kiến KHÁC với các ý kiến đồng thuận. Nói rõ, đừng để người đọc
        # tưởng số ý kiến nhận được là số ý kiến đã hỏi.
        print(f"\n⚠️ {len(failed)}/{len(want)} chuyên gia không trả lời: {', '.join(failed)}."
              f" Bạn đang đọc {len(want)-len(failed)} ý kiến, KHÔNG phải {len(want)}.")

if __name__ == "__main__":
    main()
