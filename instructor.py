from bottle import Bottle, run, template, redirect, request  
from middleware import *
import pandas as pd 
from time import time
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

   return template("templates/instructor/instructor", firstName=firstName, position=position, time=int(time()))







#--------View Assigned Courses Route--------
@instructorApp.route("/viewAssignedCourses")
@requiresLogin
def viewAssignedCourses():   
  session = request.environ.get("beaker.session")
  iD = session.get("ID")

  if os.path.exists("data/courseData.csv"):
    courseData = pd.read_csv("data/courseData.csv")
    assignedCourseDict = courseData.loc[(courseData["InstructorID"] == iD) | (courseData["AssistantID"] == iD)].to_dict("records")

  else:
    assignedCourseDict = {}
    


  return template("templates/instructor/viewAssignedCourses", assignedCourseDict=assignedCourseDict, time=int(time()))
