# export GOOGLE_APPLICATION_CREDENTIALS="/Users/insiya/Desktop/something.json"
# youtube-dl --no-check-certificate [url]

import sys

# Imports the Google Cloud client library
# from google.cloud import language
# from google.cloud.language import enums
# from google.cloud.language import types

# Imports the Google Cloud Video Client Library
from google.cloud import videointelligence
from google.cloud.videointelligence import enums

import argparse
import io

def get_labels(input):
    video_client = videointelligence.VideoIntelligenceServiceClient()
    features = [videointelligence.enums.Feature.LABEL_DETECTION]
    operation = video_client.annotate_video(input_content=input, features=features)
    print('\nProcessing video for label annotations:')

    result = operation.result(timeout=90)
    print('\nFinished processing.')

    segment_labels = result.annotation_results[0].segment_label_annotations
    for i, segment_label in enumerate(segment_labels):
        print('Video label description: {}'.format(
            segment_label.entity.description))
        for category_entity in segment_label.category_entities:
            print('\tLabel category description: {}'.format(
                category_entity.description))

        for i, segment in enumerate(segment_label.segments):
            start_time = (segment.segment.start_time_offset.seconds +
                          segment.segment.start_time_offset.nanos / 1e9)
            end_time = (segment.segment.end_time_offset.seconds +
                        segment.segment.end_time_offset.nanos / 1e9)
            positions = '{}s to {}s'.format(start_time, end_time)
            confidence = segment.confidence
            print('\tSegment {}: {}'.format(i, positions))
            print('\tConfidence: {}'.format(confidence))
        print('\n')

def track_objects(input): 
    video_client = videointelligence.VideoIntelligenceServiceClient()
    features = [videointelligence.enums.Feature.OBJECT_TRACKING]

    operation = video_client.annotate_video(
        input_content=input_content, features=features)
    print('\nProcessing video for object annotations.')

    result = operation.result(timeout=300)
    print('\nFinished processing.\n')

    # The first result is retrieved because a single video was processed.
    object_annotations = result.annotation_results[0].object_annotations

    # Get only the first annotation for demo purposes.
    object_annotation = object_annotations[0]
    print('Entity description: {}'.format(
        object_annotation.entity.description))
    if object_annotation.entity.entity_id:
        print('Entity id: {}'.format(object_annotation.entity.entity_id))

    print('Segment: {}s to {}s'.format(
        object_annotation.segment.start_time_offset.seconds +
        object_annotation.segment.start_time_offset.nanos / 1e9,
        object_annotation.segment.end_time_offset.seconds +
        object_annotation.segment.end_time_offset.nanos / 1e9))

    print('Confidence: {}'.format(object_annotation.confidence))

    # Here we print only the bounding box of the first frame in this segment
    frame = object_annotation.frames[0]
    box = frame.normalized_bounding_box
    print('Time offset of the first frame: {}s'.format(
        frame.time_offset.seconds + frame.time_offset.nanos / 1e9))
    print('Bounding box position:')
    print('\tleft  : {}'.format(box.left))
    print('\ttop   : {}'.format(box.top))
    print('\tright : {}'.format(box.right))
    print('\tbottom: {}'.format(box.bottom))
    print('\n')

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

        # The number of alternatives for each transcription is limited by
        # SpeechTranscriptionConfig.max_alternatives.
        # Each alternative is a different possible transcription
        # and has its own confidence score.
        for alternative in speech_transcription.alternatives:
            print('Alternative level information:')

            print('Transcript: {}'.format(alternative.transcript))
            print('Confidence: {}\n'.format(alternative.confidence))

            # print('Word level information:')
            # for word_info in alternative.words:
            #     word = word_info.word
            #     start_time = word_info.start_time
            #     end_time = word_info.end_time
            #     print('\t{}s - {}s: {}'.format(
            #         start_time.seconds + start_time.nanos * 1e-9,
            #         end_time.seconds + end_time.nanos * 1e-9,
            #         word))


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



