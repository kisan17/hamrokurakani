from flask import Flask, redirect, request, url_for
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, logout_user
from hamrokurakani import db, login_manager
from hamrokurakani.models import Message, User

app = Flask(__name__)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/logout')
def logout():
    logout_user()
    return 'Logged Out'


"""This is for database models."""


class ModeratedModelView(ModelView):

    def is_accessible(self):
        if current_user.is_authenticated and not current_user.is_anonymous and current_user.id == 1:
            return True

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('admin.index', next=request.url))

    can_export = True


"""This is for dashboard and admin panel models."""


class ModeratedAdminIndexView(AdminIndexView):
    def is_accessible(self):
        if current_user.is_authenticated and not current_user.is_anonymous and current_user.id == 1:
            return True


admin = Admin(name="Admin Panel", template_mode='bootstrap3',
              index_view=ModeratedAdminIndexView(name='Dashboard',  url='/admin'))


admin.add_view(ModeratedModelView(User, db.session))
admin.add_view(ModeratedModelView(Message, db.session))
