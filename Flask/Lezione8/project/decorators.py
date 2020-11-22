from functools import wraps
from flask import g, abort
from project.errors import forbidden
from project.ruoli.models import Permission
from flask_login import current_user

# These decorators are built with the help of the functools package from the Python standard library 

'''
def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not g.current_user.can(permission):
                return forbidden('Permessi insufficienti')
            return f(*args, **kwargs)
        return decorated_function
    return decorator
'''

def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator    

def admin_required(f):    
    return permission_required(Permission.ADMIN)(f)
