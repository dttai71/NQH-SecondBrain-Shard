---
nguồn: "NQH-HO-OPS-STD-MASTER_SOP_Registry + NQH-HO-QA-STD-001"
tự_sửa: false
mục_đích: "Dạy AI CÁCH DỰNG ĐỊA CHỈ tài liệu — thay cho việc phát một chỉ mục 500 dòng"
---

# Cách gọi tên & tìm tài liệu NQH

> 🤖 **File này cho TRỢ LÝ AI của bạn, không phải để bạn học thuộc.**
> Biết quy ước thì AI **tự dựng được địa chỉ** tới bất kỳ tài liệu nào — kể cả tài liệu **chưa có
> trong chỉ mục nào**. Quy ước ~20 dòng làm được việc mà một chỉ mục 500 dòng làm không xong,
> vì chỉ mục **luôn thiếu**, còn quy ước thì **không cũ đi**.

## 1. Cấu trúc mã tài liệu

```
<Pháp nhân>-<Phòng ban>-<Loại>-<###>_<Tiêu đề>.md

NQH-HO-FIN-SOP-008_Cash_Flow_Management.md
 │   │   │   │   │
 │   │   │   │   └── số thứ tự 001–999
 │   │   │   └────── loại tài liệu
 │   │   └────────── phòng ban
 │   └────────────── HO = Head Office (chỉ có ở NQH)
 └────────────────── pháp nhân
```

| Vị trí | Giá trị thường gặp |
|---|---|
| **Pháp nhân** | `NQH` *(Tập đoàn)* · `NQH-HO` *(Hội sở)* · `NQDL` *(Nhật Quang Đà Lạt)* |
| **Loại** | `SOP` quy trình · `STD` tiêu chuẩn · `POL` chính sách · `GDL` hướng dẫn · `CHK` checklist · `FM`/`FRM` biểu mẫu · `WI` chỉ dẫn công việc · `REF` tra cứu · `MP` quy trình gốc · `MDG` sổ dữ liệu gốc · `ADR` quyết định kiến trúc |

## 2. Phòng ban — viết tắt hay gặp

`FIN` Tài chính · `AC` Kế toán NQDL · `HR` Nhân sự · `AG` Hành chính · `IT` CNTT ·
`LEG`/`LEGAL` Pháp chế · `MKT` Marketing · `BRD` Thương hiệu · **`CT` Concept Studio** ·
`SAL` Kinh doanh · `BD` Phát triển KD · `CS` Chăm sóc KH · `OPS` Vận hành · `FB` An toàn TP ·
`PL`/`PRO` Mua hàng · `QA` Chất lượng · `OAS` OaaS · `STR` Chiến lược · `MDP` Dữ liệu gốc

> 🔴 **`CS` = Customer Service**, **KHÔNG** phải Concept Studio. Concept Studio là **`CT`**.
> *(Đây là ca đã gây nhầm thật — nhãn trong danh mục từng ghi sai.)*

## 3. Tài liệu riêng của từng cơ sở

```
NQDL-<BU>-<Bộ phận>-SOP-###      NQDL-BKL-BOH-SOP-001
```

`BKL` Buôn Kơ Lang · `THOM` Nhà hàng Thơm · `KUP` Kupid Homestay · `AFS` AirDream Forest Station ·
`TMM` Trại Mèo Mướp · `COM` Mâm Cơm · `REX` Rex Kingdom · `PZG` Pizza Gập · `CK` Bếp trung tâm
Bộ phận: `FOH` tiền sảnh · `BOH` hậu bếp · `HK` buồng phòng · `FB` ẩm thực · `FIN` tài chính ·
`HR` nhân sự · `QA` chất lượng · `SEC` an ninh · `MT` bảo trì · `FO` lễ tân

## 4. 🔗 Mở một tài liệu — công thức link

```
https://docs.nhatquangholding.com/viewer.html?file=RAG_Library/01_NQH-SOPs/<đường-dẫn>
```

Ví dụ:
```
.../viewer.html?file=RAG_Library/01_NQH-SOPs/01_Nhat_Quang_Holding/Finance/NQH-HO-FIN-SOP-008_Cash_Flow_Management.md
```

**Cần đăng nhập SSO** `id.nhatquangholding.com`. Thư mục gốc:

| Thư mục | Chứa gì |
|---|---|
| `01_Nhat_Quang_Holding/` | SOP cấp Tập đoàn *(`NQH-HO-*`)* |
| `02_Nhat_Quang_Da_Lat/` | SOP cấp NQDL *(`NQDL-*`)* |
| `03_Business_Units/` | SOP riêng từng cơ sở |
| `04_Compensation_KPI_Framework/` | lương · KPI · mã vị trí |
| `05_NQH_NQDL_JDs/` | mô tả công việc |

## 5. Ba cách tìm — theo thứ tự nên thử

| # | Cách | Khi nào |
|---|---|---|
| **1** | Hỏi **`@sop`** *(MTClaw)* bằng câu tự nhiên | mặc định — không cần biết mã |
| **2** | Tra **`08 - Context/My-SOPs.md`** trong chính vault này | tài liệu **của vị trí bạn** |
| **3** | **Dựng địa chỉ** theo §1–§4 rồi mở Docsify | biết mã, muốn mở thẳng |

## 6. ⚠️ Ba điều AI phải biết trước khi trả lời

| | |
|---|---|
| **① Mã có thể ĐÚNG mà tiêu đề SAI** | tài liệu trích dẫn có thể ghi tên cũ. **Tin TÊN FILE**, không tin tên trong bảng trích |
| **② Một mã có thể có HAI file** | *(đã có 7 ca)* — gặp thì **nêu cả hai**, đừng chọn giúp |
| **③ Không tìm thấy ≠ không tồn tại** | chỉ mục còn thiếu. Trả lời *"chưa tra được, hỏi QA"*, **đừng suy ra nội dung** |

> 🔑 **Không bịa nội dung SOP.** Không mở được thì nói không mở được. Một câu trả lời sai về quy
> trình **nguy hơn** một câu *"tôi chưa tra được"* — vì người ta sẽ làm theo.
