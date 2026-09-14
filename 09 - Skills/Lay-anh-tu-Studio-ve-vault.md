---
tags: [skill, pilot]
domain: "Marketing/Creative"
updated: "2026-09-14"
---

# Lấy ảnh vừa tạo ở Studio về vault (oga-fetch) — PILOT

> Kỹ năng cho AI agent trong SecondBrain: kéo ảnh/video bạn vừa tạo ở **NQH Creative Studio** về thẳng `00 - Inbox/studio/`, kèm file `.json` "giấy khai sinh" (tạo bằng AI, model nào, prompt gì, mã kiểm tra sha256). Không cần bấm Tải xuống rồi kéo tay nữa.
>
> **Trạng thái 14/09:** pilot — E2E 9/10 đạt (dòng 10 = kiểm thu hồi key, chờ IT). Thử được ngay; đường cũ (Tải xuống → kéo vào vault) vẫn dùng song song.

## Khi nào dùng

- Vừa tạo ảnh/video ở Studio, muốn nó nằm trong vault để cắt dựng, viết bài, hay gửi duyệt.
- Lấy lại **mọi thứ đã tạo hôm nay/hôm qua** một lượt.

## Cần gì (làm 1 lần)

1. **Key cá nhân** do IT cấp (`assets:read`, hết hạn sau 90 ngày). IT đưa bạn một dòng dạng `NQH_AI_KEY=aip_…`.
2. Mở file `.env` trong thư mục gốc vault (tạo nếu chưa có), dán:
   ```
   STUDIO_URL=https://studio.nhatquangholding.com
   NQH_AI_KEY=sk-…               # cùng khoá LiteLLM bạn đã đặt cho AI trong vault — không cần khoá riêng
   ```
   Không đưa key vào ghi chú, không commit, không chat.
3. Máy cần `curl`, `jq` (`brew install jq`), `shasum` (có sẵn trên Mac).

## Cách dùng

**Người dùng:** tạo xong ở Studio, quay lại SecondBrain và nói với AI agent:
- "Lấy ảnh vừa tạo ở Studio về vault"
- "Kéo mọi asset Studio từ hôm qua về"
- "Lấy asset `e0161252…` về" (mã hiện ở Studio sau khi tạo — 32 ký tự)

**AI agent** chạy `.claude/skills/oga-fetch/fetch.sh` (`--since`, `--id`, `--dest`). Kết quả vào `00 - Inbox/studio/`:
```
2026-09-14T00-21-19Z-e0161252….png
2026-09-14T00-21-19Z-e0161252….json   ← giữ cùng file, không xoá
```

## Kiểm tra nhanh (5 phút, để nghiệm thu pilot)

| # | Làm | Phải thấy |
|---|---|---|
| 1 | Tạo 1 ảnh ở Studio (Image Studio, 768) | Studio hiện `id` 32 ký tự |
| 2 | Nói "Lấy ảnh vừa tạo ở Studio về vault" | `đã lấy: …png` + 2 file trong `00 - Inbox/studio/` |
| 3 | Mở file `.json` | `"ai_generated": true`, `"model": "flux2-klein-4b"`, có `"sha256"` |
| 4 | Nói lại lần nữa | `đã có, bỏ qua` — không tải trùng |
| 5 | Sửa `.env` thành key sai rồi thử | `401 — key hết hạn hoặc bị thu hồi` — không tải gì |

Lỗi thường gặp: `401` → key sai/hết hạn, hỏi IT · `404` → ảnh đã bị dọn (Studio giữ 30 ngày) · `429` → chờ 1 phút · `thiếu STUDIO_ASSET_KEY` → chưa có `.env`.

## Luật

- File `.json` là bằng chứng ảnh tạo bằng AI (yêu cầu §D6 quy chế thương hiệu) — **không tách, không xoá** khi chuyển đi đâu.
- Key là của **cá nhân**, nghỉ việc = IT thu hồi. Không cho mượn.
- Không nối thẳng Studio → BAP/Postiz; mọi đăng tải vẫn đi qua BAP.

## Cập nhật skill
Nguồn: repo `Studio` → `docs/08-collaborate/shard-skill-oga-fetch/` (ADR-030). Khi Studio đổi API, @cto Studio cập nhật `.claude/skills/oga-fetch/` ở đây.
