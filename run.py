from app import app
import os

# je récupère le port depuis l'environment
# par défaut sa valeur sera 5000 (si la variable n'existe pas dans le .env)
port = int(os.environ.get('PORT', 5000))
app.run('0.0.0.0', port=port)

