# A mini version of the canvas registrar

Features:
The admin account can add students, instructors, and course accounts, and see the info related to each category
The student accounts can see the classes they have enrolled in and enroll in new classes
The instructor account can see the classes they are assigned to teach, but nothing else

How to use:
Website:
    Go to the url https://kelvinregistrar.onrender.com/adminLogin

Locally:
    Un comment (if + __name__ == "__main__") at the bottom of app.py and all the indented statements that go with it, then run app.py. The wehsite should apear in localhost:8080


File Structure:

```Python
├── Procfile.txt
├── README.md
├── __pycache__
│   ├── admin.cpython-312.pyc
│   ├── app.cpython-312.pyc
│   ├── instructor.cpython-312.pyc
│   ├── middleware.cpython-312.pyc
│   └── student.cpython-312.pyc
├── admin.py
├── app.py
├── app.wsgi
├── data
│   ├── adminData.csv
│   ├── courseData.csv
│   └── enrollment.csv
├── instructor.py
├── middleware.py
├── requirements.txt
├── session_data
│    └── container_file
│       └── *Lots of random files (the cookies)*
├── student.py
└── templates
    ├── admin
    │   ├── addCourse.html
    │   ├── addInstructor.html
    │   ├── addStudent.html
    │   ├── admin.html
    │   ├── adminLogin.html
    │   ├── showAllCourses.html
    │   ├── showAllInstructors.html
    │   └── showAllStudents.html
    ├── index.html
    ├── instructor
    │   ├── instructor.html
    │   ├── instructorLogin.html
    │   └── viewAssignedCourses.html
    └── student
        ├── enrollInACourse.html
        ├── student.html
        ├── studentLogin.html
        └── viewEnrolledCourses.html
```
