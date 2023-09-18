from flask import Flask, request
from flask_cors import CORS
import db.character
import db.banner
import db.users
import json

app = Flask(__name__)

def mockCalculator():
    return {""}

@app.route('/auth/signup', methods=["POST"])
def register():
    data = request.get_json()
    data = json.loads(data)
    name = data['name']
    username = data['username']
    password = data['password']
    validation = db.users.register(name, username, password)
    if validation == True:
        return json.dumps({"message": "Sign Up Successfully"})
    else:
        return json.dumps({"error": "Use login instead"})
    
@app.route('/auth/users', methods=["POST"])
def authentication():
    data = request.get_json()
    data = json.loads(data)
    username = data['username']
    password = data['password']
    auth = db.users.login(username, password)
    if auth == False:
        return json.dumps({"error": "Wrong Password"})
    else:
        return json.dumps({"message": "Login Successfully"})

@app.route('/get/rerun-history')
def getCharacterRerunHistory():
    return json.dumps(db.character.sendCharacterRerunHistory())

@app.route('/get/recent-rerun-history')
def getRecentRerunHistory():
    return json.dumps(db.banner.sendRecentCharacterBanner())

@app.route('/calculate/banner-history', methods=["POST"])
def recalculateBannerHistory():
    data = request.get_json()
    data = json.loads(data)
    date = data["date"]
    character_names = db.character.getCharacterNames()
    for name in character_names:
        db.banner.calculateBannerEstimationData(date[0], date[1], date[2], name)
    return json.dumps(db.character.sendCharacterRerunHistory())

@app.route('/planner/calculate', methods=["POST"])
def calculatePlannerData():
    data = data['input']

@app.route('/planner/store-data', methods=["POST"])
def savePlannerData():
    data = request.get_json()
    data = json.loads(data)
    username = data["username"]
    input_data = data["input"]
    output_data = data["output"]
    save_name = data["save_name"]
    check = db.users.savePlannerData(username, input_data, output_data, save_name)
    if check == False:
        return json.dumps({"error": "Data limit reached"})
    else:
        return json.dumps({"message": "Saved Successfully"})

if __name__ == '__main__':
    app.run(debug=True)
    CORS(app, ['http://localhost'])
