from flask import Flask
from dotenv import load_dotenv
from flasgger import Swagger


def initialize_app():
  load_dotenv()
  app = Flask(__name__)
  
  swagger = Swagger(app, template={
		"info": {
			"title": "Caritas API",
			"description": "REST API para Caritas de Monterrey",
			"version": "1.0.1"
			}
  })
  
  from .auth import auth_routes 
  app.register_blueprint(auth_routes, url_prefix="/api/auth")
  
  from .user import user_routes
  app.register_blueprint(user_routes, url_prefix="/api/user")
  
  
  return app

