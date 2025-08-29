import sys

from app import app
import os

from app.config.db_init import initialize_database

# python run.py --with-init-db
# si j'ai le paramètre --with-init-db dans la ligne de commande
if "--with-init-db" in sys.argv:
    with app.app_context():
        initialize_database()

# je récupère le port depuis l'environment
# par défaut sa valeur sera 5000 (si la variable n'existe pas dans le .env)
port = int(os.environ.get('PORT', 5000))
app.run('0.0.0.0', port=port)

