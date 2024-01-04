from flask import Flask,jsonify, request, render_template
from flask_restful import Api, Resource
import os
import bcrypt

from pymongo import MongoClient

client = MongoClient("mongodb://db:27017")
db = client.SDB
users = db["users"]

class Register(Resource):
    def post(self):
        postedData = request.get_json()
        username = postedData["username"]
        password = postedData["password"]
        hashed_pwd = bcrypt.hashed_pwd(password.encode('utf8'), bcrypt.gensalt())

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
    
class Store(Resource) :
    def post(self):
        #Step1 get the posted data
        postedData = request.get_json()

        #step2 read the data from the request
        username = postedData["username"]
        password = postedData["password"]
        sentence = postedData["sentence"]
        
        #step3 verify the username and password match
        db_result = {}
        if username != users.find({"username" : username}) :
            retJson = {
                "status" : 301,
                "msg" : "Invalid Username"
            }
            return jsonify(retJson)
        else :
            db_result = users.find({"username": username})
        
        if  not bcrypt.checkpw(password.encode('utf8'),db_result["password"]):
            retJson = {
                "status" : 301,
                "msg" : "Your Password is wrong please check it again"
            }
            return jsonify(retJson)
    
        
        #step4 verify the user have enough token
        if db_result["Token"]== 0:
            retJson = {
                "status" : 302,
                "msg" : "You don't have any token left. You need to buy more tokens"
            }
            return jsonify(retJson)

        #step5 store the sentence and reduce one token return 200
        




