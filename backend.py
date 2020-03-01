from flask import Flask
from predict_youtube import *
import json
import os

app = Flask(__name__)

@app.route('/', methods = ['GET'])
def hello_world():
    return 'Welcome to ClickSafe!'

@app.route('/is_clickbait', methods = ['GET'])
def check_for_clickbait():
    client_input = request.json

    # create base response
    response = {
        "success": False,
        "is_clickbait": -1,
        "error": "INVALID_REQUEST"
    }

    # get parameters from JSON request
    title, views, likes, dislikes = None, None, None, None
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

    # analyze parameters and send JSON response
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

    # create base response
    response = {
        "success": False,
        "audio_analysis": "",
        "visual_analysis": "",
        "error": "INVALID_REQUEST"
    }

    # get parameters from JSON request
    URL, audio_transcription = None, None

    if 'URL' in client_input:
        URL = str(client_input['URL'])
    else:
        return json.dumps(response), 400

    if 'audio_transcription' in client_input:
        audio_transcription = str(client_input['audio_transcription'])
    else:
        response["error"] = "MISSING_AUDIO_TRANSCRIPTION"
        return json.dumps(response), 400

    # download YouTube video to vid_shots
    try:
        os.system("cd vid_shots && rm -rf *.mp4 && youtube-dl --no-check-certificate " + URL)
    except Exception as err:
        print('Error:', err)
        response["success"] = False
        response["audio_analysis"] = ""
        response["video_analysis"] = ""
        response["error"] = "VIDEO_RETRIEVAL_FAILED"
        return json.dumps(response), 400

    # analyze video content and send JSON response
    try:
        response["audio_analysis"] = {} # call appropriate function
        response["video_analysis"] = {} # call appropriate function
        response["success"] = True
        response["error"] = "None"
        return response
    except Exception as err:
        print('Error:', err)
        response["success"] = False
        response["audio_analysis"] = ""
        response["video_analysis"] = ""
        response["error"] = "ANALYSIS_FAILED"
        return json.dumps(response), 400

    # return "getting more information"
