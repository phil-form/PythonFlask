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

Les controlleurs vont habituellement avoir au minimum les routes suivantes : 

GET ALL /nom_de_l_entite : récupère toutes les entités du type en DB

```python
@app.get('/users')
def get_users():
    user_service = UserService()
    return jsonify([u.serialize() for u in user_service.find_all()])
```

GET /nom_entitee/ID => récupère une entité par son ID

```python
@app.get('/users/<int:userid>')
def get_user(userid: int):
    user_service = UserService()
    user = user_service.find_one(userid)
    return jsonify(user.serialize()) if user else ('', 404)
```

POST /nom_entite => ajoute une nouvelle entité en DB

```python
@app.post('/users')
def post_user():
    user_service = UserService()
    form = UserRegisterForm.from_json(request.json)
    
    if form.validate():
        user = user_service.insert(form)
        
        return jsonify(user.serialize())
    
    return jsonify(form.errors)
```

PUT /nom_entite/ID => permet de modifier une entité en DB

```python
@app.put('/users/<int:userid>')
def put_user(userid: int):
    user_service = UserService()
    form = UserUpdateForm.from_json(request.json)
    
    if form.validate():
        user = user_service.update(userid, form)

        return jsonify(user.serialize())
    
    return jsonify(form.errors)
```

DELETE /nom_entite/ID : Servira pour supprimer une entité par ID

```python
@app.delete('/users/<int:userid>')
def delete_user(userid: int):
    user_service = UserService()
    user = user_service.find_one(userid)
    if user:
        user_service.delete(user)
        return ('', 204)
    return ('', 404)
```

### Codes de retour de l’API

L’API renvoie un code standard dans chaque réponse pour indiquer l’état du traitement :

| Code | Signification                | Description                                                                 |
|------|------------------------------|-----------------------------------------------------------------------------|
| 200  | OK                           | La requête a été traitée avec succès.                                       |
| 201  | Created                      | Une nouvelle ressource a été créée.                                         |
| 400  | Bad Request                  | La requête est invalide ou contient des paramètres incorrects.              |
| 401  | Unauthorized                 | Authentification requise ou jeton invalide.                                 |
| 403  | Forbidden                    | L’accès à la ressource demandée est refusé.                                |
| 404  | Not Found                    | La ressource demandée n’existe pas.                                         |
| 409  | Conflict                     | Conflit avec l’état actuel de la ressource (ex. doublon).                   |
| 422  | Unprocessable Entity         | Données valides mais impossibles à traiter.                                 |
| 500  | Internal Server Error        | Une erreur interne est survenue sur le serveur.                             |
| 503  | Service Unavailable          | Le service est temporairement indisponible (ex. maintenance).               |


## models

Les modès sont créé via SQLAlchemy et les migrations sont gérée par Alembic

Après avoir modifier ou créé une entité il faut absolument générer une migration et l'exécuter!

### 1) Créer la classe de Base

=> Fichier Models/Base.py

Ici on doit créer une classe de base pour nos entités, qui nous servira pour créer
de nouvelles classes dérivée qui pourront être liées à une DB.

```python
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass
```

### 2) Créer vos entités : 

=> Fichiers Models/user.py Models/Basket.py

Ici on va déclarer des variables static qui vont définir les différents parametres 
de notre table : 

__tablename__ => nom de la table

pour les champs : 
nomDuChamp: Mapped[TYPE] = mapped_column(?contraintes?)

id: Mapped[int] = mapped_column(primary_key=True)

Crée un champ username d'une longueur max de 50 et avec le flag unique

username: Mapped[String] = mapped_column(String(50), unique=True)
```python
from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column
from Models.Base import Base

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column()
```

### 3) créer l'engine et manipuler nos entités 

=> Fichier engine.py

Dans celui-ci je vais devoir créer l'engine de la DB via la fonction create_engine, 
attention que la DB doit être créée au préalable

```python
from sqlalchemy import create_engine

# url = connection string
# echo = afficher les informations de transaction avec la DB dans le terminal
engine = create_engine(url='sqlite:///myfile.db', echo=True)
```
Créer les tables 
```python
from Models.Base import Base

Base.metadata.create_all(engine)
```
Drop les tables
```python
from Models.Base import Base

Base.metadata.drop_all(engine)
```

### One to many
```python
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
    
    # On définit la clé étrangère !! users.id = nom_de_la_table.nom_colonne
    user_id = Column(Integer, ForeignKey('users.id'))
    # Optionel On défini la relation des objets entre eux
    # Ici je dis que l'objet BasketItem contient une relation qui cible l'objet User
    # le back_population est optionel
    # !! Le back_population est le nom du champ dans l'objet !!
    # Pour la relationship, je passe le nom de l'objet sous forme de string,
    # pour éviter les boucles d'import example : 
    #   Le fichier user.py qui import la classe BasketItem de basket_item.py
    #   et le fichier basket_item.py qui importe la classe User de user.py
    user = relationship('User', back_populates='basket_items')
```
```python
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user = relationship('User', back_populates='basket_items')
```

Du coté de l'entité ciblée :
```python
# l'option cascade va me permettre de dire comment et quels opération faire en cascade 
#   - all => toutes les opération, insert, update, delete
#   - save-update => on cascade les insert et update
#   - delete => uniquement cascade les delete
#   - delete-orphan => supprime les éléments qui ne sont plus lié à un parent automatiquement.
basket_items = relationship('BasketItem', back_populates='user', cascade='all, delete-orphan')
```

### Many to many
Créer une table d'association
```python
from sqlalchemy import Table, Integer, Column, ForeignKey
from Models.Base import Base

user_roles = Table('user_roles', Base.metadata,
                   Column('user_id', Integer, ForeignKey('users.id')),
                   Column('role_id', Integer, ForeignKey('roles.id'))
                   )
```

Faire les relations dans les entités respectives.

Dans l'entité User
```python
    roles = relationship('Role', back_populates='users', secondary='user_roles')
```

Dans l'entité Role
```python
    users = relationship('User', back_populates='roles', secondary='user_roles')
```
#### Si j'ai des informations supplémentaires dans ma relation

Dans ce cas ci il faut faire une entité supplémentaires, stockant les données
```python
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from Models.Base import Base


class BasketItem(Base):
    __tablename__ = 'basketitems'

    id = Column(Integer, primary_key=True)
    quantity = Column(Integer, nullable=False)

    item_id = Column(Integer, ForeignKey('items.id'))
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship('User', back_populates='basket_items')
    item = relationship('Item', back_populates='basket_items')
```

### SQLALCHEMY/Alembic

Utilisation de SqlAlchemy pour les select : 
```python
# 1. Récupérer tous les enregistrements
    users = User.query.all()
    print("Tous les utilisateurs:", users)

    # 2. Filtrer (WHERE)
    alice = User.query.filter_by(username="alice").first()
    print("Utilisateur Alice:", alice)

    # 3. Filtre plus complexe
    emails = User.query.filter(User.email.like("%@example.com")).all()
    print("Tous les emails @example.com:", emails)

    # 4. ORDER BY
    ordered_users = User.query.order_by(User.username.desc()).all()
    print("Utilisateurs triés:", ordered_users)

    # 5. LIMIT
    first_two = User.query.limit(2).all()
    print("Deux premiers:", first_two)

    # 6. OFFSET + LIMIT (Pagination)
    second_page = User.query.offset(2).limit(2).all()
    print("Page 2:", second_page)

    # 7. COUNT
    count = User.query.count()
    print("Nombre total d’utilisateurs:", count)

    # 8. Projection (sélection de colonnes spécifiques)
    usernames = db.session.query(User.username).all()
    print("Liste des usernames:", usernames)

    # 9. Filtre In
    users = User.query.filter(User.username.in_(['alice', 'test'])).all()
    print("Liste des utilisateurs:", emails)
```

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
```python
class UserService:
    def find_all(self):
        # User.query.all() -> permet de récupérer toutes les données en DB
        return [UserDTO(u) for u in User.query.all()]

    def find_one(self, id):
        # User.query.filter_by(champ_de_l_objet=valeur) -> permet de récupérer les entités
        # respectant une certaine valeur de champ
        # le .first() permet de récupérer seulement le première élément
        user = User.query.filter_by(userid=id).first()
        return UserDTO(user) if user else None

    def insert(self, form: UserRegisterForm):
        user = User(
            username=form.username.data,
            password=form.password.data
        )
        # db.session.add(entité) -> permet d'ajouter une entité en DB via la transaction en cours
        db.session.add(user)
        # db.session.commit() -> confirme les modification et applique la transaction en DB
        db.session.commit()
        return UserDTO(user)

    def update(self, id, form: UserUpdateForm):
        user = User.query.filter_by(userid=id).first()
        
        user.lastname = form.lastname.data
        user.firstname = form.firstname.data

        if form.password.data:
            user.password = form.password.data

        # db.session.commit() -> confirme les modification et applique la transaction en DB
        db.session.commit()
        return UserDTO(user)

    def delete(self, user: User):
        # db.session -> créé une transaction
        # db.session.delete(entité) -> supprimera l'entité
        db.session.delete(user)
        # db.session.commit() -> confirme les modification et applique la transaction en DB
        db.session.commit()
        return UserDTO(user)
```