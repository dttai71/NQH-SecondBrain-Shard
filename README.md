# SecondBrain NQH — vault Obsidian cá nhân cho nhân viên

> **CEO directive 07/2026:** Tất cả vị trí quản lý **BẮT BUỘC** cài đặt và sử dụng SecondBrain.

Vault mẫu cá nhân — mỗi nhân viên tự cài, tự dùng. Repo này (`dttai71/NQH-SecondBrain-Shard`)
chỉ chứa vault mẫu — đầy đủ hướng dẫn cài đặt/sử dụng nằm ở kho tài liệu đào tạo, repo khác:
[`02_Installation.md`](https://github.com/dttai71/NQH-GROUP-SOP-SYSTEM/blob/main/02_Training/07_Second_Brain_Training/02_Installation.md)
(hoặc [đọc trên Google Drive](https://drive.google.com/drive/folders/1AIXJJuvGWAfpOk6uk-yoEaFmDbHicCtV), không cần GitHub).

## ⭐ Cài nhanh nhất — qua ShardMind (khuyến nghị)

```bash
npm install -g shardmind
mkdir MySecondBrain && cd MySecondBrain
shardmind install github:dttai71/nqh-secondbrain-shard
```

Wizard hỏi 7 câu (họ tên, chức danh, phòng ban, PC/BU, báo cáo cho, trách nhiệm chính, SOP hay
dùng) → tự điền sẵn `08 - Context/My-Role.md`. Sau này đổi vai trò/nâng cấp: `shardmind update`
— tự merge, không mất phần bạn đã sửa tay.

## Cách khác — copy tay

1. **Tải/clone** repo này ra máy, đổi tên tuỳ ý (vd `MySecondBrain`).
2. Mở **Obsidian** → *Open folder as vault* → trỏ vào thư mục vừa tải.
3. Cài plugin: **Dataview**, **Tasks** (bắt buộc); **Periodic Notes**, **Templater** (khuyến nghị).
4. Mở `07 - Maps of Content/Home.md` để bắt đầu.
5. **Điền `08 - Context/My-Role.md`** — vai trò, phòng ban, PC/BU của bạn (để AI hiểu bạn).

## Dùng AI agent

Mở vault trong **VS Code** (File → Open Folder), rồi dùng extension AI:

- **⭐ Qwen Code Companion (mặc định)** — virtual key tự lấy tại
  `portal.nhatquangholding.com/my-ai-key` (đăng nhập NQH SSO/Zitadel). Xem chi tiết
  `02_Installation.md` mục B.
- **Kimi Code / Claude Code** — tuỳ chọn, chỉ dùng nếu cá nhân đã có tài khoản/quyền riêng.
- Chưa từng dùng VS Code/AI agent? Đọc **01_Beginner_Guide_AI_Agents.md** trong kho tài liệu đào
  tạo (link ở đầu file này).

## Kết nối thêm — MTClaw, Email/Lịch

1. Tạo file **`.env`** trong vault (đã có sẵn khung, điền key vào):
   ```
   NQH_AI_KEY=<lấy tại portal.nhatquangholding.com/my-ai-key>
   MTCLAW_API_KEY=<xin @devops>
   ```
2. Nói với AI agent: *"đọc .env, cấu hình MCP MTClaw/email giúp tôi"* — hoặc làm tay theo
   `02_Installation.md` mục F (Email/Lịch) + mục I (MTClaw).
3. **Đã tích hợp sẵn trong vault này:**
   - Hook `SessionStart` (`.claude/hooks/session-start-context.sh`) — mở phiên tự bơm task quá
     hạn thật (grep vault), không cần gõ `/daily` mới thấy.
   - `/daily` + `/weekly` tự quét email nếu MCP đã nối, báo chi phí token cuối phiên.
   - `guard-config.sh` — agent không tự sửa hook/settings.json của chính nó (an toàn cấu hình).

## Tra SOP

Hệ thống SOP NQH đã có trên AI-Platform (CBrain). **Không cần clone** hệ thống SOP — NQH đã
ngừng cấp quyền clone (chặn bản sao offline). Tra bằng:

- **Qua MTClaw:** nhắn agent **@sop** trong Pod → hỏi quy trình bất kỳ.
- **Qua AI agent trong vault:** gõ *"SOP quy trình mở ca nhà hàng"* → agent tra qua MTClaw MCP
  (nếu đã kết nối).

## Có sẵn trong vault

- Khung PARA (00–09), templates (Daily, Weekly, Meeting, Person, Project Brief, Decision).
- `Home` + `Dashboard` (Dataview tự gom task).
- `My-Role.md` — điền sẵn nếu cài qua ShardMind, hoặc điền tay.
- `.claude/` — quy ước + lệnh `/daily` `/weekly` `/inbox` `/distill` + hook git-safety +
  guard-config + session-start-context.
- File quy ước AI: `CLAUDE.md`, `AGENTS.md`, `GEMINI.md` (giống nhau — sửa thì đồng bộ cả 3).
- `.gitignore` (chặn `.env` — key cá nhân không bao giờ vào git).

## An toàn

Không đưa dữ liệu mật NQH vào vault/AI chia sẻ. AI chỉ soạn nháp — bạn duyệt trước khi gửi. Xem
`CLAUDE.md` mục AN TOÀN.
