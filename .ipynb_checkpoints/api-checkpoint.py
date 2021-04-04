from flask import Flask
from flask import jsonify
from user import *

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello World'

@app.route('/user/<username>')
def getUserInformation(username):
    resp = getUserInfo(username)
    # print(resp)
    return jsonify(resp)

@app.route('/subscriptions/<username>')
def getUserSubscriptions(username):
    userRestId = getUserInfo(username)['rest_id']
    resp = getUserFollowing(userRestId)

    return resp.to_json()



if __name__ == "__main__":
    app.run()
