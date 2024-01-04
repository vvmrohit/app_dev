from flask import Flask,jsonify, request, render_template
from flask_restful import Api, Resource
import os

from pymongo import MongoClient

client = MongoClient("mongodb://db:27017")
db = client.aNewDb
UserNum = db["UserNum"]

UserNum.insert_one({
    'num_of_users' : 0
})

class Visit(Resource):
    def get(self):
        prev_num = UserNum.find({})[0]['num_of_users']
        new_num = prev_num + 1
        UserNum.update_one({},{"$set": {"num_of_users":new_num}})
        return str("Hello User " + str(new_num))


app = Flask(__name__)
api = Api(app)


def checkPostedData(postedData, functionName):
    if (functionName == "add" or functionName== "subtract" or functionName == "multiply"):
        if "x" not in postedData or "y" not in postedData:
            return 301
        else:
            return 200
    if functionName=="divide":
        if "x" not in postedData or "y" not in postedData:
            return 301
        elif postedData["y"]==0:
            return 302
        else:
            return 200 
    

class Add(Resource):
    def post(self):
        postedData = request.get_json()
        status_code = checkPostedData(postedData, "add")
        if status_code!= 200:
            retJson = {
                "Message": "Missing parameters. Please check if you are passing both x and y",
                "Status Code": status_code
            }
            return jsonify(retJson)
        
        x = postedData["x"]
        y = postedData["y"]
        x = int(x)
        y = int(y)
        ret = x+y
        retMap = {
            'Sum' : ret,
            'Status Code' : 200
        }
        return jsonify(retMap)

class Subtract(Resource):
    def post(self):
        postedData = request.get_json()
        status_code = checkPostedData(postedData, "subtract")
        if status_code!= 200:
            retJson = {
                "Message": "Missing parameters. Please check if you are passing both x and y",
                "Status Code": status_code
            }
            return jsonify(retJson)
        
        x = postedData["x"]
        y = postedData["y"]
        x = int(x)
        y = int(y)
        ret = x-y
        retMap = {
            'Subtraction_Result' : ret,
            'Status Code' : 200
        }
        return jsonify(retMap)

class Divide(Resource):
    def post(self):
        postedData = request.get_json()
        status_code = checkPostedData(postedData, "divide")
        if status_code == 301:
            retJson = {
                "Message": "Missing parameters. Please check if you are passing both x and y",
                "Status Code": status_code
            }
            return jsonify(retJson)
        elif status_code == 302:
            retJson = {
                "Message": "You have entered y value as 0 which is not valid for division",
                "Status Code": status_code
            }
            return jsonify(retJson)
        
        x = postedData["x"]
        y = postedData["y"]
        x = int(x)
        y = int(y)
        ret = x / y
        retMap = {
            'Division_Result': ret,
            'Status Code': 200
        }
        return jsonify(retMap)


class Multiply(Resource):
    def post(self):
        postedData = request.get_json()
        status_code = checkPostedData(postedData, "multiply")
        if status_code!= 200:
            retJson = {
                "Message": "Missing parameters. Please check if you are passing both x and y",
                "Status Code": status_code
            }
            return jsonify(retJson)
        
        x = postedData["x"]
        y = postedData["y"]
        x = int(x)
        y = int(y)
        ret = x*y
        retMap = {
            'Multiplication_Result' : ret,
            'Status Code' : 200
        }
        return jsonify(retMap)

api.add_resource(Add,"/add")
api.add_resource(Subtract,"/subtract")
api.add_resource(Divide,"/divide")
api.add_resource(Multiply,"/multiply")
api.add_resource(Visit,"/hello")



@app.route('/')
def calculator():
    return ('hello_world!')


if __name__=="__main__":
    app.run(host='0.0.0.0',port=5050)