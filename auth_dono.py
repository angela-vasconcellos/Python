from flask import request, make_response, Flask
from functools import wraps
from flask_mysqldb import MySQL

app = Flask(__name__)

conexao=MySQL(app)

def auth_required(f):
    @wraps(f)
    def decorated (*args, **kwargs):
        auth = request.authorization
        if auth and auth.username == 'username1' and auth.password == 'password':
            return f(*args, **kwargs) 
        return make_response ('Login/senha inválidos!', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
    return decorated
