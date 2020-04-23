import time
import json
import redis
from flask import Flask, request

app = Flask(__name__)
conn = redis.StrictRedis(host='localhost', port=50005, db=0)

@app.route('/')
def index():
    return "Hello Flask"

@app.route('/<name>', methods=['PUT'])
def create(name):
    parameter_dict = request.get_json(silent=True)
    print(json.dumps(parameter_dict))
    if len(parameter_dict) == 0:
        return {"message":"FAIL"}
    else:
        for key, val in parameter_dict.items():
            print(key + " " + val)
            conn.set(key, val)
        return {"message":"SUCCESS"}

@app.route('/<name>', methods=['GET'])
def read(name):
        result = conn.get(name).decode('ascii')
        return {"message":"SUCCESS", f"{name}": f"{result}"}

@app.route('/<name>', methods=['PATCH'])
def update(name):
    parameter_dict = request.get_json(silent=True)
    print(json.dumps(parameter_dict))
    if len(parameter_dict) == 0:
        return {"message": "FAIL"}
    else:
        for key, val in parameter_dict.items():
            print(key + " " + val)
            conn.set(key, val)
        return {"message": "SUCCESS"}

@app.route('/<name>', methods=['DELETE'])
def delete(name):
        conn.delete(name)
        return {"message": "SUCCESS"}

if __name__ == "__main__":
    app.run()


