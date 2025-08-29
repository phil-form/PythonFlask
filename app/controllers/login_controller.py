from flask import request, jsonify

from app.framework.forms.user_login_form import UserLoginForm
from app.framework.auth_service import AuthService
from app.framework.decorators.inject import inject
from app.services.user_service import UserService
from app import app

@app.post("/login")
@inject
def login(userService: UserService, authService: AuthService):
    form = UserLoginForm.from_json(request.json)

    if form.validate():
        user = userService.find_user_entity_by_username(form.username.data)

        if user is None:
            # Pour des raison de sécurité on tends à retourner la même erreur
            # de connection, si l'utilisateur s'est trompé de mots de passe
            # ou si l'utilisateur n'existe pas (évite de récupérer la liste
            # des utilisateurs par brute force)
            raise Exception('Invalid password')

        token = authService.login(user, form)

        return jsonify({ 'token': token })

    # Pour des raison de sécurité on tends à retourner la même erreur
    # de connection, si l'utilisateur s'est trompé de mots de passe
    # ou si l'utilisateur n'existe pas (évite de récupérer la liste
    # des utilisateurs par brute force)
    raise Exception('Invalid password')