from flask import Flask
from dotenv import load_dotenv

def initialize_app():
  app = Flask(__name__)
  load_dotenv()
  
  from .auth import auth_routes 
  app.register_blueprint(auth_routes, url_prefix="/api/auth")
  
  from .user import user_routes
  app.register_blueprint(user_routes, url_prefix="/api/user")

  from .attendace import attendance_routes
  app.register_blueprint(attendance_routes,url_prefix= "/api/attendance")
  
  return app

