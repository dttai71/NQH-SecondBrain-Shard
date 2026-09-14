#!/usr/bin/env bash
# oga-fetch — kéo asset từ Studio về vault Inbox, kèm sidecar provenance (ADR-030 §D5, ADR-029).
set -euo pipefail

: "${STUDIO_URL:?thiếu STUDIO_URL — đặt trong .env của vault}"
: "${STUDIO_ASSET_KEY:?thiếu STUDIO_ASSET_KEY — key cá nhân, hỏi @itadmin}"
command -v jq >/dev/null || { echo "cần jq" >&2; exit 1; }
if command -v sha256sum >/dev/null; then SHA() { sha256sum "$1" | cut -d' ' -f1; }
elif command -v shasum   >/dev/null; then SHA() { shasum -a 256 "$1" | cut -d' ' -f1; }
else echo "cần sha256sum hoặc shasum" >&2; exit 1; fi

SINCE="" ; ID="" ; DEST="00 - Inbox/studio" ; LIMIT=50
while [ $# -gt 0 ]; do
  case "$1" in
    --since) SINCE="${2:?--since cần giá trị ISO8601}"; shift 2 ;;
    --id)    ID="${2:?--id cần giá trị}";              shift 2 ;;
    --dest)  DEST="${2:?--dest cần thư mục}";          shift 2 ;;
    --limit) LIMIT="${2:?--limit cần số}";             shift 2 ;;
    *) echo "tham số lạ: $1" >&2; exit 2 ;;
  esac
done

if [ -n "$ID" ] && ! printf '%s' "$ID" | grep -Eq '^[0-9a-f]{32}$'; then
  echo "id sai định dạng (cần 32 hex thường): $ID" >&2; exit 2
fi
if [ -z "$SINCE" ]; then
  SINCE="$(date -u -d '24 hours ago' +%Y-%m-%dT%H:%M:%SZ 2>/dev/null \
        || date -u -v-24H +%Y-%m-%dT%H:%M:%SZ)"
fi
mkdir -p "$DEST"
API="${STUDIO_URL%/}/api/v1/media/assets"

# get <url> <outfile> -> in ra HTTP code, body ghi vào outfile
get() { curl -sS -o "$2" -w '%{http_code}' -H "x-api-key: ${STUDIO_ASSET_KEY}" "$1"; }

explain() { case "$1" in
  401) echo "401 — key hết hạn hoặc bị thu hồi, hỏi @itadmin cấp lại" ;;
  404) echo "404 — asset đã bị dọn (retention 30 ngày)" ;;
  429) echo "429 — quá 60 req/phút, chờ rồi chạy lại" ;;
  400) echo "400 — tham số sai định dạng" ;;
  *)   echo "HTTP $1" ;;
esac; }

tmp="$(mktemp -d)"; trap 'rm -rf "$tmp"' EXIT

if [ -n "$ID" ]; then IDS="$ID"; else
  code="$(get "${API}?since=${SINCE}&limit=${LIMIT}" "$tmp/list.json")"
  [ "$code" = 200 ] || { explain "$code" >&2; exit 1; }
  IDS="$(jq -r '.assets[].id' "$tmp/list.json")"
fi

n=0
for id in $IDS; do
  printf '%s' "$id" | grep -Eq '^[0-9a-f]{32}$' || { echo "bỏ qua id lạ: $id" >&2; continue; }
  code="$(get "${API}/${id}" "$tmp/sidecar.json")"
  [ "$code" = 200 ] || { echo "sidecar $id: $(explain "$code")" >&2; continue; }

  created="$(jq -r '.created_at' "$tmp/sidecar.json" | tr ':' '-')"  # ":" không hợp lệ trong tên file trên vài FS
  ctype="$(jq -r '.content_type // ""' "$tmp/sidecar.json")"
  want="$(jq -r '.sha256 // ""' "$tmp/sidecar.json")"
  case "$ctype" in
    image/png) ext=png ;; video/mp4) ext=mp4 ;; audio/mpeg) ext=mp3 ;;
    *) echo "bỏ qua $id: content_type lạ '$ctype'" >&2; continue ;;
  esac
  [ -n "$want" ] || { echo "bỏ qua $id: sidecar thiếu sha256" >&2; continue; }

  base="${DEST}/${created}-${id}"
  if [ -e "${base}.${ext}" ]; then echo "đã có, bỏ qua: ${base}.${ext}"; continue; fi

  code="$(get "${API}/${id}/download" "$tmp/blob")"
  [ "$code" = 200 ] || { echo "download $id: $(explain "$code")" >&2; continue; }

  got="$(SHA "$tmp/blob")"
  [ "$got" = "$want" ] || { echo "sha256 KHÔNG khớp $id (mong $want, được $got) — huỷ" >&2; continue; }

  # sidecar luôn đi cùng file — không bao giờ tách (ADR-029)
  cp "$tmp/blob" "${base}.${ext}"
  cp "$tmp/sidecar.json" "${base}.json"
  n=$((n+1)); echo "đã lấy: ${base}.${ext}"
done
echo "xong: $n asset vào ${DEST} (since=${SINCE})"

# self-check (không chạy trong CI, chạy tay với mock):
#   python3 -m http.server 8099 --directory ./mock &   # mock/api/v1/media/assets{,/<id>,/<id>/download}
#   STUDIO_URL=http://127.0.0.1:8099 STUDIO_ASSET_KEY=dummy \
#     bash fetch.sh --since 2026-09-01T00:00:00Z --dest /tmp/oga-inbox
#   # kỳ vọng: mỗi asset có cả .png lẫn .json; sửa 1 byte trong mock blob -> báo "sha256 KHÔNG khớp", không ghi file
#   bash fetch.sh --id ../../etc/passwd   # kỳ vọng: exit 2, "id sai định dạng"
