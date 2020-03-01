import sys
import json
import argparse
import io

# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
from google.cloud import language_v1
from google.cloud.language_v1 import enums
from google.cloud import videointelligence
from google.cloud.videointelligence import enums

def classify(path, verbose=True):
    """Classify the input text into categories. """
    from google.cloud import videointelligence

    video_client = videointelligence.VideoIntelligenceServiceClient()
    features = [videointelligence.enums.Feature.TEXT_DETECTION]
    video_context = videointelligence.types.VideoContext()

    with io.open(path, 'rb') as file:
        input_content = file.read()

    operation = video_client.annotate_video(
        input_content=input_content,  # the bytes of the video file
        features=features,
        video_context=video_context)

    result = operation.result(timeout=300)

    # The first result is retrieved because a single video was processed.
    annotation_result = result.annotation_results[0]

    text = ""
    for text_annotation in annotation_result.text_annotations:
        text = text + str(text_annotation.text) + " "
    print(text)

    classification_client = language.LanguageServiceClient()
    entities_client = language_v1.LanguageServiceClient()
    #encoding_type = enums.EncodingType.UTF8
    document = language.types.Document(
        content=text,
        type=language.enums.Document.Type.PLAIN_TEXT)

    categories_response = classification_client.classify_text(document)
    entities_response = entities_client.analyze_entities(document, encoding_type=language_v1.enums.EncodingType.UTF8)

    if "fuck"in text or "cunt" in text:
        prof = "R"
    elif "shit" in text or "bitch" in text:
        prof = "PG-13"
    elif "ass" in text or "damn" in text:
        prof = "PG"
    else:
        prof = "G"
    

    obj = {}
    obj['categories'] = []
    obj["entities"] = []
    obj["suggested-rating"] = prof

    categories = categories_response.categories
    i = j = 0
    for category in categories:
        if i == 5:
            break
        obj["categories"].append(category)
        i = i+1

    entities = entities_response.entities
    for entity in entities:
        if j==5:
            break
        obj["entities"].append(entity)
        j=j+1
    print(obj)



if __name__ == '__main__':
	classify(sys.argv[1])


