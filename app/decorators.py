from functools import wraps
from flask import abort
from flask_login import current_user

def isFaculty():
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.faculty:
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def isAdmin():
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.admin:
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def isStudent():
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.student:
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def isLeader():
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.leader:
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator



    
