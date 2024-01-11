from flask import Flask,jsonify, request, render_template
from flask_restful import Api, Resource
import os
import bcrypt

from pymongo import MongoClient

client = MongoClient("mongodb://db:27017")
db = client.SDB
users = db["users"]

app = Flask(__name__)
api = Api(app)

class Register(Resource):
    def post(self):
        postedData = request.get_json()
        username = postedData["username"]
        password = postedData["password"]
        hashed_pwd = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

        users.insert_one({
            "Username" : username,
            "Password" : hashed_pwd,
            "Sentence" : "",
            "Tokens" : 6
            })
        
        retJson = {
            "status" : 200,
            "msg" : "You have successfully registered for the API"
        }

        return jsonify(retJson)
    
def verifyPw(username, password):
    hashed_pwd = users.find({
        "Username" : username
    })[0]["Password"]
    
    if bcrypt.hashpw(password.encode("utf"),hashed_pwd) == hashed_pwd:
        return True
    else :
        return False


def countTokens(username):
    return users.find({"Username" : username})[0]["Tokens"]

    
class Store(Resource) :
    def post(self):
        #Step1 get the posted data
        postedData = request.get_json()

        #step2 read the data from the request
        username = postedData["username"]
        password = postedData["password"]
        sentence = postedData["sentence"]
        
        #step3 verify the username and password match
        correct_pw = verifyPw(username,password)

        if not correct_pw :
            retJson = {
                "status" : 302,
                "msg" : "Invalid Username or password"
            }
            return jsonify(retJson)
        
        #step4 verify the user have enough token
        num_tokens = countTokens(username)
        if num_tokens <=0:
            retJson = {
                "status" : 301,
                "msg" : "You don't have any tokens left. Please buy more to use the API"
            }
            return jsonify(retJson)
        #step5 store the sentence and reduce one token return 200
        users.update_one({
            "Username" : username 
            },
            {
                "$set" : {
                    "Sentence": sentence,
                    "Tokens": num_tokens -1
                }
            })
        retJson = {
            "status" : 200,
            "msg" : "Sentence saved successfully"
        }
        return jsonify(retJson)

class Get(Resource):
    def get(self):
        postedData = request.get_json()

        username = postedData["username"]
        password = postedData["password"]

        correct_pw = verifyPw(username,password)
        if not correct_pw:
            retJson = {
                "status" : 302,
                "msg" : "Incorrect username or password"
            }
            return jsonify(retJson)

        num_tokens = countTokens(username=username)
        if num_tokens <=0:
            retJson = {
                "status" : 301,
                "msg" : "You don't have enough tokens left"
            }
            return jsonify(retJson)
        
        sentence = users.find({
            "Username" : username})[0]["Sentence"]
        retJson = {
            "status" : 200,
            "sentence" : sentence
        }
        return jsonify(retJson)
        

        

    

api.add_resource(Register,"/register")
api.add_resource(Store,"/store")
api.add_resource(Get,"/get")


@app.route('/')
def calculator():
    return ('hello_world!')


if __name__=="__main__":
    app.run(host='0.0.0.0',port=5050)

        
        




