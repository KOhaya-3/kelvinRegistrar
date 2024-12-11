# A mini version of the canvas registrar

Features:
The admin account can add students, instructors, and course accounts, and see the info related to each category
The student accounts can see the classes they have enrolled in and enroll in new classes
The instructor account can see the classes they are assigned to teach, but nothing else

File Structure:

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
│   ├── container_file
│   │   ├── 0
│   │   │   ├── 00
│   │   │   │   └── 0057dc8f51c64eb888ddb1f9b62edea3.cache
│   │   │   ├── 04
│   │   │   │   └── 0461b1e728d34c9a9caa432ab76d0f54.cache
│   │   │   └── 08
│   │   │       ├── 0843263130a349c7993c55c4a0bf911b.cache
│   │   │       └── 087e4d178a5c42b4903169cc49d91ba4.cache
│   │   ├── 1
│   │   │   ├── 10
│   │   │   │   └── 102b178cf6a54f47b7b3180f6a7c2d71.cache
│   │   │   ├── 11
│   │   │   │   └── 11d1c2ac1ad5498b891392e7a2e50c3e.cache
│   │   │   ├── 14
│   │   │   │   └── 1460c899273a41bcbc44b8ddc93ecaf9.cache
│   │   │   ├── 1a
│   │   │   │   └── 1ae81c1c161d43f3b92e1323de02e690.cache
│   │   │   ├── 1c
│   │   │   │   └── 1cc9c5d271064a86ac22db4758b4529a.cache
│   │   │   └── 1f
│   │   │       └── 1fe8ddb7150d4dc3bf8001b831f8aa03.cache
│   │   ├── 2
│   │   │   ├── 25
│   │   │   │   └── 2594422af7a54703a981863e7889c942.cache
│   │   │   ├── 26
│   │   │   │   └── 2638bbcaeb5d4865bebe3a83f0d205af.cache
│   │   │   └── 2d
│   │   │       └── 2d978f633696424a982328c38e47ba69.cache
│   │   ├── 3
│   │   │   ├── 32
│   │   │   │   └── 322912e0c64a4b75bdd77c8429b87938.cache
│   │   │   ├── 38
│   │   │   │   └── 386d9cc070a84477b74c01972b3266cf.cache
│   │   │   └── 3c
│   │   │       └── 3c4c9b1d11f6464ea45f91176e1fd37f.cache
│   │   ├── 4
│   │   │   ├── 43
│   │   │   │   ├── 43b1e5875eaf48cda9a164e9d3561014.cache
│   │   │   │   └── 43bc5228bf3a406080556f7c322b20a1.cache
│   │   │   ├── 45
│   │   │   │   └── 45c06d09714145fc84485454a05e95f1.cache
│   │   │   ├── 4c
│   │   │   │   └── 4c4d74d68e1c41a6beacbdec504cadb8.cache
│   │   │   ├── 4d
│   │   │   │   └── 4d9dc45ab2a54d57b4e9c971d08ae300.cache
│   │   │   └── 4e
│   │   │       └── 4e01631c22eb45e8a077426e8e681895.cache
│   │   ├── 5
│   │   │   ├── 51
│   │   │   │   └── 51ea7d3cfc924fb28cfcf46872ced1f7.cache
│   │   │   ├── 52
│   │   │   │   └── 5230ef8dd33d41218adf434bfd1bf2e7.cache
│   │   │   ├── 53
│   │   │   │   └── 536cf27cdc3645e3a7c544e1cd740966.cache
│   │   │   ├── 58
│   │   │   │   └── 58fbf699704a4c01b5230c114cbc2e1c.cache
│   │   │   ├── 5a
│   │   │   │   └── 5ab35ff4c669467c84cc476019a77308.cache
│   │   │   ├── 5b
│   │   │   │   └── 5b1de7c886894c72b7356cb6afe8f169.cache
│   │   │   └── 5d
│   │   │       └── 5dbdb5d89ce84e9fa29cd1a65e477ee2.cache
│   │   ├── 6
│   │   │   ├── 61
│   │   │   │   └── 6103e874bd3548ac86e095650a806392.cache
│   │   │   ├── 62
│   │   │   │   └── 623e4795920c4c8eb0566f9046dd9b32.cache
│   │   │   ├── 64
│   │   │   │   ├── 6441c9367a0c4dcb9af1ced4b253ce01.cache
│   │   │   │   └── 64485f0b407e46ea80af4269d2156106.cache
│   │   │   └── 6b
│   │   │       └── 6b8ce1854b9f46dbb2e3c5b9b2a6a783.cache
│   │   ├── 7
│   │   │   └── 74
│   │   │       └── 74e68c22aace4a11ba37b5be1e6d3752.cache
│   │   ├── 8
│   │   │   ├── 81
│   │   │   │   └── 819edb8c3e534dfdaab9bcbac69f9a6c.cache
│   │   │   ├── 82
│   │   │   │   └── 8270590d154c4ad29eca2c3889108700.cache
│   │   │   ├── 88
│   │   │   │   └── 8855baef76134074a898b1551b701368.cache
│   │   │   └── 8e
│   │   │       └── 8e47fd23d05248bc8c71a4c7515dea09.cache
│   │   ├── 9
│   │   │   ├── 96
│   │   │   │   └── 962782ce719b4988a871bfebb604f4d8.cache
│   │   │   ├── 97
│   │   │   │   └── 97797a87cbd3495087b2e9097fa3b1ce.cache
│   │   │   ├── 98
│   │   │   │   └── 987930b1bfed49b18d58d117cf88fb7a.cache
│   │   │   ├── 9a
│   │   │   │   └── 9a2daae0d11b48099c0f25b4d4432adc.cache
│   │   │   ├── 9b
│   │   │   │   ├── 9bf28b7aea854a79a92690de25faad18.cache
│   │   │   │   └── 9bf59b0481a9400b99d5356c957ba3d5.cache
│   │   │   └── 9d
│   │   │       ├── 9d42a12e23eb4b1fb9f380c6488dbb49.cache
│   │   │       └── 9da3a8bbd4ef48129b8e9b1994ab51c7.cache
│   │   ├── a
│   │   │   ├── a0
│   │   │   │   └── a011ba00c9a140f79dcbfb675335acd6.cache
│   │   │   ├── a3
│   │   │   │   └── a380e0c9547c48918ecdf684f35404d0.cache
│   │   │   ├── a5
│   │   │   │   └── a536b14197f5469b9ec30f5b5f396271.cache
│   │   │   ├── a7
│   │   │   │   └── a7b5b68b213b4d4e83a68a174d7cac10.cache
│   │   │   ├── a8
│   │   │   │   └── a8ac250cf4024d79afbf9db41674b6ee.cache
│   │   │   └── ae
│   │   │       └── ae41ae1c77c340aea10aa281c7cd9cd3.cache
│   │   ├── b
│   │   │   ├── b2
│   │   │   │   ├── b2a8231d529444c3a77b5143a5e209d2.cache
│   │   │   │   └── b2bb8f444d86423fac2b7f1dd9d82898.cache
│   │   │   ├── b3
│   │   │   │   └── b3bf5b660db14f8ca230fb219e2fed75.cache
│   │   │   ├── b5
│   │   │   │   └── b5bd5fac386640b29e7c928b56e68b36.cache
│   │   │   ├── b6
│   │   │   │   └── b61b7354100146789335c49d8f342284.cache
│   │   │   ├── bb
│   │   │   │   └── bbd7c1b5488345df8b16ada150c5f479.cache
│   │   │   ├── be
│   │   │   │   └── be69f4984526412b929fd8062dea7506.cache
│   │   │   └── bf
│   │   │       └── bf3e5174b4d94ed082e7628f3868a22c.cache
│   │   ├── c
│   │   │   └── c6
│   │   │       └── c69e54ea483f41eaa44b7d3039a94dd8.cache
│   │   ├── d
│   │   │   ├── d3
│   │   │   │   └── d3adcc748cad483aa587b375811211f9.cache
│   │   │   ├── d4
│   │   │   │   └── d4e273a84aec4a87959cb847be928a12.cache
│   │   │   ├── d8
│   │   │   │   └── d8efc616692343bb90cd08eb06917632.cache
│   │   │   └── db
│   │   │       └── db5ff4ce3dae4551a34a6078a0120209.cache
│   │   ├── e
│   │   │   ├── e1
│   │   │   │   └── e18b039eb5bd4db08fc0c53b952084b8.cache
│   │   │   ├── e3
│   │   │   │   └── e37575879000483ea589de7207b3c531.cache
│   │   │   └── ea
│   │   │       └── ea3e482637fe458ca7d8b8715cdc0a7e.cache
│   │   └── f
│   │       ├── f0
│   │       │   └── f081f3674df64a1b80cf98f05c4a5592.cache
│   │       ├── f1
│   │       │   └── f1c3c160939446c688e597915d55ec29.cache
│   │       ├── f6
│   │       │   ├── f6044e529b5f4abfa898f8f243844072.cache
│   │       │   └── f649459ea02b4b49b6385fe31aef8f80.cache
│   │       ├── fb
│   │       │   └── fbc6d6099b2e4ee48c77e6c6c99707d2.cache
│   │       ├── fd
│   │       │   └── fdb208e8a4244c03aa6d6217106b9007.cache
│   │       └── fe
│   │           └── fe3126c224c349d5907794bc33868ad3.cache
│   └── container_file_lock
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
