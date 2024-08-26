from flask import Flask

def initialize_app():
  app = Flask(__name__)
  from .auth import auth as authBlueprint
  app.register_blueprint(authBlueprint, url_prefix="/auth") 
  return app

