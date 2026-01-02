# PRD 2.2 Setup Instructions for PythonAnywhere

## Quick Setup (2 Commands)

```bash
# Step 1: Create all 55 courses
cd ~/uni-path/backend
python create_degree_chart_v2.py

# Step 2: Create chart schema with electives
python setup_chart_schema.py

# Step 3: Reload web app
# Go to: https://www.pythonanywhere.com/
# Click your web app → Reload
```

---

## What Gets Created

### After Step 1: 55 Computer Engineering Courses
- CE-101 through CE-107 (Semester 1)
- CE-201 through CE-208 (Semester 2)
- CE-301 through CE-307 (Semester 3)
- CE-401 through CE-407 (Semester 4)
- CE-501 through CE-507 (Semester 5)
- CE-601 through CE-607 (Semester 6)
- CE-701 through CE-707 (Semester 7)
- CE-801 through CE-805 (Semester 8)
- Plus: All prerequisite relationships (37) and co-requisite relationships (7)

### After Step 2: Chart Schema Setup
- 1 ChartSchema: Computer Science Bachelor (1392-1402)
- 2 CourseGroups: Technical Electives, General Electives
- 55 ChartNodes: Full degree chart structure

---

## Verify Success

### Check in Django Admin
```
https://isinanej.pythonanywhere.com/admin/courses/degreechart/
https://isinanej.pythonanywhere.com/admin/courses/chartschema/
https://isinanej.pythonanywhere.com/admin/courses/coursegroup/
https://isinanej.pythonanywhere.com/admin/courses/chartnode/
```

### Expected Results
- 55 courses visible
- 1 ChartSchema: "مهندسی کامپیوتر - کارشناسی (ورودی ۹۲-۴۰۲)"
- 2 CourseGroups with courses assigned
- 55 ChartNodes organized by semester

---

## If Error Occurs

### "Course not found" warnings
This is normal if you run Step 2 before Step 1. Just run Step 1 first, then Step 2.

### SSH Access
If you need to run commands directly:
```bash
ssh isinanej@ssh.pythonanywhere.com
cd ~/uni-path/backend
python manage.py migrate courses    # If migrations not applied yet
python create_degree_chart_v2.py    # Create courses
python setup_chart_schema.py        # Create schema
```

### Then Reload
Go to: https://www.pythonanywhere.com/  
Click: Web → Your app → Reload

---

## Troubleshooting

### Courses still not showing after Step 1?
```bash
cd ~/uni-path/backend
python manage.py shell
>>> from courses.models import Course
>>> Course.objects.filter(code__startswith='CE-').count()
# Should show 55 if successful
```

### ChartSchema not showing after Step 2?
```bash
cd ~/uni-path/backend
python manage.py shell
>>> from courses.models import ChartSchema
>>> ChartSchema.objects.all()
# Should show CS-BS-92-402
```

---

**That's it! PRD 2.2 is now live on PythonAnywhere!** 🚀
