from flask import Flask,jsonify, request

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Hello World!"

@app.route('/addnums',methods=['POST'])
def addnumber():
    dataDict = request.get_json()
    sum = 0
    x = dataDict["x"]   
    y = dataDict["y"]
    answer = {
        "x" : x,
        "y" : y,
        "x+y": x+y
    }
    return (answer),200

@app.route('/hitthere')
def hi_there_everyone():
    return "I just checking how does it work"

@app.route('/bye')
def bye():
    return "Bye for now we will meet soon"

if __name__ == "__main__":
    app.run(debug=True)
