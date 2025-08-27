# FLASK

## Méthodologie
```
On part des modèles
Ensuite on fait les DTO et les Forms
Après on fait les services avec leur fonctions
Et en dernier le controller

!!! En cas de modification du modèle !!!
Toujours faire une migration 
-> flask db migrate -m "message"
-> flask db upgrade
```

## FROM DTO MODELE
### Modèles

Les modèles sont uniquement utilisé pour communiqué avec la DB et modifier les informations de la DB.

### FORMS

Vont récupérer les données envoyées par l'utilisateur au travers des body de la requête. Et les forms vont aussi faire la validation de ces données, donc vérifier que les contraintes d'intégrité sont bien respectées.

### DTOS

Les DTOs sont les objets qui contiendront les données envoyée à l'utilisateur. Ceux-ci peuvent être utilisé entre autre pour filtrer des données ne devant pas être renvoyée (example le password de l'utilisateur). Ils peuvent contenir des données supplémentaires (example le nom complèt d'une personne)

## controllers

```python
@app.get('/users')
def get_users():
    user_service = UserService()
    return jsonify([u.serialize() for u in user_service.find_all()])

@app.post('/users')
def post_user():
    user_service = UserService()
    form = UserRegisterForm.from_json(request.json)
    
    if form.validate():
        user = user_service.insert(form)
        
        return jsonify(user.serialize())
    
    return jsonify(form.errors)
```

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
flask db migrate -m "nom de la migration"

OU 

flask db revision --autogenerate -m "nom de la migration"
```

Mettre à jour la DB 
```bash
flask db upgrade
```