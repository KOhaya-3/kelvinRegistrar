from bottle import Bottle, run, template, redirect, request  
from middleware import *
import pandas as pd 
import os


#start the adminApp
instructorApp = Bottle()  


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
@requiresLogin
def viewAssignedCourses():   
  session = request.environ.get("beaker.session")
  username = session.get("username")

  if os.path.exists("data/courseData.csv"):
    courseData = pd.read_csv("data/courseData.csv")
    hasCourses = courseData["Instructor"].isin([username]).any()

  else:
    hasCourses = False

  if hasCourses:
    assignedCourseDict = courseData[courseData["Instructor"] == username]
    assignedCourseDict = assignedCourseDict.to_dict("records")
  else:
    assignedCourseDict = []

  return template("templates/instructor/viewAssignedCourses", assignedCourseDict=assignedCourseDict, hasCourses=hasCourses, username=username)
