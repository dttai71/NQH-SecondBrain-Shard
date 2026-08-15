#!/usr/bin/env bash
# guard-config hook (PreToolUse: Edit|Write) — CONFIG SELF-PROTECTION
# Nguyên tắc hệ (ECC pattern): agent KHÔNG được sửa guardrail quản chính nó.
# Chặn Edit/Write vào .claude/hooks/ · .claude/rules/ · settings*.json của vault.
# Unlock: bạn tự tạo cờ ở TERMINAL:  touch .claude/hooks/.allow-guardrail-edit  (dùng xong xoá).
# Cờ tự hết hạn sau 15 phút (phòng quên xoá — fail-open không giới hạn thời gian là lỗ hổng).
# ponytail: chỉ chặn tool Edit/Write — Bash vẫn là root-escape; containment thật = agentsec Cap-2.
input=$(cat)
fp=$(printf '%s' "$input" | python3 -c "import sys,json;d=json.load(sys.stdin);print(d.get('tool_input',{}).get('file_path',''))" 2>/dev/null)

# Resolve theo REALPATH (theo symlink, chuẩn hoá ../ ./) rồi so với thư mục thật — so khớp
# chuỗi thô bị né được qua symlink trỏ vào trong (vd 1 file gốc vault symlink -> .claude/hooks/x.sh).
resolved=$(python3 -c "
import os, sys
base = os.environ.get('CLAUDE_PROJECT_DIR', '.')
fp = sys.argv[1] if len(sys.argv) > 1 else ''
if not fp:
    print('')
    sys.exit(0)
p = fp if os.path.isabs(fp) else os.path.join(base, fp)
print(os.path.realpath(p))
" "$fp" 2>/dev/null)
guard_hooks=$(python3 -c "import os;print(os.path.realpath(os.path.join(os.environ.get('CLAUDE_PROJECT_DIR','.'), '.claude/hooks')))" 2>/dev/null)
guard_rules=$(python3 -c "import os;print(os.path.realpath(os.path.join(os.environ.get('CLAUDE_PROJECT_DIR','.'), '.claude/rules')))" 2>/dev/null)
guard_settings=$(python3 -c "import os;print(os.path.realpath(os.path.join(os.environ.get('CLAUDE_PROJECT_DIR','.'), '.claude/settings.json')))" 2>/dev/null)
guard_settings_local=$(python3 -c "import os;print(os.path.realpath(os.path.join(os.environ.get('CLAUDE_PROJECT_DIR','.'), '.claude/settings.local.json')))" 2>/dev/null)

is_protected=0
case "$resolved" in
  "$guard_hooks"/*|"$guard_rules"/*|"$guard_settings"|"$guard_settings_local") is_protected=1 ;;
esac

flag="$CLAUDE_PROJECT_DIR/.claude/hooks/.allow-guardrail-edit"

if [ "$resolved" = "$(python3 -c "import os;print(os.path.realpath('$flag'))" 2>/dev/null)" ]; then
  echo "🚫 guard-config: cờ unlock chỉ bạn tự tạo từ terminal, agent không tự cấp." >&2
  exit 2
fi

if [ "$is_protected" = "1" ]; then
  if [ -f "$flag" ]; then
    age=$(( $(date +%s) - $(stat -f %m "$flag" 2>/dev/null || stat -c %Y "$flag" 2>/dev/null || echo 0) ))
    if [ "$age" -le 900 ]; then
      exit 0
    fi
    echo "🚫 guard-config: cờ unlock đã quá 15 phút (hết hạn tự động) — chạy lại: touch \"$flag\"." >&2
    exit 2
  fi
  echo "🚫 guard-config: agent không sửa guardrail quản chính nó ($fp)." >&2
  echo "→ Duyệt thì chạy ở terminal: touch .claude/hooks/.allow-guardrail-edit (xong xoá cờ)." >&2
  exit 2
fi
exit 0
