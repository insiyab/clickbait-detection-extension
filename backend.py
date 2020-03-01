from flask import Flask
from predict_youtube import *
from lang_parse import *
from get_frames import *
import json
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/', methods = ['GET'])
def hello_world():
    return 'Welcome to ClickSafe!'

@app.route('/is_clickbait', methods = ['POST'])
def check_for_clickbait():
    client_input = request.json

    # create base response
    response = {
        "success": False,
        "is_clickbait": -1,
        "error": "INVALID_REQUEST"
    }

    # get parameters from JSON request
    title, views, likes, dislikes, comments = None, None, None, None
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
    if 'comments' in client_input:
        comments = int(client_input['comments'])

    # analyze parameters and send JSON response
    try:
        response["is_clickbait"] = youtube_predictor(title, views, likes, dislikes, comments)
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

@app.route('/get_info', methods = ['POST'])
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

    # if 'audio_transcription' in client_input:
    #     audio_transcription = str(client_input['audio_transcription'])
    # else:
    #     response["error"] = "MISSING_AUDIO_TRANSCRIPTION"
    #     return json.dumps(response), 400

    # download YouTube video to vid_shots folder as .mp4
    try:
        os.system("cd vid_shots && rm -rf *.mp4 && " \
	       "youtube-dl --no-check-certificate -f mp4 --restrict-filenames " + URL \
           + " && cp *.mp4 video.mp4")
    except Exception as err:
        print('Error:', err)
        response["success"] = False
        response["audio_analysis"] = ""
        response["video_analysis"] = ""
        response["error"] = "VIDEO_RETRIEVAL_FAILED"
        return json.dumps(response), 400

    # analyze video content and send JSON response
    try:
        video_path = os.path.join("vid_shots", "video.mp4")
        response["audio_analysis"] = audio_classify(video_path) # call appropriate function
        response["video_analysis"] = get_video_labels_and_safety(video_path)
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
