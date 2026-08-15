---
tags: [review, weekly]
week: "{{date:YYYY-[W]ww}}"
---

# Weekly Review — {{date:YYYY-[W]ww}}

## 1. Tuần qua
- Hoàn thành:
- Chưa xong / dời:

## 2. Việc đã xong (7 ngày)
```dataview
TASK
WHERE completed AND completion >= date(today) - dur(7 days)
```

## 3. Còn tồn / quá hạn
```dataview
TASK
WHERE !completed AND due AND due < date(today)
SORT due ASC
```

## 4. Kế hoạch tuần tới (3 ưu tiên)
1.
2.
3.
