"""
server.py

This script creates all the private REST API endpoints for the gacha planner.
Created by Pattarapark Chutisamoot around mid-september

"""

"""
WORKING IN PROGRESS

1. Big Data for Banner History Page including half patches indicator
2. Database modifications to include half patches.
3. Banner History sort for backend

"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import db.character
import db.banner
import db.users
import db.primocalc
import json
import datetime

app = Flask(__name__)

app.json.sort_keys = False
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}}, supports_credentials=True)

@app.route('/api/auth/signup', methods=["POST"])
def register():
    data = request.get_json()
    # data = json.loads(data)
    name = data['name']
    username = data['username']
    password = data['password']
    validation = db.users.register(name, username, password)
    if validation == True:
        return jsonify({"message": "Sign Up Successfully"})
    else:
        return jsonify({"error": "Use login instead"})

@app.route('/api/planner/check-valid-banner')
def checkValidBanner():
    # version = db.banner.checkValidInputBanner()
    # print(version)
    VERSION = '4.2'
    END_DATE = datetime.date(2023, 11, 28)
    full_version = db.primocalc.getcurrent(VERSION, END_DATE)
    # full_version = db.primocalc.getcurrent(version[0][0], version[0][2])
    full_version[0] = str(full_version[0])
    return jsonify({"load": full_version})
    
@app.route('/api/auth/users', methods=["POST"])
def authentication():
    data = request.get_json()
    # data = json.loads(data)
    username = data['username']
    password = data['password']
    auth = db.users.login(username, password)
    if auth == False:
        return jsonify({"error": "Wrong Password"})
    else:
        return jsonify({"message": "Login Successfully"})

@app.route('/api/get/rerun-ranking')
def getCharacterRerunHistory():
    return jsonify(db.banner.getRerunRanking())

@app.route('/api/get/recent-rerun-history')
def getRecentRerunHistory():
    return jsonify(db.banner.getRecentCharacterBanner())

@app.route('/api/get/all-banner-data')
def getAllCharacterBannerData():
    # Uncomment these lines to recalculate the rankings.
    # character_names = db.character.getCharacterNames()
    # for name in character_names:
    #     db.banner.calculateBannerEstimationData(name)
    return jsonify(db.character.getAllCharacterData())

# @app.route('/api/calculate/banner-history', methods=["GET"])
# def recalculateBannerHistory():
#     character_names = db.character.getCharacterNames()
#     for name in character_names:
#         db.banner.calculateBannerEstimationData(name)
#     return jsonify(db.character.sendCharacterRerunHistory())

@app.route('/api/planner/checkvalidpatch', methods=["POST"])
def checkValidInputBanner():
    possible_banners = db.banner.checkValidInputBanner()
    return jsonify(possible_banners)

@app.route('/api/planner/calculate', methods=["POST"])
def calculatePlannerData():
    data = request.get_json()
    # data = json.loads(data)
    primos = data['primogems']
    crystals = data['crystals']
    fates = data['fates']
    guarantee = data["guarantee"]
    pity = data['pity']
    targetpatch = data['targetpatch']
    half = data['half']
    fiveorprimos = data['fiveorprimos']
    havewelk = data["havewelkin"]
    havebp = data["havebp"]
    welkin = data["welkindays"]
    bp = data["bp"]
    welkinplan = data["welkinplan"]
    bpplan = data["bpplan"]
    fivestars = data["fivestars"]
    primowant = data["primowant"]

    previous_patch_data = db.banner.getPreviousPatch()
    previous_currentpatch = float(previous_patch_data[0][0])
    previous_currentpatch_date = previous_patch_data[0][2]
    # print(currentpatch)

    calculation_results = db.primocalc.calculations(primos, crystals, fates, pity, havewelk, havebp, welkinplan, bpplan,
                                                    fiveorprimos, previous_currentpatch, previous_currentpatch_date, welkin, bp, guarantee, targetpatch, 
                                                    half, fivestars, primowant)
    
    # print("Lol: ", type(calculation_results))
    return jsonify(calculation_results)

@app.route('/api/planner/save-data', methods=["POST"])
def savePlannerData():
    data = request.get_json()
    # data = json.loads(data)
    username = data["username"]
    input_data = data["input"]
    output_data = data["output"]
    save_name = data["save_name"]
    check_operation = db.users.savePlannerData(username, input_data, output_data, save_name)
    if check_operation == False:
        return jsonify({"error": "Data limit reached, user doesn't exists or invalid save name"})
    else:
        return jsonify({"message": "Saved Successfully"})

@app.route('/api/user/fetch-data', methods=["POST"])
def fetchPlannerData():
    data = request.get_json()
    # data = json.loads(data)
    username = data["username"]
    user_data = db.users.fetchUserData(username)
    if user_data == False:
        return jsonify({"error": "No saved data found"})
    else:
        return jsonify(user_data)

@app.route('/api/user/delete-data', methods=["POST"])
def deletePlannerData():
    data = request.get_json()
    username = data["username"]
    save_name = data["save_name"]
    db.users.deleteUserData(username, save_name)
    return jsonify({"message": "Deleted successfully"})
    
# @app.route('/api/planner/calculate-progress', methods=["POST"])
# def calculateProgress():
#     data = request.get_json()
#     # data = json.loads(data)
#     username = data["username"]
#     save_name = data["save_name"]
#     user_data = db.users.fetchUserData(username)
#     if user_data == False:
#         return jsonify({"error": "No saved data found"})
#     else:
#         return jsonify(user_data)

if __name__ == '__main__':
    app.run(debug=True)
