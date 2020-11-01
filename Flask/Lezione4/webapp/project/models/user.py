from project import db


class User(db.Model):

    # Create a table in the db
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    profile_image = db.Column(
        db.String(20), nullable=False, default="default_profile.png"
    )
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    # This connects BlogPosts to a User Author.
    posts = db.relationship("BlogPost", backref="author", lazy=True)

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        # https://stackoverflow.com/questions/23432478/flask-generate-password-hash-not-constant-output
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"UserName: {self.username}"
