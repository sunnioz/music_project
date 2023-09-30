from music import db,app
from flask_login import UserMixin
from music import bcrypt
from music import login_manager
from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model,UserMixin):
    id = db.Column(db.Integer(),primary_key = True)
    username = db.Column(db.String(length=30),nullable = False,unique = True)
    email_address = db.Column(db.String(length=50),nullable = False,unique = True)
    password_hash = db.Column(db.String(length=50),nullable = False)

    def __repr__(self) -> str:
        return f'<User> {self.username}'

    def get_token(self,expires_sec=300):
        serial = Serializer(app.config['SECRET_KEY'])
        return serial.dumps({'user_id':self.id})
    
    @staticmethod
    def verify_token(token):
        serial = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = serial.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    @property
    def password(self):
        return self.password_hash
    @password.setter
    def password(self,plan_text_passeword):
        self.password_hash = bcrypt.generate_password_hash(plan_text_passeword,10).decode('utf-8')

    def check_password_correction(self, attempted_password):
        if bcrypt.check_password_hash(self.password_hash, attempted_password):
            return True
        return False

class Songs(db.Model):
    id = db.Column(db.Integer(),primary_key =True)
    ten = db.Column(db.String(length=50),nullable = False,unique = True)
    nghesi = db.Column(db.String(length=50),nullable = False)
    theloai = db.Column(db.String(length=30),nullable = False)
    img = db.Column(db.String(length = 200))
    link = db.Column(db.String(length=200),nullable = False,unique = True)

class Playlist(db.Model):
    user_id = db.Column(db.Integer(),db.ForeignKey('user.id'),primary_key = True)
    song_id = db.Column(db.Integer(),db.ForeignKey('songs.id'),primary_key  = True)
    user = db.relationship('User',backref = "songs",lazy = True)
    songs = db.relationship('Songs',backref='user',lazy = True)
