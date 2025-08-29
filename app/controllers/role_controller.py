from flask import jsonify, request
from app import app

from app.forms.role.role_form import RoleForm
from app.framework.decorators.auth_required import auth_required
from app.framework.decorators.inject import inject
from app.services.role_service import RoleService


@app.get('/roles')
@auth_required(level="ADMIN")
@inject
def get_all_roles(roleService: RoleService):
    return jsonify([r.serialize() for r in roleService.find_all()])

@app.get('/roles/<int:id>')
@auth_required(level="ADMIN")
@inject
def get_role_by_id(id, roleService: RoleService):
    dto = roleService.find_one(id)
    return jsonify(dto.serialize())

@app.post('/roles')
@auth_required(level="ADMIN")
@inject
def post_role(roleService: RoleService):
    form = RoleForm.from_json(request.json)
    if form.validate():
        dto = roleService.insert(form)

        return jsonify(dto.serialize())

    return jsonify(form.errors)

@app.put('/role/<int:id>')
@auth_required(level="ADMIN")
@inject
def put_role(id, roleService: RoleService):
    form = RoleForm.from_json(request.json)
    if form.validate():
        dto = roleService.update(id, form)

        return jsonify(dto.serialize()) if dto else None

    return jsonify(form.errors)

@app.delete('/role/<int:id>')
@auth_required(level="ADMIN")
@inject
def delete_role(id, roleService: RoleService):
    dto = roleService.delete(id)
    return jsonify(dto.serialize()) if dto else None