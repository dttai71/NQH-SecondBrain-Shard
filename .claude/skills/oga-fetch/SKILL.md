---
name: oga-fetch
description: Lấy ảnh/video vừa tạo ở Studio về vault, kèm sidecar provenance.
---

# oga-fetch

## Khi nào dùng

Người dùng nói một câu kiểu:

- "lấy ảnh vừa tạo về vault"
- "kéo asset Studio về"
- "lấy mấy ảnh hôm nay ở Studio về Inbox"

## Env cần có

| Biến | Ví dụ | Ghi chú |
|---|---|---|
| `STUDIO_URL` | `https://studio.nhatquangholding.com` | Gốc của Studio. |
| `STUDIO_ASSET_KEY` | `oga_...` | **Key cá nhân** (một key một người, ADR-030 §D6). |

`STUDIO_ASSET_KEY` nằm trong `.env` của vault nhân viên, **KHÔNG commit vào Shard**. Thiếu env
thì fail-closed: dừng, báo người dùng, không đoán.

## Hai lời gọi

Cả hai đều gửi header `x-api-key: $STUDIO_ASSET_KEY`.

1. `GET {STUDIO_URL}/api/v1/media/assets?since=<ISO8601>&limit=<int>` → danh sách sidecar-shaped
   rows, mới nhất trước (ADR-030 §D5).
2. Với mỗi `id`: `GET {STUDIO_URL}/api/v1/media/assets/{id}/download` (bytes) và
   `GET {STUDIO_URL}/api/v1/media/assets/{id}` (sidecar JSON verbatim).

## File rơi vào đâu

```
00 - Inbox/studio/{created_at}-{id}.{ext}     # bytes
00 - Inbox/studio/{created_at}-{id}.json      # sidecar provenance
```

`ext` suy ra từ `content_type` trong sidecar (`image/png`→png, `video/mp4`→mp4,
`audio/mpeg`→mp3). Skill **không** move/rename/diễn giải gì thêm — ranh giới "consume, not
author" của ADR-029.

## Bước xác minh sha256 (bắt buộc)

Tải file → tính `sha256` của bytes → phải **bằng** `sidecar.sha256` (ADR-030 C4).
Không khớp → **xoá cả file lẫn sidecar vừa ghi**, báo cáo id hỏng, không giữ lại bản nghi ngờ.

## Ánh xạ lỗi

| HTTP | Nói với người dùng |
|---|---|
| 400 | id sai định dạng (không phải 32 hex thường) — lỗi của skill, không phải của Studio. |
| 401 | "Key hết hạn hoặc bị thu hồi — hỏi @itadmin cấp lại." |
| 404 | "Asset đã bị dọn (retention 30 ngày)." |
| 429 | Quá 60 req/phút — chờ rồi thử lại, không vòng lặp gấp. |
| 5xx | Studio lỗi — báo lại, không retry vô hạn. |

## Luật không được phá

- **Không bao giờ tách sidecar khỏi file** (ADR-029). Sidecar đi đâu file đi đó; không ghi file
  mà thiếu `.json`, không xoá `.json` để "cho gọn".
- Không ghi đè file đã có trong Inbox — trùng tên thì bỏ qua và báo.
- Không tự thêm/sửa field trong sidecar. Đó là bản ghi provenance, không phải note.
