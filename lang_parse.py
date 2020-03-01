import sys
import json

# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
from google.cloud import language_v1
from google.cloud.language_v1 import enums

def classify(text, verbose=True):
    """Classify the input text into categories. """

    classification_client = language.LanguageServiceClient()
    entities_client = language_v1.LanguageServiceClient()
    encoding_type = enums.EncodingType.UTF8
    document = language.types.Document(
        content=text,
        type=language.enums.Document.Type.PLAIN_TEXT)

    categories_response = classification_client.classify_text(document)
    entities_response = entities_client.analyze_entities(document, encoding_type=encoding_type)

    obj = {}
    obj['categories'] = []
    obj["entities"] = []

    categories = categories_response.categories
    for category in categories:
        obj["categories"].append(category)

    entities = entities_response.entities
    for entity in entities:
        obj["entities"].append(entity)
    print(obj)



if __name__ == '__main__':
	classify(sys.argv[1])


