---
tags: [skill]
domain: "SOP/Docs"
updated: "2026-08-15"
---

# Tra cứu & dẫn link SOP NQH qua Docsify (docs.nhatquangholding.com)

## Khi nào dùng
Cần tìm SOP/JD của phòng ban/vai trò mình, hoặc chia sẻ link tới 1 SOP cụ thể — mà bạn **không có** repo `NQH-GROUP-SOP-SYSTEM` clone local (đúng với đa số nhân viên, vì NQH đã ngừng cấp quyền clone).

## Cách làm (các bước)

1. Đăng nhập **id.nhatquangholding.com** (SSO công ty) → mở **docs.nhatquangholding.com**.
2. Tìm theo mã SOP hoặc duyệt cây thư mục (xem cấu trúc bên dưới). Danh mục trung tâm:
   `01_NQH-SOPs/01_Nhat_Quang_Holding/NQH-HO-OPS-STD-MASTER_SOP_Registry.md`
3. **Công thức link Docsify:**
   ```
   https://docs.nhatquangholding.com/viewer.html?file=RAG_Library/<đường dẫn trong 01_NQH-SOPs>
   ```
4. Muốn AI trong vault đọc nội dung SOP đó → copy nội dung từ trang Docsify → dán cho AI, nhờ tóm tắt/lưu vào `03 - Resources/`.

## Ví dụ / Mẫu
```text
https://docs.nhatquangholding.com/viewer.html?file=RAG_Library/01_NQH-SOPs/01_Nhat_Quang_Holding/NQH-HO-OPS-STD-MASTER_SOP_Registry.md

https://docs.nhatquangholding.com/viewer.html?file=RAG_Library/01_NQH-SOPs/01_Nhat_Quang_Holding/Finance/NQH-HO-FIN-SOP-008_Cash_Flow_Management.md
```

## Cấu trúc thư mục `01_NQH-SOPs/` (đoán đường dẫn khi không tìm được ngay)
```
01_NQH-SOPs/
├── 01_Nhat_Quang_Holding/    # Tier 1 — NQH-HO (Finance, HR, IT, BD, Marketing, Quality_Compliance, Legal, OaaS, Governance...)
├── 02_Nhat_Quang_Da_Lat/     # Tier 2 — NQDL (Operations, Sales, Accounting_Local, Procurement_Local, Customer_Services, PMO, Concept_Studio...)
├── 03_Business_Units/        # Tier 3 — theo BU (Thom, BKL, AirDream, Kupid, PizzaGap, Central_Kitchen, Trai_Meo_Muop...)
├── 04_Compensation_KPI_Framework/
├── 05_NQH_NQDL_JDs/          # Job Descriptions
├── 06_Accounting_Framework/  · 07_Accounting_Handbook/
├── 10_Archive/                # đã đóng — đừng dùng
└── 11_Working/                # bản nháp, chưa ratify — nếu dẫn link phải ghi rõ "chưa chính thức"
```

**Mã hoá tên file:** `<Entity>-<Dept>-<Type>-<###>_<Title>.md` — `Entity` = `NQH-HO` (trụ sở) / `NQDL` (Đà Lạt). `Type` = SOP/STD/GDL/POL/CHK/FM/RPT.

**Tài liệu nào cần theo vai trò của bạn?** Xem bảng ánh xạ trong [Module 06 — Roles](https://github.com/dttai71/NQH-GROUP-SOP-SYSTEM/blob/main/02_Training/07_Second_Brain_Training/06_Roles.md#tài-liệu-cần-tra-theo-vai-trò-sop--đào-tạo).

## Cạm bẫy (pitfalls)
- 🔴 Danh mục registry **chưa đầy đủ** — tra không thấy ≠ chưa có file. Nếu cần chắc chắn, nhờ AI hỏi qua MTClaw @sop (nếu đã nối) để đối chiếu.
- `10_Archive/` = ngừng dùng. `11_Working/` = nháp, chưa chính thức.
- Link Docsify **cần đăng nhập SSO** — khác với repo GitHub training (public, không cần tài khoản).

## Nguồn
- `NQH-GROUP-SOP-SYSTEM/01_NQH-SOPs/CLAUDE.md`, `NQH-HO-OPS-STD-MASTER_SOP_Registry.md`
