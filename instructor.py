from bottle import Bottle, run, template, redirect, request  
from middleware import *
import pandas as pd 
import os


#start the adminApp
instructorApp = Bottle()  

#import the universal cookies
sessionMiddleware = createSessionMiddleware(instructorApp)

#--------Instructor Dashboard--------
@instructorApp.route('/')  
@requiresLogin
def instructor():  
   session = request.environ.get('beaker.session')   
   firstName = session.get("firstName") 
   position = session.get("position")

   return template("templates/instructor/instructor", firstName=firstName, position=position)







#--------View Assigned Courses Route--------
@instructorApp.route("/viewAssignedCourses")
def viewAssignedCourses():
    courseData = pd.read_csv("data/courseData.csv")
    session = request.environ.get("beaker.session")
    username = session.get("username")

    hasCourses = courseData["Instructor"].isin([username]).any()

    if hasCourses:
      assignedCourseDict = courseData[courseData["Instructor"] == username]
      assignedCourseDict = assignedCourseDict.to_dict("records")
    else:
      assignedCourseDict = []

    return template("templates/instructor/viewAssignedCourses", assignedCourseDict=assignedCourseDict, hasCourses=hasCourses, username=username)
