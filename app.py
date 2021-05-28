from flask import Flask, request, jsonify, make_response
import json

app = Flask(__name__)


def get_data():
    speech= 'Demo Response'

    return {'fulfillmentText': speech}
def processRequest(req):

    query= req['queryResult']
    print(query)

    text= query.get('queryText', None)
    parameters= query.get('parameters', None)

    res= get_data()
    return res

@app.route('/')
def home():
    return None

@app.route('/webhook',methods=['POST'])
def webhook():

    req = request.get_json(silent= True, force=True)
    result= processRequest(req)

    res= json.dumps(result, indent= 4)
    r= make_response(res)
    r.headers['Content-type']= 'application/json'

    return r

if __name__ == "__main__":
    app.run(debug=True, port=5000)