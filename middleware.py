from bottle import request, redirect
from beaker.middleware import SessionMiddleware


sessionOpts = {  
   'session.type': 'file',  
   'session.data_dir': './session_data',  
   'session.auto': True,  
} 


def requiresLogin(func):  
   def wrapper(*args, **kwargs):  
      session = request.environ['beaker.session']  
      if 'authenticated' not in session or not session['authenticated']:  
        return redirect('/adminLogin')  
      return func(*args, **kwargs)  
   return wrapper

def createSessionMiddleware(app):
   return SessionMiddleware(app, sessionOpts)