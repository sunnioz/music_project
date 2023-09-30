from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from music.models import User,Songs,Playlist
from flask_admin.contrib.sqla import ModelView
from music import db,app
from music import bcrypt

admin = Admin(app,template_mode='bootstrap3')

class UserView(ModelView):
    def on_model_change(self, form, model, is_created):
        model.password_hash = bcrypt.generate_password_hash(model.password_hash)

class PlaylistView(ModelView):
    form_columns = [
        'user_id',
        'song_id',
    ]
    list_columns = [
        'user_id',
        'song_id',
    ]


admin.add_view(UserView(User,db.session))
admin.add_view(ModelView(Songs,db.session))
admin.add_view(PlaylistView(Playlist,db.session))

