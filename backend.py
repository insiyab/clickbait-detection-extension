from flask import Flask
from predict_youtube import *
from lang_parse import *
from get_frames import *
import json
import os
from flask_cors import CORS
import time

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

# if __name__ == '__main__':
#     parser = argparse.ArgumentParser(description="Predict if a Youtube video is clickbait or not.")
#     parser.add_argument(
#         "--title", "-t",
#         type=str, help="Title.", required=True)
#     parser.add_argument(
#         "--views", "-v",
#         type=int, help="Number of views.", required=False)
#     parser.add_argument(
#         "--likes", "-l",
#         type=int, help="Number of likes.", required=False)
#     parser.add_argument(
#         "--dislikes", "-d",
#         type=int, help="Number of dislikes.", required=False)
#     parser.add_argument(
#         "--comments", "-c",
#         type=int, help="Number of comments.", required=False)
#     parser.add_argument(
#         "--URL", "-u",
#         type=str, help="URL of video.", required=False)
#     args = parser.parse_args()
#
#     print(youtube_predictor(args.title, args.views, args.likes, args.dislikes, args.comments))
#
#     if(args.URL is not None):
#         # os.system("bash load.sh")
#         os.system("cd vid_shots && rm -rf *.mp4 && youtube-dl --no-check-certificate -f mp4 --restrict-filenames " + str(args.URL) + " && cp *.mp4 video.mp4")
#         # os.system("cd vid_shots && cp *.mp4 video.mp4")
#         # time.sleep(2000)
#         video_path = os.path.join("vid_shots", "video.mp4")
#         print(audio_classify(video_path))
#         print(get_video_labels_and_safety(video_path))
