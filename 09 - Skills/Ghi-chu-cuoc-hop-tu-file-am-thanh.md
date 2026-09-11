---
tags: [skill]
domain: "Họp/Ghi chú"
updated: "2026-09-10"
---

# Ghi chú cuộc họp từ file âm thanh (meeting-notes)

> Kỹ năng cho AI agent (Claude Code / Qwen Code / Codex…) trong SecondBrain: biến file ghi âm cuộc họp thành **biên bản chuẩn vault** — tóm tắt, quyết định, action items có owner + deadline.

## Khi nào dùng

- Có file ghi âm cuộc họp / phỏng vấn / voice memo (`.m4a`, `.mp3`, `.wav`, `.mp4`…) cần thành biên bản.
- Cần transcript kèm mốc giờ để trích dẫn lại ai nói gì, lúc nào.

## Cách làm

**Ngườidùng (không cần kỹ thuật):**

1. Chép file ghi âm vào vault (gợi ý: `00 - Inbox/` hoặc thư mục dự án).
2. Mở AI agent trong vault, gõ ví dụ:

   > *"Ghi chú cuộc họp từ file `00 - Inbox/hop-marketing-10-09.m4a`, lưu biên bản vào dự án Marketing"*

3. Agent tự chạy skill, hỏi bạn chốt chỗ lưu, rồi tạo note biên bản `status: draft`.
4. **Đọc lại + sửa**: tên người lạ hiện là `Speaker 1/2` (hệ thống chưa phân biệt giọng), deadline chưa rõ được agent liệt kê ở cuối để bạn bổ sung.

**Bên dưới — agent tự làm (tham khảo):**

1. Probe độ dài file → quá 90 phút thì từ chối, yêu cầu cắt nhỏ.
2. Chuyển sang wav 16k mono bằng ffmpeg → gửi qua dịch vụ chuyển-giọng-nói-thành-văn-bản (STT) của công ty → nhận transcript kèm mốc giờ từng câu (file dài tự chia khúc 5 phút/lần gửi rồi ghép lại).
3. Soạn biên bản tiếng Việt theo chuẩn SecondBrain:
   - **Thông tin** (file nguồn, thời lượng, ngày) → **Tóm tắt** → **Quyết định** → **Action items** dạng task vault: `- [ ] Việc cần làm #task 👤[[Tên]] 📅 YYYY-MM-DD` → **Transcript đầy đủ** có mốc giờ `[hh:mm:ss]`.

## Cạm bẫy

- **File tối đa 90 phút.** Dài hơn → cắt nhỏ trước (nhờ agent cắt bằng ffmpeg).
- **Không phân biệt người nói** (chưa có diarization) — biên bản ghi `Speaker 1/2`, tự thay tên thật.
- **Âm thanh rởm → transcript rởm.** Ghi âm điện thoại đặt giữa bàn là đủ tốt; họp online nên xuất file ghi trực tiếp.
- **Bảo mật:** file được gửi lên dịch vụ STT của công ty để xử lý. Nội dung **lương / nhân sự / hợp đồng mật** → KHÔNG dùng skill này, hỏi IT phương án riêng.
- Biên bản luôn ở trạng thái `draft` — **con ngườikiểm lại trước khi dùng chính thức**.
- Cần IT cấp 2 biến môi trường (làm 1 lần): `VOICE_STT_GATEWAY_URL` + `VOICE_STT_API_KEY` (thêm vào `.env` của vault) và `ffmpeg` trên máy (`brew install ffmpeg`). Kiểm tra đủ chưa:
  ```bash
  python3 .claude/skills/meeting-notes/scripts/transcribe.py --doctor
  ```

## Cập nhật skill

Skill nằm trong repo vault mẫu — khi có bản mới, chạy `shardmind update` hoặc `git pull` trong thư mục vault là xong (xem hướng dẫn cập nhật trong tài liệu training).

## Nguồn

- Chắt lọc từ: pipeline Transcribe Studio của dự án OGA (cùng dịch vụ STT, cùng bài học vận hành: chia khúc file dài, bắt buộc word-timestamps).
