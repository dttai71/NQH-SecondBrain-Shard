---
description: Cập nhật vault SecondBrain lên bản mới nhất (skill mới, template mới) — không mất phần bạn đã sửa tay
---

Người dùng muốn cập nhật vault SecondBrain của họ lên bản mới nhất từ `NQH-SecondBrain-Shard`.

1. Kiểm `shardmind` đã cài chưa: `which shardmind || npm list -g shardmind`.
   - Chưa có → chạy `npm install -g shardmind` trước (báo người dùng 1 dòng đang cài).
2. Ghi lại trạng thái trước khi cập nhật để so sánh sau: `git -C . log -1 --format=%H 2>/dev/null` (nếu vault là git repo) — gọi là `TRUOC`.
3. Chạy cập nhật thật: `shardmind update`. Đây là 3-way merge (dùng `node-diff3`) — **giữ nguyên phần người dùng đã tự sửa** (vd `08 - Context/My-Role.md`), chỉ merge phần template/skill mới. Không tự ý chạy `git pull`/`git reset` thay cho lệnh này — `shardmind` đã lo đúng phần merge an toàn.
4. Nếu `shardmind update` báo xung đột (không tự merge được) — dừng, in nguyên văn thông báo xung đột, hỏi người dùng muốn giữ bản nào, **không tự chọn thay**.
5. Cập nhật xong, so sánh `TRUOC` với `HEAD` mới (nếu có git): liệt kê skill/command mới hoặc đổi — nhìn vào các đường dẫn `09 - Skills/`, `.claude/commands/`, `.claude/skills/` xuất hiện trong `git diff --stat TRUOC HEAD`. Không có git (vault tải tay, không clone) → chỉ báo "đã cập nhật xong", không so sánh được.
6. Trình bày ngắn gọn cho người dùng: **skill/lệnh nào mới** (tên + 1 câu skill đó làm gì, đọc từ frontmatter `description` của file mới) + **cách dùng** (vd "gõ `/sop <câu hỏi>` để tra SOP qua API, không cần mở trình duyệt"). Không liệt kê file nội bộ (template, hook) nếu không phải skill/lệnh nhân viên dùng trực tiếp.
7. Nếu không có gì mới (đã ở bản mới nhất) — nói rõ 1 câu, không bịa ra thay đổi.

**Không tự chạy lệnh này** khi người dùng không yêu cầu — cập nhật vault là hành động người dùng chủ động chọn lúc nào, không tự động nền.
