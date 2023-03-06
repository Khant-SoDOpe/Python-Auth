from flask import Flask, jsonify, request,g
from flask_restful import Api, Resource
import jwt
import datetime
from functools import wraps
from pymongo import MongoClient
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)
CORS(app)
app.config['SECRET_KEY'] = "andrew"

cluster = MongoClient("mongodb+srv://aviothicedu:hello@cluster0.nghuy2n.mongodb.net/?retryWrites=true&w=majority")
db = cluster["Data"]
collection = db["user_data"]

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')

        if not token:
            return {'message': 'Token is missing'}, 401
        
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            g.user = data['user']

        except:
            return {'message': 'Token is invalid'}, 401

        return f(*args, **kwargs)

    return decorated


class UnprotectedResource(Resource):
    def get(self):
        return jsonify({'message': 'Anyone can view this!'})

class ProtectedResource(Resource):
    @token_required
    def get(self):
        results = collection.find_one({"username":g.user})
        if results:
            results.pop('_id', None)
            return jsonify(results)

class signupResource(Resource):
    def get(self,username,password):
        
        result = collection.find_one({"username":username})
        if result:
            return {'message': 'Username already exists'}, 409
        
        post = {"username":username,"password":password}
        collection.insert_one(post)
        return {'message': 'signup sucessfully'},201
        

class LoginResource(Resource):
    def get(self, username, password):

        results = collection.find_one({"username":username})
        if results:
            if password == results["password"]:
                token = jwt.encode({'user': username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                                app.config['SECRET_KEY'], algorithm='HS256')
                return {'token': token}
            else:
                return jsonify({'message':'Wrong Password'}),401

        return jsonify({'message':'Username not found'}),401


api.add_resource(LoginResource, '/login/<string:username>/<string:password>')
api.add_resource(UnprotectedResource, '/unprotected')
api.add_resource(ProtectedResource, '/protected')
api.add_resource(signupResource,'/signup/<string:username>/<string:password>')

if __name__ == "__main__":
    app.run(debug=True)