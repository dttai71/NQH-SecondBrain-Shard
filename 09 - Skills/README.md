---
tags: [moc, skills, hermes]
---

# 🛠️ Skills — Bài học & quy trình tái dùng (Hermes)

> Mỗi khi bạn + AI giải xong một việc khó, **chắt lọc** thành 1 note ở đây để lần sau dùng lại. Hệ thống "học" dần theo thời gian.

## Vòng lặp chắt lọc
1. Giải xong việc khó → lệnh `/distill` (hoặc nói "ghi bài học này vào Skills").
2. AI tóm tắt: khi nào dùng, cách làm, cạm bẫy → tạo note từ [[Template - Skill]].
3. Lần sau gặp việc tương tự → AI đọc Skills trước, áp dụng.

## Vòng lặp 2 chiều
- Ý tưởng (ghi trong `01 - Projects`) → AI sinh nội dung/code.
- Sau khi xong → AI cập nhật lại tài liệu/pattern ở đây.

---

## 📦 Skill dùng chung của NQH **không nằm trong repo này**

Repo mẫu này **công khai** nên chỉ chứa **cấu trúc vault** — không chứa công cụ nội bộ.

Các skill NQH *(tra cứu SOP · thiết kế theo thương hiệu · ghi chú cuộc họp từ file ghi âm · xử lý video · lấy ảnh từ Studio · nội dung 3D)* nay tải riêng, **cần đăng nhập NQH SSO**:

**`docs.nhatquangholding.com`** → `RAG_Library/02_Training/07_Second_Brain_Training/skills/` → tải **`skills.zip`**

Giải nén rồi chạy **một lệnh**:
```bash
./install.sh "/đường/dẫn/tới/vault-cua-ban"
```
Nó đặt **một bản duy nhất** ở `~/.agents/skills/`, cho **Claude Code và Qwen cùng trỏ vào** bằng symlink, và chép phần ghi chú vào đúng `09 - Skills/` này. Hướng dẫn đầy đủ: `CAI-DAT.md` trong gói.

**Hai thứ cập nhật độc lập:**

| | Lấy ở đâu | Cập nhật bằng |
|---|---|---|
| **Vault mẫu** — cấu trúc, template | repo này (công khai) | `shardmind update` |
| **Skill** — công cụ NQH | `docs.nhatquangholding.com` (**cần SSO**) | tải `skills.zip` → `./install.sh` |

> Thư mục này **vẫn là nơi `/distill` ghi bài học của bạn** — phần trên không đổi. Nó chỉ không còn là nơi phát hành skill chung của NQH.
