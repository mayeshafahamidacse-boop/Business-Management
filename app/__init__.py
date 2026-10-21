from flask import Flask
from pathlib import Path
import os
from .db import init_app

def create_app(test_config=None):
 app=Flask(__name__,instance_relative_config=True)
 app.config.from_mapping(SECRET_KEY=os.environ.get('BOUTIQUE_SECRET','local-development-key-change-me'),DATA_DIR=str(Path(app.instance_path)/'data'),MAX_CONTENT_LENGTH=5*1024*1024)
 if test_config: app.config.update(test_config)
 Path(app.instance_path).mkdir(parents=True,exist_ok=True)
 for d in ('product_images','backups'): Path(app.config['DATA_DIR'],d).mkdir(parents=True,exist_ok=True)
 init_app(app)
 from .routes import bp
 app.register_blueprint(bp)
 return app
