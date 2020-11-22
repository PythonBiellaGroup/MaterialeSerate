from datetime import datetime
# Per la gestione delle password
import hashlib
from werkzeug.security import generate_password_hash, check_password_hash
# Per flask_login
from flask_login import UserMixin, AnonymousUserMixin
from project import db, login_manager
# Per token (conferma mail)
from flask import current_app, request, url_for
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from project.ruoli.models import Ruolo
from project.ruoli.models import Permission

class Utente(UserMixin, db.Model):
    __tablename__ = 'utenti'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    name = db.Column(db.String(64))
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text())
    '''
    The two timestamps are given a default value of the current time. 
    Note that the datetime.utcnow is missing the () at the end. 
    This is because the default argument in db.Column() can take a function as a value
    '''
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    # last_seen è aggiornato dalla funzione ping, chiamata da before_request ad ogni request
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
    avatar_hash = db.Column(db.String(32))
    # FK - Ruolo dell'utente
    role_id = db.Column(db.Integer, db.ForeignKey('ruoli.id'))
    '''
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    followed = db.relationship('Follow',
                               foreign_keys=[Follow.follower_id],
                               backref=db.backref('follower', lazy='joined'),
                               lazy='dynamic',
                               cascade='all, delete-orphan')
    followers = db.relationship('Follow',
                                foreign_keys=[Follow.followed_id],
                                backref=db.backref('followed', lazy='joined'),
                                lazy='dynamic',
                                cascade='all, delete-orphan')
    comments = db.relationship('Comment', backref='author', lazy='dynamic')


    @staticmethod
    def add_self_follows():
        for user in Utente.query.all():
            if not user.is_following(user):
                user.follow(user)
                db.session.add(user)
                db.session.commit()
    '''

    '''
    Utile per il popolamento dei dati e per i test
    '''
    @staticmethod
    def insert_test_users():
        # Il ruolo degli utenti è quello di default
        utenti = [ 
            ("test1@test.it", "mariateresa", "pwd1" ),
            ("test2@test.it", "davcom", "pwd2" ),
        ]
        for ut in utenti:
            ut_db = Utente.query.filter_by(email=ut[0]).first()
            if ut_db is None:
                ut_db = Utente(email=ut[0], username=ut[1], password=ut[2], confirmed=True)
            db.session.add(ut_db)
        db.session.commit()    


    def __init__(self, **kwargs):
        super(Utente, self).__init__(**kwargs)
        # Gestione dell'amministratore: email da variabile di ambiente
        if self.ruolo is None:
            if self.email == current_app.config['PBG_ADMIN']:
                self.ruolo = Ruolo.query.filter_by(name='Administrator').first()
            if self.ruolo is None:
                self.ruolo = Ruolo.query.filter_by(default=True).first()
        if self.email is not None and self.avatar_hash is None:
            self.avatar_hash = self.gravatar_hash()
        '''
        self.follow(self)
        '''

    @property
    def password(self):
        raise AttributeError('La password non si può leggere')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Per conferma mail
    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id}).decode('utf-8')
    
    # Per conferma mail
    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
            print(data)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True
    
    # Per conferma mail (generazione token)
    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id}).decode('utf-8')
    
    # Per conferma mail
    @staticmethod
    def reset_password(token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        user = Utente.query.get(data.get('reset'))
        if user is None:
            return False
        user.password = new_password
        db.session.add(user)
        return True
    
    # Per conferma mail
    def generate_email_change_token(self, new_email, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps(
            {'change_email': self.id, 'new_email': new_email}).decode('utf-8')

    # Per cambio mail
    def change_email(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('change_email') != self.id:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.query.filter_by(email=new_email).first() is not None:
            return False
        self.email = new_email
        self.avatar_hash = self.gravatar_hash()
        db.session.add(self)
        return True

    # Ruoli
    def can(self, perm):
        return self.ruolo is not None and self.ruolo.has_permission(perm)

    def is_administrator(self):
        return self.can(Permission.ADMIN)

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    # Avatar
    def gravatar_hash(self):
        return hashlib.md5(self.email.lower().encode('utf-8')).hexdigest()

    def gravatar(self, size=100, default='identicon', rating='g'):
        url = 'https://secure.gravatar.com/avatar'
        hash = self.avatar_hash or self.gravatar_hash()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=hash, size=size, default=default, rating=rating)

    '''
    def follow(self, user):
        if not self.is_following(user):
            f = Follow(follower=self, followed=user)
            db.session.add(f)

    def unfollow(self, user):
        f = self.followed.filter_by(followed_id=user.id).first()
        if f:
            db.session.delete(f)

    def is_following(self, user):
        if user.id is None:
            return False
        return self.followed.filter_by(
            followed_id=user.id).first() is not None

    def is_followed_by(self, user):
        if user.id is None:
            return False
        return self.followers.filter_by(
            follower_id=user.id).first() is not None

    @property
    def followed_posts(self):
        return Post.query.join(Follow, Follow.followed_id == Post.author_id)\
            .filter(Follow.follower_id == self.id)


    def to_json(self):
        json_user = {
            'url': url_for('api.get_user', id=self.id),
            'username': self.username,
            'member_since': self.member_since,
            'last_seen': self.last_seen
            'posts_url': url_for('api.get_user_posts', id=self.id),
            'followed_posts_url': url_for('api.get_user_followed_posts',
                                          id=self.id),
            'post_count': self.posts.count()
        }
        return json_user
    '''
    
    def generate_auth_token(self, expiration):
        s = Serializer(current_app.config['SECRET_KEY'],
                       expires_in=expiration)
        return s.dumps({'id': self.id}).decode('utf-8')

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return Utente.query.get(data['id'])

    def __repr__(self):
        return '<Utente %r>' % self.username

class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser

@login_manager.user_loader
def load_user(user_id):
    return Utente.query.get(int(user_id))