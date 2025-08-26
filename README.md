# FLASK

# SQLALCHEMY
initialiser la DB
```bash
flask db init
```

générer une migration
```bash
flask db revision --autogenerate -m "nom de la migration"
```

Mettre à jour la DB 
```bash
flask db upgrade
```