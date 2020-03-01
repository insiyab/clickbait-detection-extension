import sys

# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types


from google.cloud import language_v1
from google.cloud.language_v1 import enums

# Instantiates a client
client = language.LanguageServiceClient()

def classify(text, verbose=True):
    """Classify the input text into categories. """

    language_client = language.LanguageServiceClient()

    document = language.types.Document(
        content=text,
        type=language.enums.Document.Type.PLAIN_TEXT)
    response = language_client.classify_text(document)
    categories = response.categories

    result = {}

    for category in categories:
        # Turn the categories into a dictionary of the form:
        #{category.name: category.confidence}, so that they can
        # be treated as a sparse vector.
        result[category.name] = category.confidence

    if verbose:
        #print(text)
        cat = []
        for category in categories:
            #print(u'=' * 20)
            cat.append(category.name)
            #print(category.name)
            #print(u'{:<16}: {}'.format('confidence', category.confidence))
        print('{\n\t"categories": [' + str(cat)[1:-1] + ']')



    client = language_v1.LanguageServiceClient()

    # text_content = 'California is a state.'

    # Available types: PLAIN_TEXT, HTML
    type_ = enums.Document.Type.PLAIN_TEXT

    # Optional. If not specified, the language is automatically detected.
    # For list of supported languages:
    # https://cloud.google.com/natural-language/docs/languages
    language2 = "en"
    document = {"content": text, "type": type_, "language": language2}

    # Available values: NONE, UTF8, UTF16, UTF32
    encoding_type = enums.EncodingType.UTF8
    subcat =[]
    response = client.analyze_entities(document, encoding_type=encoding_type)
    # Loop through entitites returned from the API
    for entity in response.entities:

        

        #print(u"Representative name for the entity: {}".format(entity.name))
        # Get entity type, e.g. PERSON, LOCATION, ADDRESS, NUMBER, et al
        #print(u"Entity type: {}".format(enums.Entity.Type(entity.type).name))
        # Get the salience score associated with the entity in the [0, 1.0] range
        #print(u"Salience score: {}".format(entity.salience))
        # Loop over the metadata associated with entity. For many known entities,
        # the metadata is a Wikipedia URL (wikipedia_url) and Knowledge Graph MID (mid).
        # Some entity types may have additional metadata, e.g. ADDRESS entities
        # may have metadata for the address street_name, postal_code, et al.
        a = b = 0
        for metadata_name, metadata_value in entity.metadata.items():
            a = metadata_name
            b = metadata_value
        if a or b:
            subcat.append((entity.name, enums.Entity.Type(entity.type).name, (a,b)))
        else:
            subcat.append((entity.name, enums.Entity.Type(entity.type).name))

        # Loop over the mentions of this entity in the input document.
        # The API currently supports proper noun mentions.
        
        #for mention in entity.mentions:
            #subcat.append((mention.text.content, enums.EntityMention.Type(mention.type).name))
            # Get the mention type, e.g. PROPER for proper noun

        
    # Get the language of the text, which will be the same as
    # the language specified in the request or, if not specified,
    # the automatically-detected language.
    print('\t"sub-categories": [' + str(subcat)[1:-1] + ']')
    #print(u"Language of the text: {}".format(response.language))

    return result



if __name__ == '__main__':
	classify(sys.argv[1])


