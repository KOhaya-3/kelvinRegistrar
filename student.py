from bottle import Bottle, template, request  
from middleware import *
import pandas as pd 
import os

#start the studentApp
studentApp = Bottle()  

#import the universal cookies
sessionMiddleware = createSessionMiddleware(studentApp)


#---------Student Dashboard Route--------
@studentApp.route("/")
def student():
    session = request.environ.get("beaker.session")
    firstName = session.get("firstName")
    return template("templates/student/student", firstName=firstName)







#--------View erolled courses route--------
@studentApp.route("/viewEnrolledCourses")
def viewEnrolledCourses():
    session = request.environ.get("beaker.session")
    username = session.get("username")

    enrollmentData = pd.read_csv("data/enrollment.csv", dtype=str)
    enrollmentData = enrollmentData.fillna("")


    filteredCourses = enrollmentData[enrollmentData["Student Usernames"].str.contains(rf"\b{username}\b")]

    hasCourses = len(filteredCourses) > 0

    if hasCourses:
        enrolledCourseDict = filteredCourses.to_dict("records")
    else:
        enrolledCourseDict = []
    

    return template("templates/student/viewEnrolledCourses", hasCourses=hasCourses, enrolledCourseDict=enrolledCourseDict)







#--------Enroll In A Course Route and Post--------
@studentApp.route("/enrollInACourse")
def enrollInACourse():
    coursesExist = os.path.exists("data/enrollment.csv")
    session = request.environ.get("beaker.session")
    username = session.get("username")

    if coursesExist:
        enrollmentDict = pd.read_csv("data/enrollment.csv", dtype=str)
        enrollmentDict = enrollmentDict.fillna("")

        # Split the column values by the separator (e.g., ':')
        enrollmentDict['Student Usernames'].apply(lambda x: x.split(';')).apply(lambda lst: username not in lst)
        filteredData = enrollmentDict[enrollmentDict['Student Usernames'].apply(lambda x: username not in x.split(';'))].to_dict("records")


    else: filteredData = []


    return template("templates/student/enrollInACourse", coursesExist=coursesExist, enrollmentDict=filteredData)


@studentApp.post("/enrollInACourseProcessor")
def processCourseEnrollment():
    enrollmentData = pd.read_csv("data/enrollment.csv", dtype=str)
    enrollmentData = enrollmentData.fillna("")
    session = request.environ.get("beaker.session")
    firstName = session.get("firstName")
    lastName = session.get("lastName")
    username = session.get("username")
    
    requestedClasses = request.forms.getlist("enrollmentList[]")

    for course in requestedClasses:
        # Update Student First Names column
        currentFirstNames = enrollmentData.loc[enrollmentData["Number"] == course, "Student First Names"].values[0]

        if currentFirstNames == "":
            updatedFirstNames = firstName
        else:
            updatedFirstNames = f"{currentFirstNames};{firstName}"

        enrollmentData.loc[enrollmentData["Number"] == course, "Student First Names"] = updatedFirstNames



        # Update Student Last Names column
        currentLastNames = enrollmentData.loc[enrollmentData["Number"] == course, "Student Last Names"].values[0]

        if currentLastNames == "":
            updatedLastNames = lastName
        else:
            updatedLastNames = f"{currentLastNames};{lastName}"

        enrollmentData.loc[enrollmentData["Number"] == course, "Student Last Names"] = updatedLastNames
        

        # Update Student Usernames column
        currentUsernames = enrollmentData.loc[enrollmentData["Number"] == course, "Student Usernames"].values[0]

        if currentUsernames == "":
            updatedUsernames = username
        else:
            updatedUsernames = f"{currentUsernames};{username}"
        
        enrollmentData.loc[enrollmentData["Number"] == course, "Student Usernames"] = updatedUsernames

# Save the updated dataframe back to the CSV
    enrollmentData.to_csv("data/enrollment.csv", index=False)

    return template(f"""
<p>All courses have been enrolled!</p>
<a href="/student">Back to dashboard</a>
""")


