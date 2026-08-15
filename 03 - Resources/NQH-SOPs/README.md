---
tags: [sop, reference]
---

# NQH SOPs — Tài liệu tham khảo

> Hệ thống SOP NQH đã được index trên **AI-Platform (CBrain)**. Bạn tra SOP bằng 2 cách:

## Cách 1 — MTClaw @sop (khuyến nghị)

Nhắn agent **@sop** trong Pod MTClaw → hỏi quy trình bất kỳ. Agent @sop có RAG access toàn bộ hệ thống SOP — không cần download về máy.

## Cách 2 — Hỏi AI agent trong vault

Gõ trong chat AI: *"SOP quy trình mở ca nhà hàng"* → agent tra qua MTClaw MCP (nếu đã kết nối).

## File local (tùy chọn)

IT có thể copy các SOP hay dùng vào thư mục này cho bạn tra offline. Cấu trúc:

```text
NQH-SOPs/
├── Operations/    # SOP vận hành (nếu vai trò Ops/GM/FOH)
├── Accounting/    # SOP kế toán
├── Sales/         # SOP sales
├── HR/            # SOP nhân sự
├── Procurement/   # SOP mua hàng
└── ...
```

**Không sửa** file SOP — đây là bản tham khảo read-only.
