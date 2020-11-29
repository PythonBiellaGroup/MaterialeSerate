from project import db


'''
The list of tasks for which permissions are needed is obviously application specific
The benefit of using powers of two for permission values is that it allows permissions 
to be combined, giving each possible combination of permissions a unique value to store 
in the role’s permissions field. 

For example, for a user role that gives users permission to follow 
other users and comment on posts, 
the permission value is FOLLOW + COMMENT = 3. 
This is a very efficient way to store the list of permissions assigned to each role.
'''
class Permission:
    FOLLOW = 1
    COMMENT = 2
    WRITE = 4
    MODERATE = 8
    ADMIN = 16

class Ruolo(db.Model):
    __tablename__ = 'ruoli'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    # n utenti hanno un certo ruolo
    users = db.relationship('Utente', backref='ruolo', lazy='dynamic')

    def __init__(self, **kwargs):
        super(Ruolo, self).__init__(**kwargs)
        # Since SQLAlchemy will set this field to None by default, 
        # a class constructor is added that sets it to 0 
        # if an initial value isn’t provided in the constructor arguments. 
        if self.permissions is None:
            self.permissions = 0

    '''
    Inserimento dei ruoli nel db; User è il default
    '''
    @staticmethod
    def insert_roles():
        roles = {
            'Utente': [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE],
            'Admin': [Permission.FOLLOW, Permission.COMMENT,
                              Permission.WRITE, Permission.MODERATE,
                              Permission.ADMIN],
        }
        default_role = 'Utente'
        for r in roles:
            role = Ruolo.query.filter_by(name=r).first()
            if role is None:
                role = Ruolo(name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        self.permissions = 0

    # The has_permission() method is the most complex of the set, as it relies on the bitwise
    # and operator & to check if a combined permission value includes the given basic per‐
    # mission
    def has_permission(self, perm):
        return self.permissions & perm == perm

    def __repr__(self):
        return self.name