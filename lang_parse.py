# export GOOGLE_APPLICATION_CREDENTIALS="/Users/insiya/Desktop/lang_api.json"

import sys

# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
# Instantiates a client
client = language.LanguageServiceClient()
def get_wiki_url(text):
    document = language.types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT,
    )
    response = client.analyze_sentiment(
        document=document,
        encoding_type='UTF32',
    )

    print(response.document_sentiment)

if __name__ == '__main__':
	get_wiki_url(sys.argv[1])


