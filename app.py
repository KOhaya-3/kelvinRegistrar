from bottle import Bottle, run, template, redirect, request, static_file
from admin import adminApp
from instructor import instructorApp
from student import studentApp
from middleware import *
import pandas as pd 
from time import time
from bottle import template



app = Bottle()  


# Create a BeakerMiddleware instance  
middlewareApp = createSessionMiddleware(app) 


#--------Handling static pages (stylesheets)--------
@app.route("/static/<filename:path>")
def serve_static(filename):
   response = static_file(filename, root='./static')
   response.set_header('Cache-Control', 'no-cache, no-store, must-revalidate')
   response.set_header('Pragma', 'no-cache')
   response.set_header('Expires', '0')
   return static_file(filename, root="./static")





#--------Home Login Page Route and Validation Handling-------- 
@app.route('/')  
def index(): 
   session = request.environ.get("beaker.session") 
   session.delete()
   invalidCredentials = request.query.get("invalidCredentials")  
   return template("templates/login", invalidCredentials = invalidCredentials, attempts = 5, time=int(time()))



@app.post("/loginValidation")  
def validateUser():  
   userData = pd.read_csv("data/userData.csv")
   
   session = request.environ.get('beaker.session')
   username = request.forms.get("username")  
   password = request.forms.get("password")  

   match = userData[(userData["Username"] == username) & (userData["Password"] == password)]
   
   if match.empty:   
         return redirect(f"/?invalidCredentials=True")  

   role = match["Role"].values[0] 
   session['authenticated'] = True  
   session["firstName"] = match["First Name"].values[0] 
   session["ID"] = match["ID"].values[0]
   session.save()
   
   if role  == "admin":
      return redirect("/admin")  
   elif role  == "student":
      return redirect("/student")
   elif role  == "instructor":
      return redirect("/instructor")

@app.post("/returnHome")
def returnHome():
   return redirect("/")



#mount the admin, instructor, and student Apps here
app.mount("/admin",adminApp)
app.mount("/instructor", instructorApp)
app.mount("/student", studentApp)



# Run the Bottle server
application = middlewareApp

if __name__ == "__main__":
   run(middlewareApp, host='localhost', port=8080, reloader=True, debug=True)