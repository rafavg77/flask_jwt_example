from flask import Flask, jsonify, request, make_response
import jwt
import datetime
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisisthesecretkey'

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwgars):
        token = request.args.get('token')

        if not token:
            return jsonify({'message' : 'Token is missing!'})
        try:
            data = jwt.decode(token,app.config['SECRET_KEY'],algorithms=["HS256"])
        except:
            return jsonify({'message: ' : 'Token is invalid!'}),403
        
        return f(*args, **kwgars)

    return decorated

@app.route('/unprotected')
def unprotected():
    return jsonify({'message: ' : 'Anuone can view this!'})

@app.route('/protected')
@login_required
def protected():
    token = request.args.get('token')
    user = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
    print(user)
    return jsonify({'message ' : 'This is only avaliable for the people with valid tokens {}'.format(user['user'])})

@app.route('/login')
def login():
    auth = request.authorization
    if auth and auth.password =='password':
        token = jwt.encode({'user' : auth.username, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
        print(token)
        #return jsonify({'token' : jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])})
        return jsonify({'token' : token})
        
    return make_response('Could not Verify!',401,{'www-Authenticate' : 'Basic realm="Login Requires"'})

if __name__ == '__main__':
    app.run(debug=True)