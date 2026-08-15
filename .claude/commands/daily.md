---
description: Tạo daily note hôm nay, kéo task đến hạn, quét email nếu đã nối
---

1. Xác định ngày hôm nay (YYYY-MM-DD).
2. Tạo `05 - Daily Notes/<ngày>.md` từ `06 - Templates/Template - Daily Note.md` nếu chưa có.
3. Quét toàn vault các `#task` chưa xong, đến hạn hôm nay hoặc quá hạn → liệt kê vào mục "Ưu tiên hôm nay".
4. **Nếu có MCP email đã nối** (kiểm bằng ToolSearch — Gmail/Outlook, xem `02_Installation.md`
   mục F): quét unread 2 ngày gần nhất, chỉ đọc. Lọc nhiễu (bot notification, marketing) —
   chỉ tạo note `00 - Inbox/Email - <chủ đề>.md` cho thread thật sự cần xử lý.
5. **Nếu có MCP MTClaw đã nối**: hỏi trợ lý xem có tin nhắn/báo cáo mới cho mình không.
6. Tóm tắt ngắn cho người dùng: task ưu tiên + email/tin nhắn cần xử lý (nếu có) → hỏi "Hôm nay
   bạn muốn ưu tiên gì?"
7. Trước câu hỏi cuối, thêm 1 dòng: **"Chi phí phiên: ~N nghìn token"** (ước theo mức đã đọc
   trong `/daily`).

Chỉ tạo/đọc note, không gửi gì ra ngoài — không tự trả lời email/tin nhắn.
