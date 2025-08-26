# FLASK

## controllers

## models

## mappers

## services

```
- des fonctions pour contacter la db : 
    - findOne => retourne une entité en fonction de son id
    - findOneBy => retourne une entité en fonction d'un 
        paramètre passé (données d'une des colonnes)
    - findAll => retourne toutes les data
    - update => met à jours les donnés en DB
    - insert => insert des nouvelles donnée en DB
    - delete => delete une entrée en DB
```

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