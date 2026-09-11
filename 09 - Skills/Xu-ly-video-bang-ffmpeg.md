---
tags: [skill]
domain: "Marketing/Video"
updated: "2026-09-11"
---

# Cắt dựng & xử lý video bằng AI (ffmpeg-skill)

> Kỹ năng cho AI agent trong SecondBrain: cắt, ghép, chèn phụ đề, nén, đổi khung hình video/audio **ngay trên máy** — không cần cài phần mềm dựng phim, không gửi file lên dịch vụ ngoài.

## Khi nào dùng

- **Reel/TikTok/Shorts:** đổi video ngang → dọc 9:16, chèn phụ đề tự động, cắt bỏ đoạn im lặng.
- **Video nội bộ / đào tạo:** ghép nhiều đoạn, chèn logo, chuẩn hoá âm lượng nghe đều nhau.
- **Nén video** quá nặng để gửi Zalo/email/upload drive.
- **Trích audio** từ video (lấy tiếng để ghi chú), cắt một đoạn highlight.

## Cách làm

**Ngườ1 dùng (không cần kỹ thuật):** chép video vào vault rồi nói yêu cầu bằng lời với AI agent, ví dụ:

- *"Cắt video `00 - Inbox/review-moingay.mp4` lấy từ giây 30 đến 90, xuất thành reel dọc có phụ đề."*
- *"Bỏ hết đoạn im lặng trong file `phongvan.mp4`."*
- *"Nén video này còn dưới 25MB để gửi Zalo."*
- *"Chuẩn hoá âm lượng 3 clip trong thư mục `01 - Projects/PizzaGap/raw/` cho bằng nhau."*

Agent tự probe file → chọn tool → chạy → kiểm tra kết quả → báo đường dẫn file xuất.

**Bên dưới (tham khảo):** skill gồm ~40 script Python gọi ffmpeg — cut/join/silence/fit/caption/overlay/loudness/batch…, chạy local 100%. Đã nghiệm thu trên macOS 11/09/2026: cắt, dựng 9:16, phụ đề karaoke, ghép logo, đồng bộ mic rờ1, bỏ im lặng, chuẩn âm -14 LUFS, xuất preset Reels/YouTube, tự kiểm 12 tiêu chuẩn nền tảng.

## Cạm bẫy

- **Cần ffmpeg trên máy** (IT cài 1 lần): macOS `brew install ffmpeg`. Kiểm tra: mở terminal gõ `ffmpeg -version` thấy số phiên bản là được.
- **Phụ đề tiếng Việt BẮT BUỘC chỉ định font macOS** (Helvetica Neue hoặc Arial) — font mặc định của skill (DejaVu Sans) không có trên máy Mac, máy sẽ thay bằng font khác và dấu chồng bị tách (vd "giớ i"). Khi yêu cầu phụ đề, nói rõ: *"chèn phụ đề tiếng Việt, font Helvetica Neue"*.
- **Chống rung (stabilize) và xử lý màu HDR→SDR** cần bản ffmpeg đầy đủ (`brew install ffmpeg-full`) — bản Homebrew thường thiếu 2 bộ lọc này. Marketing quay iPhone thường không cần; agent sẽ báo rõ nếu máy thiếu.
- **File lớn → chờ lâu** là bình thường (mã hoá lại video tốn thời gian thật). Cắt không mã hoá lại (copy) thì gần như tức thì — agent biết cách ưu tiên.
- **Phụ đề tự động** cần giọng nói rõ; tiếng ồn lớn → phụ đề sai nhiều, phải sửa tay.
- **Luôn kiểm tra file xuất** (mở xem thử) trước khi đăng — AI kiểm tra kỹ thuật được, nhưng "đẹp hay chưa" là mắt người.
- Không dùng để **chỉnh sửa nội dung gốc duy nhất** — luôn giữ file gốc, xuất ra file mới.
- **Tạo hình/video mới bằng AI (không phải cắt dựng)** → dùng OGA Studios (link nội bộ — hỏi IT), không phải skill này. Skill này chỉ xử lý footage quay sẵn trên máy.

## Cập nhật skill

Skill nằm trong repo vault mẫu — có bản mới thì `shardmind update` hoặc `git pull` (xem module 10 trong tài liệu training).

## Nguồn

- Skill gốc: [kajisho5/ffmpeg-skill](https://github.com/kajisho5/ffmpeg-skill) (MIT) — đóng gói sẵn trong vault, không cần cài thêm.
