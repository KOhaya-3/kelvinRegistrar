from bottle import Bottle, run, template, redirect, request  
from admin import adminApp
from instructor import instructorApp
from student import studentApp
from middleware import *
import pandas as pd 
import os


app = Bottle()  


# Create a BeakerMiddleware instance  
middleWare_app = createSessionMiddleware(app) 


  
#--------Home Page Route-------- 
@app.route('/')  
def index():  
   session = request.environ["beaker.session"]
   if 'authenticated' in session:  
      session.delete()  
      session.save()  
   return template("templates/index")  








#--------Admin Login Route and Post Validation Handling--------
@app.route('/adminLogin')  
def admins():  
   session = request.environ.get('beaker.session')  
   attempts = session.get('attempts', 5)  # default value is 5  
   invalidCredentials = request.query.invalidCredentials == "True"   
   return template("templates/admin/adminLogin", invalidCredentials=invalidCredentials, attempts=attempts)  


@app.post("/adminLoginValidation")  
def validateUser():  
   adminData = pd.read_csv("data/adminData.csv")
   
   session = request.environ.get('beaker.session')
   session['authenticated'] = False  
   username = request.forms.get("username")  
   password = request.forms.get("password")  

   match = adminData[(adminData["Username"] == username) & (adminData["Password"] == password)]
  
   attempts = session.get('attempts', 5)  
  
   if match.empty:  
      if attempts > 1:
         attempts -= 1  
         session['attempts'] = attempts  
         session.save()  
         return redirect(f"/adminLogin?invalidCredentials=True&loginError=*Invalid+Username+or+password.+Please+try+again.")  
      else:
         session.pop("attempts")
         return redirect("/")
    
   session['authenticated'] = True  
   session["firstName"] = match["First Name"].values[0] 
   session.save()  
   return redirect(f"/admin")  

  







#--------Instructor Login Route and Post Validation--------
@app.route("/instructorLogin")
def instructorLogin():

   instructorsExist = os.path.exists("data/instructorData.csv")

   session = request.environ.get('beaker.session')  
   attempts = session.get('attempts', 5)  # default value is 5  
   invalidCredentials = request.query.invalidCredentials == "True"

   return template("templates/instructor/instructorLogin", instructorsExist=instructorsExist, invalidCredentials=invalidCredentials,attempts=attempts)

@app.post("/instructorLoginValidation")
def validateInstructor():
   instructorData = pd.read_csv("data/instructorData.csv")


   session = request.environ.get('beaker.session')
   session['authenticated'] = False  
   username = request.forms.get("username")  
   password = request.forms.get("password")  

   
   match = instructorData[(instructorData["Username"] == username) & (instructorData["Password"] == password)]
  
   attempts = session.get('attempts', 5)  
  
   if match.empty:  
      if attempts > 1:
         attempts -= 1  
         session['attempts'] = attempts  
         session.save()  
         return redirect(f"/instructorLogin?invalidCredentials={True}")  
      else:
         session.pop("attempts")
         return redirect("/")
    
   session['authenticated'] = True  
   session["firstName"] = match["First Name"].values[0] 
   session["username"] = match["Username"].values[0]
   session["position"] = match["Position"].values[0]
   session.save()  
   return redirect(f"/instructor")








#--------Instructor Login Route and Post Validation--------
@app.route("/studentLogin")
def studentLogin():

   studentsExist = os.path.exists("data/studentData.csv")

   session = request.environ.get('beaker.session')  
   attempts = session.get('attempts', 5)  # default value is 5  
   invalidCredentials = request.query.invalidCredentials == "True"

   return template("templates/student/studentLogin", studentsExist=studentsExist, invalidCredentials=invalidCredentials,attempts=attempts)


@app.post("/studentLoginValidation")
def validateStudent():
   studentData = pd.read_csv("data/studentData.csv")


   session = request.environ.get('beaker.session')
   session['authenticated'] = False  
   username = request.forms.get("username")  
   password = request.forms.get("password")  

   
   match = studentData[(studentData["Username"] == username) & (studentData["Password"] == password)]
  
   attempts = session.get('attempts', 5)  
  
   if match.empty:  
      if attempts > 1:
         attempts -= 1  
         session['attempts'] = attempts  
         session.save()  
         return redirect(f"/studentLogin?invalidCredentials={True}")  
      else:
         session.pop("attempts")
         return redirect("/")
    
   session['authenticated'] = True  
   session["firstName"] = match["First Name"].values[0] 
   session["lastName"] = match["Last Name"].values[0]
   session["username"] = match["Username"].values[0]
   session.save()  
   return redirect("/student") 










#--------Handling for when the form action="returnHome" (if the user wants to go the main screen)--------
@app.post("/returnHome")  
def returnHome():  
   redirect("/") 




#mount the admin, instructor, and student Apps here
app.mount("/admin",adminApp)
app.mount("/instructor", instructorApp)
app.mount("/student", studentApp)

# Run the app  
run(middleWare_app, host='localhost', port=8080, debug=True, reloader=True)