import cv2
import os
import sys

def capture_frames(path, label_dict, topic_dict):
    vid = cv2.VideoCapture(path)

    try:
        
        # creating a folder named vid_shots if it does not exist already
        if not os.path.exists('vid_shots'):
            os.makedirs('vid_shots')
        # if the folder already exists, then make sure it's empty before adding the frames that are going to be captured
        else:
            shotlist = [ shot for shot in os.listdir('vid_shots')]
            for shot in shotlist:
                os.remove(os.path.join('vid_shots', shot))
      
    # if not created then raise error
    except OSError:
        print ('Error: Creating directory of vid_shots')
      
    # current frame we are looking at
    currentframe = 0
    # the fps of the video file
    fps = int(vid.get(cv2.CAP_PROP_FPS))
    # total amount of frames
    frame_count = vid.get(cv2.CAP_PROP_FRAME_COUNT)
    # video duration
    vid_duration = frame_count/fps
    # temporary set number of "frame captures" per video. Subject to change to accomodate length of video
    num_shots = round(vid_duration * 0.1)
    #a limit to keep track of our intervals and where and which frames we capture
    upper_limit = num_shots + 1
    #keeping track of the frame number we are capturing
    interval_num = 1

    while(True):
        # the frame we are targeting to capture
        interval = round(frame_count * (interval_num / upper_limit))
        # reading from frame
        ret,frame = vid.read()
        
        if ret:
            # if video is still left continue creating images
            # writing the frame
            if currentframe == interval:
                name = './vid_shots/frame' + str(currentframe) + '.jpg'
                cv2.imwrite(name, frame)
                # call functions here to populate dictionaries
                # do i need to write the frame capture or can I somehow analyze it without writing?
                # cause my functions that populate the dictionaries take in paths
                label_dict = detect_labels(name, label_dict)
                topic_dict = detect_safe_search(name, topic_dict)
                interval_num += 1
            # once we are done capturing the target amount of frames, exit
            if interval_num > num_shots:
                break
            currentframe += 1
        else:
            break
      
    # Release all space and windows once done
    vid.release()
    cv2.destroyAllWindows()
    return(label_dict, topic_dict)

def detect_labels(path, label_dict):
    """Detects labels in the file."""
    from google.cloud import vision
    import io
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.label_detection(image=image)
    labels = response.label_annotations
    
    for label in labels:
        label_key = label.description
        if label_key not in label_dict:
            label_dict[label_key] = 0
        else:
            label_dict[label_key] = label_dict.get(label_key, 0) + 1

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
    return label_dict


def detect_safe_search(path, topic_dict):
    """Detects unsafe features in the file."""
    from google.cloud import vision
    import io
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.safe_search_detection(image=image)
    safe = response.safe_search_annotation

    # Names of likelihood from google.cloud.vision.enums
    likelihood_name = {'UNKNOWN':0, 'VERY_UNLIKELY':1, 'UNLIKELY':2, 'POSSIBLE':3,
                       'LIKELY':4, 'VERY_LIKELY':5}
    
    key_list = list(likelihood_name.keys())
    val_list = list(likelihood_name.values())

    if "adult" not in topic_dict:
        topic_dict["adult"] = key_list[val_list.index(safe.adult)]
    elif likelihood_name.get(topic_dict.get("adult")) < val_list.index(safe.adult):
        topic_dict["adult"] = key_list[val_list.index(safe.adult)]
    
    if "violence" not in topic_dict:
        topic_dict["violence"] = key_list[val_list.index(safe.violence)]
    elif likelihood_name.get(topic_dict.get("violence")) < val_list.index(safe.violence):
        topic_dict["violence"] = key_list[val_list.index(safe.violence)]

    
    if "sexual" not in topic_dict:
        topic_dict["sexual"] = key_list[val_list.index(safe.racy)]
    elif likelihood_name.get(topic_dict.get("sexual")) < val_list.index(safe.racy):
        topic_dict["sexual"] = key_list[val_list.index(safe.racy)]

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
    return topic_dict
    
if __name__ == '__main__':
    label_dict = {}
    topic_dict = {}
    label_dict, topic_dict = capture_frames(sys.argv[1], label_dict, topic_dict)
    '''detect_labels("/Users/jaipreethundal/SLOHacks/clickbait-detection-extension/vid_shots/frame2117.jpg", label_dict)
    detect_safe_search("/Users/jaipreethundal/SLOHacks/clickbait-detection-extension/vid_shots/frame2117.jpg", topic_dict)
    for y in label_dict:
        print(y, ": ", label_dict.get(y))
    for x in topic_dict:
        print(x, ": ", topic_dict.get(x))'''
    
    #This will be the nested dictionary that'll hold one dictionary which contains prevalent labels that appear in the video and one dictionary that contains different innappriate topics and how likely they are to appear in the video
    labels_and_restrictions = {}
    labels_and_restrictions["labels"] = label_dict
    labels_and_restrictions["restrictions"] = topic_dict
    print(labels_and_restrictions.keys())
    print(labels_and_restrictions.values())
