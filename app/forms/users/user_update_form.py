from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.fields.choices import SelectMultipleField
from wtforms.validators import DataRequired

from app.framework.decorators.inject import inject
from app.services.role_service import RoleService


class UserUpdateForm(FlaskForm):
    class Meta:
        csrf = False
    password = StringField('password')
    lastname = StringField('lastname', validators=[DataRequired()])
    firstname = StringField('firstname', validators=[DataRequired()])

    roles = SelectMultipleField('roles', validators=[DataRequired()])

    @inject
    def __init__(self, roleService: RoleService, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.roleService = roleService
        self.roles.choices = [str(role.id) for role in self.roleService.find_all_active_entities()]
