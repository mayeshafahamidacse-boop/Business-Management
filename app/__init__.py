from flask import Flask
from pathlib import Path
import os
import hmac
from flask import Response, request
from .db import init_app

def create_app(test_config=None):
 app=Flask(__name__,instance_relative_config=True)
 app.config.from_mapping(SECRET_KEY=os.environ.get('BOUTIQUE_SECRET','local-development-key-change-me'),DATA_DIR=os.environ.get('DATA_DIR',str(Path(app.instance_path)/'data')),MAX_CONTENT_LENGTH=5*1024*1024)
 if test_config: app.config.update(test_config)
 username=os.environ.get('APP_USERNAME')
 password=os.environ.get('APP_PASSWORD')
 if os.environ.get('APP_AUTH_REQUIRED') == 'true' and (not username or not password):
  raise RuntimeError('APP_USERNAME and APP_PASSWORD must be configured when APP_AUTH_REQUIRED is true')
 if username and password:
  @app.before_request
  def require_app_login():
   auth=request.authorization
   if auth and hmac.compare_digest(auth.username or '',username) and hmac.compare_digest(auth.password or '',password):
    return None
   return Response('Sign in required',401,{'WWW-Authenticate':'Basic realm="Pinteresty Outfits Business Desk"'})
 Path(app.instance_path).mkdir(parents=True,exist_ok=True)
 for d in ('product_images','backups'): Path(app.config['DATA_DIR'],d).mkdir(parents=True,exist_ok=True)
 init_app(app)
 from .routes import bp
 app.register_blueprint(bp)
 return app
