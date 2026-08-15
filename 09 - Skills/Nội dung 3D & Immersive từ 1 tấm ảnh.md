---
tags: [skill, marketing, concept-studio, visual, 3d, video]
domain: "Marketing & Concept Studio — nội dung 3D / immersive"
updated: "2026-07-30"
---

# Biến 1 tấm ảnh thành nội dung 3D / immersive — chọn đúng cách, không đốt tiền

## Khi nào dùng
Khi khách hàng / chiến dịch cần cảm giác **3D, chiều sâu, "bay" qua khung cảnh** — sản phẩm xoay được, landing page cuộn immersive, video nhiều cảnh mượt. Điểm mấu chốt: **có ít nhất 3 cách rất khác nhau**, chọn sai = tốn tiền hoặc ra sản phẩm sai loại. Skill này giúp chọn đúng ngay từ lúc brief.

## Cách làm — hỏi 1 câu trước: "Đầu ra là FILE hay TRẢI NGHIỆM?"

**1. Cần một FILE 3D tải về được** (xoay sản phẩm 360°, AR, in 3D, đưa vào game/3D tool)
→ **Concept Studio → Image→3D** (chạy cloud qua MuAPI: Meshy / Tripo). 1 ảnh → file **`.glb`** có texture.
- Brief tốt: **1 ảnh sản phẩm/vật thể, nền sạch, chụp chính diện, đủ sáng**. Vật thể đơn (chai, hộp, ghế, logo) cho kết quả tốt nhất.
- Cần geometry chuẩn hơn cho vật phức tạp/bất đối xứng → dùng **nhiều ảnh (1–4 góc)**.

**2. Cần một TRẢI NGHIỆM WEB cuộn** (landing page "bay" qua các cảnh, kiểu cinematic scroll)
→ **"Scroll Story"** — KHÔNG cần mesh 3D thật. Cách làm: dựng vài cảnh (ảnh) + dùng **video (Seedance/Kling qua Video Studio)** quay chuyển động camera giữa các cảnh, rồi **cuộn chuột điều khiển thời điểm phát video** → cảm giác 3D chiều sâu với chi phí thấp hơn nhiều so với 3D thật.
- Dùng khi đích đến là **web/landing page**, không phải file mesh.

**3. Cần VIDEO nhiều cảnh nối liền, không giật cắt**
→ Kỹ thuật **"khoá khung hình" (frame-lock)**: clip nối được tạo từ **đúng khung cuối của cảnh trước + khung đầu của cảnh sau** → mọi mối nối trùng khớp từng khung, không thấy vết cắt. Brief cho Concept/Video Studio: nói rõ "nối liền, không cắt cảnh".

> **Quy tắc chọn:** File để tải/AR/in → **cách 1 (mesh)**. Trải nghiệm cuộn trên web → **cách 2 (scroll-story)**. Video liền mạch → **cách 3 (frame-lock)**. Đừng mặc định "3D = mesh" — phần lớn nhu cầu marketing thực ra là **cách 2/3, rẻ hơn**.

## Cạm bẫy
- **Ảnh đơn ra 3D yếu với: cảnh phức tạp, người, vật phản chiếu/trong suốt, chi tiết mảnh.** Mesh xấu ở mấy ca này là **bình thường, không phải lỗi** — chọn vật thể đơn giản, nền sạch.
- **Mỗi lần tạo 3D/video là TỐN TIỀN thật** (trả theo lượt, có cổng chặn theo nhu cầu). Không spam gen — brief kỹ, gen ít lần.
- **Scroll-story nhân đôi số video** (bản mobile 9:16 render riêng, không cắt-crop) → chi phí tăng. Cân nhắc có cần bản mobile không.
- **Chọn sai đầu ra**: làm mesh `.glb` trong khi khách chỉ cần landing page → mất tiền + thời gian. Luôn hỏi "file hay trải nghiệm?" trước.
- **Trạng thái công cụ (07/2026):** *Concept Sketch, Image Studio, Video Studio* = đang chạy. *Image→3D (mesh)* và *Scroll Story* = **đang thiết kế, sắp có** — hiện brief trước để chuẩn bị, hỏi Pod-G/Concept Studio về ngày mở.

## Nguồn
- Chắt lọc từ: repo OSS `github.com/oso95/scroll-world` (kỹ thuật scroll-scrub + frame-lock, chạy trên chính Seedance/Kling mà OGA đang dùng).
- MuAPI image→3D (Meshy / Tripo): [[https://muapi.ai/playground]] — endpoint `meshy-6-image-to-3d`, `tripo3d-h31-image-to-3d`, output `.glb`.
- Spec OGA: `docs/02-design/specs/image-to-3d-concept-preset.md` (PR #67) + Video Studio lane.
- Chắt lọc từ: [[Template - Skill]]
