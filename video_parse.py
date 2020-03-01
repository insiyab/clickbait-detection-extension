# sample file that goes through how to get an audio transcription of a video

# export GOOGLE_APPLICATION_CREDENTIALS="/Users/insiya/Desktop/something.json"
# youtube-dl --no-check-certificate [url]

import sys

# Imports the Google Cloud Video Client Library
from google.cloud import videointelligence
from google.cloud.videointelligence import enums

import argparse
import io

def get_transcription(input):
    video_client = videointelligence.VideoIntelligenceServiceClient()
    features = [videointelligence.enums.Feature.SPEECH_TRANSCRIPTION]

    config = videointelligence.types.SpeechTranscriptionConfig(
        language_code='en-US',
        enable_automatic_punctuation=True)
    video_context = videointelligence.types.VideoContext(
        speech_transcription_config=config)

    operation = video_client.annotate_video(
        input_content=input, features=features,
        video_context=video_context)

    print('\nProcessing video for speech transcription.')

    result = operation.result(timeout=600)

    # There is only one annotation_result since only
    # one video is processed.
    annotation_results = result.annotation_results[0]
    for speech_transcription in annotation_results.speech_transcriptions:

        for alternative in speech_transcription.alternatives:
            print('Alternative level information:')

            print('Transcript: {}'.format(alternative.transcript))
            print('Confidence: {}\n'.format(alternative.confidence))

if __name__ == '__main__':
    # parser = argparse.ArgumentParser(
    #     description=__doc__,
    #     formatter_class=argparse.RawDescriptionHelpFormatter)
    # parser.add_argument('path', help='GCS file path for label detection.')
    # args = parser.parse_args()

    path = sys.argv[1]
    with io.open(path, 'rb') as movie:
        input_content = movie.read()

    # get_labels(input_content)
    # track_objects(input_content)
    get_transcription(input_content)
