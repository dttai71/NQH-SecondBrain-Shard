# SKILL-AUTHORING-STANDARD-NQH

> Chuẩn soạn skill NQH cho Shard (`.claude/skills/`) — GĐ0 của [[QĐ - Khung Skill SCB NQH (đợt 1, 4 vai, 12 skill)]]. Mọi skill đợt 1 phải theo chuẩn này trước khi chủ vai duyệt.

## 1. Nguyên tắc bất di bất dịch

1. **Trỏ-§, không sao chép.** Skill nêu *quy trình thao tác + địa chỉ tài liệu* (`NQH-HO-FIN-SOP-008 §3.2`), KHÔNG chép nội dung SOP. SOP sửa → skill tự đúng (luật 1-tài-liệu-1-chỗ CGF).
2. **Repo public = chỉ quy trình thao tác.** Chi tiết nhạy cảm (giá, lương, PII, token, mật khẩu) nằm lại RAG_Library private. Host nội bộ không xuất hiện trong diff push — leak-gate quét mẫu domain (định nghĩa mẫu giữ ở bản private, xem memory leak-gate m56) trước mỗi push.
3. **Agent-agnostic.** Chỉ dùng: đọc/ghi file, shell, node, python. Không tool riêng CC/Qwen/Kimi. Chạy được trên mọi agent đang trong Shard (AGENTS.md + CLAUDE.md + GEMINI.md cùng nạp).
4. **Ngôn ngữ:** nội dung tiếng Việt; tên file/thư mục tiếng Việt không dấu hoặc kebab-case (`ke-toan-doi-chieu-ncc`).
5. **Không bịa.** Skill thiếu dữ liệu → ghi `[cần bổ sung: <ai>)` để chủ vai điền, không khống số.
6. **Hai CLI song song** (@itadmin chốt 22/09): Qwen Code đọc `.qwen/commands/` (cú pháp `{{args}}`), KHÔNG đọc `.claude/` — CC đọc `.claude/commands/` (`$ARGUMENTS`). Mọi **lệnh/skill mới phải ra cả hai bộ cùng lúc** (nội dung như nhau, cú pháp tham số theo CLI), không làm CC trước rồi tính sau. Skill `.claude/skills/` thì hai CLI cùng đọc qua symlink của starter-vault — không cần nhân bản.

## 2. Cấu trúc SKILL.md

```markdown
---
name: <kebab-case-tên>
description: <1 dòng — dùng để quyết định nạp skill khi nào>
type: skill
vai: ops|hr|kt-kho|mkt
status: draft|owner-reviewed|active
sop-refs:
  - "NQH-HO-<PB>-<SOP/STD>-<###> §<mục>"
updated: YYYY-MM-DD
---
# <Tên skill>
## Khi nào dùng
## Quy trình (số bước, trỏ § cho từng bước nhạy)
## Cạm bẫy
## Nguồn (địa chỉ tài liệu RAG_Library + JD)
```

- ≤ 150 dòng; quá dài → tách `references/`.
- `status` chỉ lên `active` sau khi **chủ vai duyệt nội dung** (GĐ1: Vân/Bảo Hà/OM Bảo/Đức Duy) — agent không tự duyệt.
- `sop-refs` là bắt buộc: không có § thì chưa phải skill NQH.

## 3. Địa chỉ tài liệu

Theo `08 - Context/NQH-SOP-Address.md`: `<Pháp nhân>-<Phòng>-<Loại>-<###>_<Tiêu đề>.md` + số mục `§`. Với Working docs (chưa có mã) → địa chỉ đường dẫn tương đối trong RAG_Library.

## 4. Quy trình ra skill

1. Agent soạn nháp theo chuẩn này (scaffold sẵn trong Shard).
2. Chủ vai duyệt nội dung — sửa chỗ sai quy trình, điền chỗ `[cần bổ sung]`.
3. Leak-scan diff (`nhatquangholding\.com|nqh\.com\.vn` + PII) trước push.
4. Push Shard → starter-vault submodule tự nhận (`git submodule update --remote`).

## 5. Scaffold đợt 1 (12 skill, 4 vai)

| Vai | Skill |
|---|---|
| Operations | `ops-sop-author` · `ops-handover-checklist` · `ops-giam-sat-thuc-thi` |
| HR | `hr-onboarding` · `hr-policy-lookup` · `hr-performance-review` |
| Kế toán/Kho | `ke-toan-doi-chieu-ncc` · `kho-grn-trong-ca` · `ke-toan-bao-cao-tuan` |
| Marketing | `mkt-brand-voice-check` · `mkt-campaign-brief` · `mkt-csat-nps` |

Ưu tiên GĐ1: 3 skill Kế toán/Kho (deadline ~25/09 — chỉ đạo CFO #22/#23: ngưỡng nhập kho Bflow + đối chiếu Bflow→Fast).
