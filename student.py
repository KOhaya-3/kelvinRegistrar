from bottle import Bottle, template, request  
from middleware import *
import pandas as pd 
from time import time
import os

#start the studentApp
studentApp = Bottle()  

#---------Student Dashboard Route--------
@studentApp.route("/")
@requiresLogin
def student():
    session = request.environ.get("beaker.session")
    firstName = session.get("firstName")
    return template("templates/student/student", firstName=firstName, time=int(time()))







#--------View erolled courses route--------
@studentApp.route("/viewEnrolledCourses")
@requiresLogin
def viewEnrolledCourses():
    session = request.environ.get("beaker.session")
    iD = session.get("ID")

    if os.path.exists("data/courseData.csv"):
        courseData = pd.read_csv("data/courseData.csv", dtype=str).fillna("")
        filteredCourses = courseData[courseData["StudentIDs"].str.contains(f"{iD}")].to_dict("records")
         
    else:
        filteredCourses = {}
    

    return template("templates/student/viewEnrolledCourses", enrolledCourseDict=filteredCourses,time=int(time()))







#--------Enroll In A Course Route and Post--------
@studentApp.route("/enrollInACourse")
@requiresLogin
def enrollInACourse():
    coursesExist = os.path.exists("data/courseData.csv")
    session = request.environ.get("beaker.session")
    success = request.query.get("success")
    iD = session.get("ID")

    if coursesExist:
        userData = pd.read_csv("data/userData.csv", dtype=str)
        courseData = pd.read_csv("data/courseData.csv", dtype=str).fillna("")
        courseData =  courseData[~courseData['StudentIDs'].str.contains(f"{iD}")]
        courseInstructorDict = pd.merge(userData, courseData, left_on="ID", right_on="InstructorID")
        courseDict = pd.merge(courseInstructorDict, userData, left_on="AssistantID", right_on="ID",how="left").fillna({"First Name_y": "N/A", "Last Name_y": ""})
        courseDict.drop(["InstructorID", "AssistantID", "Username_x", "Username_y", "Password_x", "Password_y", "Role_x", "Role_y", "ID_x", "ID_y"], axis=1, inplace=True)
        courseDict = courseDict.to_dict("records")
       
    else: courseData = {}


    return template("templates/student/enrollInACourse", enrollmentDict=courseDict, time=int(time()), success=success)


@studentApp.post("/enrollInACourseProcessor")
def processCourseEnrollment():
    courseData = pd.read_csv("data/courseData.csv", dtype=str).fillna("")
    desiredCourses = {}
    session = request.environ.get("beaker.session")
    iD = session.get("ID")
    selectedCourseIDs = request.forms.getlist("enrollmentList[]")

    for courseID in selectedCourseIDs:
        desiredCourses = courseData.loc[courseData["CourseID"] == str(courseID), "StudentIDs"].values[0]
        listOfEnrolledStudents = desiredCourses.split(';') if desiredCourses != "" else list(desiredCourses)
        listOfEnrolledStudents.append(str(iD))  
        enrolledStudentStr = (";".join(listOfEnrolledStudents))
        print (enrolledStudentStr)
        courseData.loc[courseData["CourseID"] == courseID, "StudentIDs"] = enrolledStudentStr
    courseData.to_csv("data/courseData.csv", index=False)

    return redirect("/student/enrollInACourse?success=True")


