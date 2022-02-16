import datetime
import time
import os
import query_process
import json
from bson import json_util

from flask import Flask, request, jsonify
from flask_cors import CORS
import pymongo
import tensorflow as tf

app = Flask(__name__)
CORS(app)
client = pymongo.MongoClient(os.getenv('MONGODB_HOST'),
                             username=os.getenv('MONGODB_USERNAME'),
                             password=os.getenv('MONGODB_PASSWORD'),
                             authSource='searchin',
                             connectTimeoutMS=300000)
searchdb = client['searchin']
metadata = searchdb['metadata']
stem2idC = searchdb['stem2idC']
steminfo = searchdb['steminfo']
lineinfo = searchdb['lineinfo']
workinfo = searchdb['workinfo']
phobox = searchdb['phobox']

line2token = searchdb['line2token']
token2info = searchdb['token2info']

one_step_reloaded = tf.saved_model.load('./Ydata/one_step')

# checked.
def parse_json(data):
    return json.loads(json_util.dumps(data))

@app.route('/detail')
def detail():
    code = request.args.get('code')
    limit = request.args.get('limit')
    thiswork = workinfo.find_one({'_id': code})
    detail = dict()
    if thiswork:
        detail['title'] = thiswork['title']
        detail['genre'] = thiswork['genre']
        detail['synopsis'] = thiswork['synopsis']
    else:
        detail['title'] = "not available"
        detail['genre'] = "not available"
        detail['synopsis'] = "not available"
    otherlines = lineinfo.find({"detail.code": code}).limit(int(limit))
    detail['otherlines'] = otherlines
    return parse_json(detail)

# checked
@app.route('/queryreg')
def queryreg():
    query = request.args.get('query')
    limit = request.args.get('limit')
    expanquery = query_process.expan_q(query)
    query_result_list = query_process.regGet(expanquery, int(limit), line2token, token2info)
    result_details = query_process.retrieveDetails(query_result_list, lineinfo)
    return parse_json(result_details)

# checked
@app.route('/querybm25')
def querybm25():
    query = request.args.get('query')
    andor = request.args.get('andor')
    limit = request.args.get('limit')
    query_result_list = query_process.query_tree(query, int(limit), int(andor), stem2idC, metadata, steminfo)
    result_details = query_process.retrieveDetails(query_result_list, lineinfo) #, workinfo
    return parse_json(result_details)

# checked
@app.route('/time')
def get_current_time():
    return {'time': time.time()}

# checked. suggest complete
@app.route('/querysug')
def querysug():
    query = request.args.get('query')
    expanquery = query_process.expan_q(query)
    return parse_json(expanquery)

# checked. switch list output
@app.route('/searchpho')
def searchpho():
    word = request.args.get('word')
    return parse_json(query_process.phoGet(word, phobox))

# checked. good practice LSTM -> <8 results
@app.route('/searchtext')
def searchPrompt():
    current_text = request.args.get('text')
    constantt = tf.constant([current_text])
    states = None
    limit = 0
    l = 0
    predictDict = dict()
    answerset = set()
    while True:
        if limit >= 8:
            break
        next_char = constantt
        result = [constantt]
        for n in range(50):
            next_char, states = one_step_reloaded.generate_one_step(next_char, states=states)
            if next_char in ['\n']:
                break
            result.append(next_char)
        stringans = tf.strings.join(result)[0].numpy().decode("utf-8")
        if stringans not in answerset:
            predictDict[l] = stringans
            answerset.add(stringans)
            l += 1
        limit += 1
    return jsonify(predictDict)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
