import os

import sys
import wtforms_json
from pathlib import Path
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv

# Charger le fichier .env
load_dotenv()

# je crée le path pour le .env.local (configuration locale du serveur)
envlocal = Path().cwd() / '.env.local'

# je regarde si il existe
if os.path.exists(envlocal):
    # si le fichier .env.local existe je le charge en plus dans l'envoironement de mon application
    load_dotenv(dotenv_path=envlocal)

app = Flask("app")
app.debug = os.environ.get('DEBUG', False)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

wtforms_json.init()

# initialise ma DB, il va récupérer la chaine de connection
# dans app.config
db = SQLAlchemy(app)
# Permet la gestion des migrations via Alembic
migrate = Migrate(app, db)

from app.models import *
from app.controllers import *

from app.config.injector_config import config_injector
from app.framework.injector import Injector

injector = Injector(app, config_func=config_injector)

from app.config.db_init import initialize_database