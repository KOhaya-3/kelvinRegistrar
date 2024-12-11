from bottle import Bottle, template, redirect, request  
from middleware import *
import pandas as pd 
import os

# IMPORTANT: work on addStudents and come back to addCourse to work on adding students to the courses (just add their first and last name, username and password)

#start the adminApp
adminApp = Bottle()  





#--------Validation functions--------
def validateName(name):  
  if name.isalpha() and " " not in name:  
    return True  
  else:  
    return False  

def usernameExistsAlready(data,username):  
  if data["Username"].isin([username]).any():  
    return True  
  else:  
    return False 






#--------Login Route--------
@adminApp.route('/')  
@requiresLogin
def admin():  
   session = request.environ.get('beaker.session')  
   firstName = session.get("firstName") 

   return template("templates/admin/admin", firstName=firstName)







#--------Adding and validating students--------
@adminApp.route("/addStudent")
@requiresLogin
def addStudent():
  invalidFirstName = request.query.get("invalidFirstName", False)
  invalidLastName = request.query.get("invalidLastName", False)  
  invalidUsername = request.query.get("invalidUsername", False) 
  return template("templates/admin/addStudent", invalidFirstName=invalidFirstName, invalidLastName=invalidLastName, invalidUsername=invalidUsername)

@adminApp.post("/addStudentValidation")
def validateStudent():
  if os.path.exists("data/studentData.csv"):
        studentData = pd.read_csv("data/studentData.csv", dtype=str)
  else:
    studentData = pd.DataFrame(columns=["First Name", "Last Name", "Username", "Password"])

  # Get all the variables from the form input fields  
  firstName = request.forms.get("firstName").strip()  
  lastName = request.forms.get("lastName").strip()  
  username = request.forms.get("username").strip()  
  password = request.forms.get("password").strip()

   
  # Validate the input fields  
  firstNameValidation = validateName(firstName)  
  lastNameValidation = validateName(lastName)  
  usernameValidation = usernameExistsAlready(studentData, username)  
  

  # Check if any of the fields are invalid  
  if not firstNameValidation or not lastNameValidation or usernameValidation:  
    return redirect(f"/admin/addStudent?invalidFirstName={not firstNameValidation}&invalidLastName={ not lastNameValidation}&invalidUsername={usernameValidation}")  
  else:  
    # Create a new instructor DataFrame  
    newStudent = pd.DataFrame({  
      "First Name": [firstName],  
      "Last Name": [lastName],  
      "Username": [username],  
      "Password": [password] 
    }) 

      # Concatenate the new instructor with the existing instructor data  
    studentData = pd.concat([studentData, newStudent])  

    # Save the updated instructor data to the CSV file  
    studentData.to_csv("data/studentData.csv", index=False)  

    return template("""
<p>Student Added successfully</p>
<a href="/admin">Back to Dashboard</a>
""")








#--------Adding and validationg instructors--------
@adminApp.route("/addInstructor")
@requiresLogin
def addInstructor():
    firstNameValidation = request.query.get("invalidFirstName", " ")
    lastNameValidation = request.query.get("invalidLastName", " ")
    usernameValidation = request.query.get("invalidUsername", " ")
    return template("templates/admin/addInstructor",invalidFirstName=firstNameValidation,invalidLastName=lastNameValidation,invalidUsername=usernameValidation)


#validation logic for the forms from the addInstructor Route
@adminApp.post("/addInstructorValidation")  
def instructorValidation():  
    if os.path.exists("data/instructorData.csv"):
        instructorData = pd.read_csv("data/instructorData.csv", dtype=str)
    else:
      instructorData = pd.DataFrame(columns=["First Name", "Last Name", "Username", "Password","Position"])
  
    # Get all the variables from the form input fields  
    firstName = request.forms.get("firstName").strip()  
    lastName = request.forms.get("lastName").strip()  
    username = request.forms.get("username").strip()  
    password = request.forms.get("password").strip()
    position = request.forms.get("position")
  

    # Validate the input fields  
    firstNameValidation = validateName(firstName)  
    lastNameValidation = validateName(lastName)  
    usernameValidation = usernameExistsAlready(instructorData, username)  
   
  
   # Check if any of the fields are invalid  
    if not firstNameValidation or not lastNameValidation or usernameValidation:  
      return redirect(f"/admin/addInstructor?invalidFirstName={not firstNameValidation}&invalidLastName={ not lastNameValidation}&invalidUsername={usernameValidation}")  
    else:  
      # Create a new instructor DataFrame  
      newInstructor = pd.DataFrame({  
        "First Name": [firstName],  
        "Last Name": [lastName],  
        "Username": [username],  
        "Password": [password],
        "Position": [position] 
      }) 
  
      # Concatenate the new instructor with the existing instructor data  
      instructorData = pd.concat([instructorData, newInstructor])  
  
      # Save the updated instructor data to the CSV file  
      instructorData.to_csv("data/instructorData.csv", index=False)  
  
      return template("""
<p>Instructor Added successfully</p>
<a href="/admin">Back to Dashboard</a>
""")








#--------Adding and validating courses--------
@adminApp.route("/addCourse")
@requiresLogin
def addCourse():
    if os.path.exists("data/instructorData.csv"):
        instructorUsernamesExist = True
        instructorData = pd.read_csv("data/instructorData.csv").to_dict("records")
    else:
       instructorUsernamesExist = False
       instructorData = None

    numberAlreadyExists = request.query.get("numberAlreadyExists", False)
    titleAlreadyExists = request.query.get("titleAlreadyExists", False)

    return template("templates/admin/addCourse", instructorUsernamesExist=instructorUsernamesExist, instructor_dict=instructorData, numberAlreadyExists=numberAlreadyExists, titleAlreadyExists=titleAlreadyExists)


#Handling the Post method for the admin course validation. This is the validation for the addCourse Route
@adminApp.post("/addCourseValidation")
def courseValidation():
    #True = the value is unique; False = the value isn't unique
    def isUnique(courseData, varToCheck, column):
        if courseData.empty:
           return True
        return not courseData[column].isin([varToCheck]).any()

    if os.path.exists("data/courseData.csv"):
        courseData = pd.read_csv("data/courseData.csv", dtype=str)
    else:
        courseData = pd.DataFrame(columns=["Title", "Number", "Instructor"])

    if os.path.exists("data/enrollment.csv"):
       enrollment = pd.read_csv("data/enrollment.csv", dtype=str)
    else:
       enrollment = pd.DataFrame(columns=["Title","Number","Instructor","Instructor First Name","Instructor Last Name","Student Usernames", "Student First Names", "Student Last Names"])
    


    #get the title, numbers, and list of usernames from the template
    #add that to the dataframe and save it
    title = request.forms.get("title").strip()
    number = str(request.forms.get("number"))
    
    if os.path.exists("data/instructorData.csv"):
        instructorData = pd.read_csv("data/instructorData.csv")
        instructorUsername = request.forms.get("instructorUsername")
        matchingInstructorInfo = instructorData[instructorData["Username"] == instructorUsername]
        instructorFirstName = matchingInstructorInfo["First Name"].values[0]
        instructorLastName = matchingInstructorInfo["Last Name"].values[0]
    else:
      instructorUsername = ""
      instructorFirstName = ""
      instructorLastName = ""

    #validation for the course number
    validNumber = isUnique(courseData, number, "Number")
    validTitle = isUnique(courseData, title, "Title")


    if validTitle == False or validNumber == False:
        return redirect(f"/admin/addCourse?numberAlreadyExists={not validNumber}&titleAlreadyExists={not validTitle}")
    else:
        newCourse = pd.DataFrame({
        "Title": [title],
        "Number": [number],
        "Instructor": [instructorUsername]
        })

        newEnrollmentCourse = pd.DataFrame({
            "Title": [title],
            "Number": [number],
            "Instructor": [instructorUsername],
            "Instructor First Name": [instructorFirstName],
            "Instructor Last Name": [instructorLastName],
            "Student Usernames": [""],
            "Student First Names": [""], 
            "Student Last Names": [""]
        })


        courseData = pd.concat([courseData, newCourse])
        enrollment = pd.concat([enrollment, newEnrollmentCourse])
        courseData.to_csv("data/courseData.csv", index=False)
        enrollment.to_csv("data/enrollment.csv", index=False)

    
    
    return template("""
    <p>Course Added successfully</p>
    <a href="/admin">Back to Dashboard</a>
    """)








#--------Show All Courses Route--------    
@adminApp.route("/showAllCourses")
@requiresLogin
def showAllCourses():
  if os.path.exists("data/courseData.csv"):
    coursesExist = True
    course_dict = pd.read_csv("data/courseData.csv").fillna("No Instructor").to_dict("records")
    
  else:
    coursesExist = False
    course_dict = []
      
  return template("templates/admin/showAllCourses", coursesExist=coursesExist, course_dict=course_dict)








#--------Show All Instructors Route--------
@adminApp.route("/showAllInstructors")
@requiresLogin
def showAllInstructors():
  if os.path.exists("data/instructorData.csv"):
    instructorsExist = True
    instructor_dict = pd.read_csv("data/instructorData.csv").to_dict("records")
  else:
    instructorsExist = False
    instructor_dict = []
      
  return template("templates/admin/showAllInstructors", instructorsExist=instructorsExist, instructor_dict=instructor_dict)







#--------Show All Students Route--------
@adminApp.route("/showAllStudents")
@requiresLogin
def showAllStudents():
  if os.path.exists("data/studentData.csv"):
    studentsExist = True
    student_dict = pd.read_csv("data/studentData.csv").to_dict("records")
  else:
    studentsExist = False
    student_dict = []
  
  return template("templates/admin/showAllStudents", studentsExist=studentsExist, student_dict=student_dict)
  