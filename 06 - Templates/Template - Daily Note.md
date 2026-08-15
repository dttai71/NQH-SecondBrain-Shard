---
tags: [daily]
date: "{{date:YYYY-MM-DD}}"
---

# {{date:YYYY-MM-DD}}

## 🎯 Ưu tiên hôm nay
- [ ]

## 📥 Ghi nhanh (capture)
-

## ✅ Việc đến hạn hôm nay
```dataview
TASK
WHERE !completed AND due AND due <= date(this.date)
SORT due ASC
```

## 🌙 Nhìn lại cuối ngày
- Làm tốt:
- Còn vướng:
