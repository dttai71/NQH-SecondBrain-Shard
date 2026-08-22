---
description: Hỏi phản biện nhiều hãng AI khác nhau (Claude + Kimi + Qwen) cho một quyết định khó
---

Lấy **phản biện từ nhiều hãng AI khác nhau** cho quyết định/câu hỏi: `$ARGUMENTS`.

Dùng khi phải quyết một việc **thật sự khó** (chọn phương án, đổi hướng, cam kết tiền/thời gian).
Không dùng cho câu hỏi vặt — mỗi lần chạy tốn token của công ty.

## Cách làm

1. **Đóng gói bối cảnh trước khi hỏi.** Model ngoài không biết gì về công việc bạn.
   Tóm tắt gọn: vấn đề · các phương án đang cân nhắc · ràng buộc (thời gian, tiền, người).
   Dẫn thêm nội dung note liên quan nếu có.

2. **Gọi:**
   ```bash
   # cả 3 hãng, chạy song song (~30 giây)
   python3 .claude/scripts/consult-litellm.py "<bối cảnh gọn> | Câu hỏi: <$ARGUMENTS>. Phản biện: rủi ro, điểm mù, phương án khác."

   # chọn tập con khi chỉ cần vài góc nhìn
   python3 .claude/scripts/consult-litellm.py "<prompt>" kimi qwen
   ```

3. **Trình bày cho người dùng:** ý kiến từng hãng · chỗ **cả ba đồng ý** (tin cậy hơn) ·
   chỗ **mâu thuẫn nhau** (đây mới là chỗ đáng suy nghĩ) · hãng nào **không trả lời được**.

4. **Phản biện lại luôn** — đừng chỉ chuyển tiếp. Nêu chỗ bạn đồng/không đồng với họ,
   dựa trên bối cảnh trong vault mà model ngoài không có. **Người dùng quyết.**

5. Quyết định lớn → ghi vào Nhật ký Quyết định, kèm dòng "đã hỏi phản biện đa-hãng".

## Vì sao gọi đích danh `claude`/`kimi`/`qwen`, không gọi `auto`

`auto` **tự chuyển hãng** khi cổng nghẽn. Gọi `auto` ba lần có thể ra **cùng một model ba lần** —
đó là hỏi một người ba lần, không phải ba ý kiến. Ba hãng khác nhau (Anthropic · Moonshot · Alibaba)
được huấn luyện khác nhau nên **điểm mù khác nhau** — đó chính là thứ ta cần.

⚠️ Ngay cả gọi đích danh, khi hãng đó nghẽn thì cổng vẫn có thể chuyển sang hãng khác.
Nếu một câu trả lời tự xưng sai hãng, **coi như ý kiến trùng** — đừng tính là góc nhìn thứ ba.

## An toàn (bắt buộc)

- **KHÔNG gửi dữ liệu nhạy cảm:** lương, đánh giá cá nhân, dữ liệu khách hàng, hợp đồng, mật khẩu.
  Cổng LiteLLM là của NQH, nhưng nó **chuyển tiếp** tới Anthropic/Moonshot/Alibaba — **cổng nội bộ không có nghĩa là model nội bộ.**
- Cần hỏi việc có dữ liệu nhạy cảm → bỏ số/tên thật ra, hỏi bằng tình huống chung.
- **Bạn chịu trách nhiệm cuối.** AI phản biện để bạn nghĩ kỹ hơn, không phải để quyết thay.
