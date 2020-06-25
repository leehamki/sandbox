import json
import redis
import sys

from flask import Flask, request
from decimal import Decimal

from database import db_process

app = Flask(__name__)
# conn = redis.StrictRedis(host='localhost', port=50005, db=0)

# @app.route('/')
# def index():
#     return "Hello Flask"
#
# @app.route('/<name>', methods=['PUT'])
# def create(name):
#     parameter_dict = request.get_json(silent=True)
#     print(json.dumps(parameter_dict))
#     if len(parameter_dict) == 0:
#         return {"message":"FAIL"}
#     else:
#         for key, val in parameter_dict.items():
#             print(key + " " + val)
#             conn.set(key, val)
#         return {"message":"SUCCESS"}
#
# @app.route('/<name>', methods=['GET'])
# def read(name):
#         result = conn.get(name).decode('ascii')
#         return {"message":"SUCCESS", f"{name}": f"{result}"}
#
# @app.route('/<name>', methods=['PATCH'])
# def update(name):
#     parameter_dict = request.get_json(silent=True)
#     print(json.dumps(parameter_dict))
#     if len(parameter_dict) == 0:
#         return {"message": "FAIL"}
#     else:
#         for key, val in parameter_dict.items():
#             print(key + " " + val)
#             conn.set(key, val)
#         return {"message": "SUCCESS"}
#
# @app.route('/<name>', methods=['DELETE'])
# def delete(name):
#         conn.delete(name)
#         return {"message": "SUCCESS"}

def json_default(obj):
	if isinstance(obj, Decimal):
		return float(obj)

@app.route('/travel', methods=['POST'])
def create():
    parameter_dict = request.get_json(silent=True)
    print(parameter_dict)
    print(json.dumps(parameter_dict, ensure_ascii=False))
    if len(parameter_dict) == 0:
        return {"message":"FAIL"}
    else:
        for key, val in parameter_dict.items():
            print(key + " " + str(val))
            if key == "name":
                name = val
            elif key == "desc":
                desc = val
            elif key == "score":
                score = val
            elif key == "place":
                place = val
            elif key == "group":
                group = val

        db.insert(name, desc, score, place, group)
        return {"message":"SUCCESS"}

@app.route('/travel', methods=['GET'])
def read():
        result_list = []
        name = request.args.get('name', None)
        group = request.args.get('group', None)
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 2))

        result_list = db.select(name, group)
        totalpage = 1 if len(result_list) < limit else int(len(result_list) / limit) if len(result_list) % limit == 0 else int(len(result_list) / limit) + 1
        startnum = 0 if page == 1 else ((page - 1) * limit)
        endnum = (page*limit)
        prevpage = page if page == 1 else page - 1
        nextpage = totalpage if (page + 1) >= totalpage else page + 1
        return json.dumps({"message": "SUCCESS", "result": result_list[startnum:endnum], "total_page": totalpage,
                           "current_page": page, "prev_page": prevpage, "next_page": nextpage}
                          , default=json_default, ensure_ascii=False)

@app.route('/travel', methods=['PATCH'])
def update():
    parameter_dict = request.get_json(silent=True)
    print(json.dumps(parameter_dict, ensure_ascii=False))
    seq = request.args.get('seq', None)
    if len(parameter_dict) == 0 or seq == None:
        return {"message":"FAIL"}
    else:
        for key, val in parameter_dict.items():
            print(key + " " + str(val))
            if key == "name":
                name = val
            elif key == "desc":
                desc = val
            elif key == "score":
                score = val
            elif key == "place":
                place = val
            elif key == "group":
                group = val

        db.update(seq, name, desc, score, place, group)
        return {"message": "SUCCESS"}

@app.route('/travel', methods=['DELETE'])
def delete():
        seq = request.args.get('seq', None)
        db.delete(seq)
        return {"message": "SUCCESS"}

if __name__ == "__main__":
    db = db_process.mariaDB()
    result = db.db_connect()

    if result == False:
        sys.exit()

    app.run()


