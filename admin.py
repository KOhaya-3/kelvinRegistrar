from bottle import Bottle, template, redirect, request  
from middleware import *
import pandas as pd 
from time import time
import os

# IMPORTANT: work on addStudents and come back to addCourse to work on adding students to the courses (just add their first and last name, username and password)

#start the adminApp
adminApp = Bottle()  





#--------Validation functions--------
def isValid(name):  
  if name.isalpha() and " " not in name:  
    return True  
  else:  
    return False  

def usernameExists(data,username): 
  if data.empty:
    return True
  return data["Username"].isin([username]).any() 
 
  
def isUnique(courseData, varToCheck, column):
    if courseData.empty:
        return True
    return not courseData[column].isin([varToCheck]).any()






#--------Login Route--------
@adminApp.route('/')  
@requiresLogin
def admin():  
   session = request.environ.get('beaker.session')  
   firstName = session.get("firstName") 

   return template("templates/admin/admin", firstName=firstName, time=int(time()))







#--------Adding and validating students--------
@adminApp.route("/addStudent")
@requiresLogin
def addStudent():
  invalidFirstName = request.query.get("invalidFirstName", False)
  invalidLastName = request.query.get("invalidLastName", False)  
  invalidUsername = request.query.get("invalidUsername", False) 
  success = request.query.get("success")
  return template("templates/admin/addStudent",
                  invalidFirstName=invalidFirstName,
                  invalidLastName=invalidLastName,
                  invalidUsername=invalidUsername,
                  success=success,
                  time=int(time()))

@adminApp.post("/addStudentValidation")
def validateStudent():
  userData = pd.read_csv("data/userData.csv")

  # Get all the variables from the form input fields  
  firstName = request.forms.get("firstName").strip()  
  lastName = request.forms.get("lastName").strip()  
  username = request.forms.get("username").strip()  
  password = request.forms.get("password").strip()

   
  # Validate the input fields  
  firstNameValidation = isValid(firstName)  
  lastNameValidation = isValid(lastName)  
  usernameValidation = usernameExists(userData, username)  
  

  # Check if any of the fields are invalid  
  if not firstNameValidation or not lastNameValidation or usernameValidation:  
    return redirect(f"/admin/addStudent?invalidFirstName={not firstNameValidation}&invalidLastName={ not lastNameValidation}&invalidUsername={usernameValidation}")  
  else:  
    # Create a new instructor DataFrame  
    newUser = pd.DataFrame({  
      "First Name": [firstName],  
      "Last Name": [lastName],  
      "Username": [username],
      "Password": [password],
      "Role": ["student"],
      "ID": [len(userData)+1]
    }) 
    

      # Concatenate the new instructor with the existing instructor data  
    userData = pd.concat([userData, newUser])  

    # Save the updated instructor data to the CSV file  
    userData.to_csv("data/userData.csv", index=False)

    return redirect("/admin/addStudent?success=True")







#--------Adding and validationg instructors--------
@adminApp.route("/addInstructor")
@requiresLogin
def addInstructor():
    firstNameValidation = request.query.get("invalidFirstName", " ")
    lastNameValidation = request.query.get("invalidLastName", " ")
    usernameValidation = request.query.get("invalidUsername", " ")
    success = request.query.get("success", "")  
    
    return template("templates/admin/addInstructor",
                    invalidFirstName=firstNameValidation,
                    invalidLastName=lastNameValidation,
                    invalidUsername=usernameValidation,
                    success=success,
                    time=int(time()))


#validation logic for the forms from the addInstructor Route
@adminApp.post("/addInstructorValidation")  
def instructorValidation():  
  userData = pd.read_csv("data/userData.csv")

  if os.path.exists("data/instructorData.csv"):
    instructorData = pd.read_csv("data/instructorData.csv", dtype=str)
  else:
    instructorData = pd.DataFrame(columns=["ID", "Position"])

  # Get all the variables from the form input fields  
  firstName = request.forms.get("firstName").strip()  
  lastName = request.forms.get("lastName").strip()  
  username = request.forms.get("username").strip()  
  password = request.forms.get("password").strip()
  position = request.forms.get("position")


  # Validate the input fields  
  firstNameValidation = isValid(firstName)  
  lastNameValidation = isValid(lastName)  
  usernameValidation = usernameExists(userData, username)  
  

  # Check if any of the fields are invalid  
  if not firstNameValidation or not lastNameValidation or usernameValidation:  
    return redirect(f"/admin/addInstructor?invalidFirstName={not firstNameValidation}&invalidLastName={ not lastNameValidation}&invalidUsername={usernameValidation}")  
  else:  
    # Create a new instructor DataFrame  
    newUser = pd.DataFrame({  
      "First Name": [firstName],
      "Last Name": [lastName],
      "Username": [username],
      "Password": [password],
      "Role": ["instructor"],
      "ID": [len(userData)+1]
    }) 
    
    newInstructor = pd.DataFrame({
      "ID": [len(userData)+1],
      "Position": [position]
    })

    # Concatenate the new instructor with the existing instructor data and user data 
    userData = pd.concat([userData, newUser], ignore_index=True)
    instructorData = pd.concat([instructorData, newInstructor], ignore_index=True)  

    # Save the updated instructor data to the CSV file   
    userData.to_csv("data/userData.csv", index=False)
    instructorData.to_csv("data/instructorData.csv", index=False) 

    return redirect("/admin/addInstructor?success=True")








#--------Adding and validating courses--------
@adminApp.route("/addCourse")
@requiresLogin
def addCourse():
  if os.path.exists("data/instructorData.csv"):
      instructorsExist = True
      instructorData = pd.read_csv("data/instructorData.csv")
      userData = pd.read_csv("data/userData.csv")
      mergedInstructorDict = pd.merge(userData,instructorData, on="ID")
      mergedProfessorDict = mergedInstructorDict[mergedInstructorDict["Position"] == "professor"].to_dict("records")
      mergedAssistantDict = mergedInstructorDict[mergedInstructorDict["Position"] == "assistant"].to_dict("records")
      
  else:
      instructorsExist = False
      instructorData = None
      mergedInstructorDict = []
      mergedProfessorDict = []
      mergedAssistantDict = []
      
  success = request.query.get("success")
  numberAlreadyExists = request.query.get("numberAlreadyExists", False)
  titleAlreadyExists = request.query.get("titleAlreadyExists", False)

  return template("templates/admin/addCourse", 
                  instructorsExist=instructorsExist,
                  instructorDict=mergedProfessorDict,
                  assistantDict=mergedAssistantDict,
                  numberAlreadyExists=numberAlreadyExists,
                  titleAlreadyExists=titleAlreadyExists,
                  success=success,
                  time=int(time()))


#Handling the Post method for the admin course validation. This is the validation for the addCourse Route
@adminApp.post("/addCourseValidation")
def courseValidation():
  if os.path.exists("data/courseData.csv"):
      courseData = pd.read_csv("data/courseData.csv", dtype=str)
  else:
      courseData = pd.DataFrame(columns=["Title", "CourseID", "InstructorID", "AssistantID", "StudentIDs"])


  #get the course's title, id, and instructor ID from the template
  title = request.forms.get("title").strip()
  courseID = request.forms.get("courseID")
  instructorID = request.forms.get("instructorID")
  assistantID = request.forms.get("assistantID")
  
  if not assistantID:
    assistantID = ""

  #validation for the course number and title
  validNumber = isUnique(courseData, courseID, "CourseID")
  validTitle = isUnique(courseData, title, "Title")

  #if invlaid, return an query to tell the website to enter an error message
  if validTitle == False or validNumber == False:
    return redirect(f"/admin/addCourse?numberAlreadyExists={not validNumber}&titleAlreadyExists={not validTitle}&success=False")
    

  newCourse = pd.DataFrame({
  "Title": [title],
  "CourseID": [courseID],
  "InstructorID": [instructorID],
  "AssistantID" : [assistantID],
  "StudentIDs": [""]
  })

  courseData = pd.concat([courseData, newCourse])
  courseData.to_csv("data/courseData.csv", index=False)
  return redirect("/admin/addCourse?success=True")








#--------Show All Courses Route--------    
@adminApp.route("/showAllCourses")
@requiresLogin
def showAllCourses():
  if os.path.exists("data/courseData.csv"):
    coursesExist = True
    userData = pd.read_csv("data/userData.csv")
    courseData = pd.read_csv("data/courseData.csv")
    courseInstructorDict = pd.merge(userData, courseData, left_on="ID", right_on="InstructorID")
    courseDict = pd.merge(courseInstructorDict, userData, left_on="AssistantID", right_on="ID",how="left").fillna({"First Name_y": "N/A", "Last Name_y": ""})
    courseDict.drop(["InstructorID", "AssistantID", "Username_x", "Username_y", "Password_x", "Password_y", "Role_x", "Role_y", "ID_x", "ID_y"], axis=1, inplace=True)
    courseDict = courseDict.to_dict("records")
    

    print(courseDict)
    
  else:
    coursesExist = False
    courseDict = []
      
  return template("templates/admin/showAllCourses",coursesExist=coursesExist, courseDict=courseDict, time=int(time()))








#--------Show All Instructors Route--------
@adminApp.route("/showAllInstructors")
@requiresLogin
def showAllInstructors():
  if os.path.exists("data/instructorData.csv"):
    instructorsExist = True
    userData = pd.read_csv("data/userData.csv")
    instructorData = pd.read_csv("data/instructorData.csv")
    instructorDict = pd.merge(userData, instructorData, on="ID").to_dict("records")
    print(instructorDict)
    
  else:
    instructorsExist = False
    instructorDict = []
      
  return template("templates/admin/showAllInstructors",
                  instructorsExist=instructorsExist,
                  instructorDict=instructorDict,
                  time=int(time()))







#--------Show All Students Route--------
@adminApp.route("/showAllStudents")
@requiresLogin
def showAllStudents():
  if os.path.exists("data/userData.csv"):
    userData = pd.read_csv("data/userData.csv")
    studentData = userData[userData["Role"] == "student"].to_dict("records")
  else:
    studentData = {}
  
  return template("templates/admin/showAllStudents", studentDict=studentData, time=int(time()))
  