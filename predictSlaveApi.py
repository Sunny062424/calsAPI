from flask import Flask, request, jsonify
import sys
import pandas as pd
import pickle
import warnings
from flask_cors import CORS

warnings.filterwarnings(action="ignore")

app = Flask(__name__)

CORS(app)
cors = CORS(app, resource={
    r"/*":{
        "origins":"*"
    }
})

with open('./models/modelCalsList.pkl', 'rb') as f:
    calsModels = pickle.load(f)
 
with open('./models/modelCalsCnt.pkl', 'rb') as f2:
    cntModel = pickle.load(f2)


@app.route('/')
def hello_world():
    return 'openapi server is running'

#거더개수, 거더간격 모두 입력 시 슬라브 두께 예측
@app.route("/predictSlaveGAll", methods=['POST'])
def predictSlaveAll():
    try:
        data = request.get_json()
        print("받은 Json 데이터 ", data)

        cnt = data["g_cnt"]
        gap = data["g_gap"]

        features = pd.DataFrame([[cnt, gap]])

        predictValue = int( calsModels[2].predict(features) )

        predictValue

        response = {
            "result": "{}".format(predictValue)
        }
        return jsonify(response)
    except Exception as e:
        print(e)
        response = {
        "result": "not json format"
        }
        return jsonify(response)
    
#거더개수 입력 시 슬라브 두께 예측
@app.route("/predictSlaveGCnt", methods=['POST'])
def predictSlaveByCnt():
    try:
        data = request.get_json()
        print("받은 Json 데이터 ", data)

        cnt = data["g_cnt"]

        feature = pd.DataFrame([[cnt]])

        predictValue = int( calsModels[0].predict(feature) )

        predictValue

        response = {
            "result": "{}".format(predictValue)
        }
        return jsonify(response)
    except Exception as e:
        print(e)
        response = {
        "result": "not json format"
        }
        return jsonify(response)
      
#거더간격 입력 시 슬라브 두께 에측    
@app.route("/predictSlaveGGap", methods=['POST'])
def predictSlaveByGap():
    try:
        data = request.get_json()
        print("받은 Json 데이터 ", data)

        gap = data["g_gap"]

        feature = pd.DataFrame([[gap]])

        predictValue = int( calsModels[1].predict(feature) )

        predictValue

        response = {
            "result": "{}".format(predictValue)
        }
        return jsonify(response)
    except Exception as e:
        print(e)
        response = {
        "result": "not json format"
        }
        return jsonify(response)
    
#교량 폭원 입력 시 거더개수 예측
@app.route("/predictSlaveGWidth", methods=['POST'])
def predictSlaveByWidth():
    try:
        data = request.get_json()
        print("받은 Json 데이터 ", data)

        width = data["width"]

        feature = pd.DataFrame([[width]])

        predictValue = int( cntModel.predict(feature) )

        predictValue

        response = {
            "result": "{}".format(predictValue)
        }
        return jsonify(response)
    except Exception as e:
        print(e)
        response = {
        "result": "not json format"
        }
        return jsonify(response)
    
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)