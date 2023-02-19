from flask import Flask
from flask_restful import Api , Resource
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
api = Api(app)

class HellWorld(Resource):
    def get(self,name,test):
        return {"data" : name ,"test":test}

    def post(self):
        return {"data" : "Hello Wor"}

class add(Resource):
    def get(self,onenumber,twonumber):
        threenumber = onenumber + twonumber
        return { "data" : threenumber}


class minus(Resource):
    def get(self,onenumber,twonumber):
        threenumber = onenumber - twonumber
        return {"data": threenumber}


api.add_resource(HellWorld,"/helloworld/<string:name>/<int:test>")
api.add_resource(add,"/add/<int:onenumber>/<int:twonumber>")
api.add_resource(minus,"/minus/<int:onenumber>/<int:twonumber>")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8082)