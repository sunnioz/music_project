from flask_admin import Admin
from flask import abort
from flask_login import current_user
from flask_sqlalchemy import SQLAlchemy
from music.models import User,Songs,Playlist
from flask_admin.contrib.sqla import ModelView
from music import db,app
from music import bcrypt
from music import login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


admin = Admin(app,template_mode='bootstrap3')


class Admin_Controll(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated and current_user.is_admin:
            return True
        else:
            return abort(404)


class UserView(Admin_Controll):
    def on_model_change(self, form, model, is_created):
        model.password_hash = bcrypt.generate_password_hash(model.password_hash)


class PlaylistView(Admin_Controll):
    form_columns = [
        'user_id',
        'song_id',
    ]
    list_columns = [
        'user_id',
        'song_id',
    ]

admin.add_view(UserView(User,db.session))
admin.add_view(Admin_Controll(Songs,db.session))
admin.add_view(PlaylistView(Playlist,db.session))

