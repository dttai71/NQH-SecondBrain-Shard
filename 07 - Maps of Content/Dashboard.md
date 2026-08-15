---
tags: [moc, dashboard]
---

# 📊 Dashboard

> Tự cập nhật từ mọi `#task` trong vault (cần plugin Dataview).

## 🔥 Quá hạn
```dataview
TASK
WHERE !completed AND due AND due < date(today)
SORT due ASC
```

## 📅 Đến hạn trong 3 ngày
```dataview
TASK
WHERE !completed AND due AND due >= date(today) AND due <= date(today) + dur(3 days)
SORT due ASC
```

## 📋 Dự án đang chạy
```dataview
TABLE status AS "Trạng thái", deadline AS "Deadline"
FROM "01 - Projects"
WHERE status != "done"
SORT deadline ASC
```

## ✅ Vừa xong (7 ngày)
```dataview
TASK
WHERE completed AND completion >= date(today) - dur(7 days)
LIMIT 15
```
