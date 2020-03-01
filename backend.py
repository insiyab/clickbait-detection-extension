from flask import Flask
from predict_youtube import *
import json

app = Flask(__name__)

@app.route('/', methods = ['GET'])
def hello_world():
    return 'Welcome to ClickSafe!'

@app.route('/is_clickbait', methods = ['GET'])
def check_for_clickbait():
    client_input = request.json

    title, views, likes, dislikes = None, None, None, None
    response = {
        "success": False,
        "is_clickbait": -1,
        "error": "INVALID_REQUEST"
    }

    if 'title' in client_input:
        title = str(client_input['title'])
    else:
        return json.dumps(response), 400 # title of video is required
    if 'views' in client_input:
        views = int(client_input['views'])
    if 'likes' in client_input:
        likes = int(client_input['likes'])
    if 'dislikes' in client_input:
        dislikes = int(client_input['dislikes'])

    try:
        response["is_clickbait"] = youtube_predictor(title, views, likes, dislikes, None)
        response["success"] = True
        response["error"] = "None"
        return response
    except Exception as err:
        print('Error:', err)
        response["success"] = False
        response["is_clickbait"] = -1
        response["error"] = "REQUEST_FAILED"
        return json.dumps(response), 400

    # return "checking for clickbait"

@app.route('/get_info', methods = ['GET'])
def get_more_info():
    client_input = request.json
    return "getting more information"
