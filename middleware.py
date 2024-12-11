from bottle import request, redirect
from beaker.middleware import SessionMiddleware


sessionOpts = {  
   'session.type': 'file',  
   'session.data_dir': './session_data',  
   'session.auto': True,  
} 


def requiresLogin(func):  
   def wrapper(*args, **kwargs):  
      session = request.environ.get('beaker.session')  
      if 'authenticated' not in session or not session:  
        return redirect('/')  
      return func(*args, **kwargs)  
   return wrapper

def createSessionMiddleware(app):
   return SessionMiddleware(app, sessionOpts)