# pasted code from youtube-clickbait-detector (source: https://github.com/alessiovierti/youtube-clickbait-detector)

import argparse
import re
import emoji
import numpy as np
import pandas as pd
import pickle
from gensim.parsing.preprocessing import *
import os.path

######## FOR YOUTUBE CLICKBAIT DETECTION #########
# source: https://github.com/alessiovierti/youtube-clickbait-detector

# load parameters and models for youtube clickbait detection
YT_DETECTOR_PATH = "yt-detector" # directory containing models and parameters

word2vec = pickle.load(open(os.path.join(YT_DETECTOR_PATH, "word2vec"), "rb"))
mean_title_embedding = pickle.load(open(os.path.join(YT_DETECTOR_PATH, "mean-title-embedding"), "rb"))
min_max_scaler = pickle.load(open(os.path.join(YT_DETECTOR_PATH, "min-max-scaler"), "rb"))
svm = pickle.load(open(os.path.join(YT_DETECTOR_PATH, "svm"), "rb"))

mean_log_video_views = pickle.load(open(os.path.join(YT_DETECTOR_PATH, "mean-log-video-views"), "rb"))
mean_log_video_likes = pickle.load(open(os.path.join(YT_DETECTOR_PATH, "mean-log-video-likes"), "rb"))
mean_log_video_dislikes = pickle.load(open(os.path.join(YT_DETECTOR_PATH, "mean-log-video-dislikes"), "rb"))
mean_log_video_comments = pickle.load(open(os.path.join(YT_DETECTOR_PATH, "mean-log-video-comments"), "rb"))

def tokenize(string):

    """ Tokenizes a string.

    Adds a space between numbers and letters, removes punctuation, repeated whitespaces, words
    shorter than 2 characters, and stop-words. Returns a list of stems and, eventually, emojis.

    @param string: String to tokenize.
    @return: A list of stems and emojis.
    """

    # Based on the Ranks NL (Google) stopwords list, but "how" and "will" are not stripped, and
    # words shorter than 2 characters are not checked (since they are stripped):
    stop_words = [
        "about", "an", "are", "as", "at", "be", "by", "com", "for", "from", "in", "is", "it", "of",
        "on", "or", "that", "the", "this", "to", "was", "what", "when", "where", "who", "with",
        "the", "www"
    ]

    string = strip_short(
        strip_multiple_whitespaces(
            strip_punctuation(
                split_alphanum(string))),
        minsize=2)
    # Parse emojis:
    emojis = [c for c in string if c in emoji.UNICODE_EMOJI]
    # Remove every non-word character and stem each word:
    string = stem_text(re.sub(r"[^\w\s,]", "", string))
    # List of stems and emojis:
    tokens = string.split() + emojis

    for stop_word in stop_words:
        try:
            tokens.remove(stop_word)
        except:
            pass

    return tokens


def average_embedding(tokens, word2vec, na_vector=None):

    """ Embeds a title with the average representation of its tokens.

    Returns the mean vector representation of the tokens representations. When no token is in the
    Word2Vec model, it can be provided a vector to use instead (for example the mean vector
    representation of the train set titles).

    @param tokens: List of tokens to embed.
    @param word2vec: Word2Vec model.
    @param na_vector: Vector representation to use when no token is in the Word2Vec model.
    @return: A vector representation for the token list.
    """

    vectors = list()
    for token in tokens:
        if token in word2vec:
            vectors.append(word2vec[token])
    if len(vectors) == 0 and na_vector is not None:
        vectors.append(na_vector)
    return np.mean(np.array(vectors), axis=0)

def youtube_predictor(title, views=None, likes=None, dislikes=None, comments=None):

    input = {
        "video_title": title,
        "video_views": views if views is not None else np.NaN,
        "video_likes": likes if likes is not None else np.NaN,
        "video_dislikes": dislikes if dislikes is not None else np.NaN,
        "video_comments": comments if comments is not None else np.NaN,
    }

    sample = pd.DataFrame([ input ])

    # Tokenize the title and then compute its embedding:
    sample["video_title"] = sample["video_title"].apply(tokenize)
    sample["video_title"] = sample["video_title"].apply(
        average_embedding, word2vec=word2vec, na_vector=mean_title_embedding)
    sample = pd.concat(
        [
            sample[["video_views", "video_likes", "video_dislikes", "video_comments"]],
            sample["video_title"].apply(pd.Series)
        ], axis=1)

    # Compute the log of the video metadata or replace the missing values with the mean values obtained
    # from the train set (done previously):
    # mean_log_video_views = pickle.load(open("mean-log-video-views", "rb"))
    # mean_log_video_likes = pickle.load(open("mean-log-video-likes", "rb"))
    # mean_log_video_dislikes = pickle.load(open("mean-log-video-dislikes", "rb"))
    # mean_log_video_comments = pickle.load(open("mean-log-video-comments", "rb"))

    sample[["video_views", "video_likes", "video_dislikes", "video_comments"]] = \
        sample[["video_views", "video_likes", "video_dislikes", "video_comments"]].apply(np.log)

    if sample["video_views"].isnull().any():
        sample["video_views"].fillna(mean_log_video_views, inplace=True)
    if sample["video_likes"].isnull().any():
        sample["video_likes"].fillna(mean_log_video_likes, inplace=True)
    if sample["video_dislikes"].isnull().any():
        sample["video_dislikes"].fillna(mean_log_video_dislikes, inplace=True)
    if sample["video_comments"].isnull().any():
        sample["video_comments"].fillna(mean_log_video_comments, inplace=True)

    # Replace any -Inf value with 0:
    sample = sample.replace(-np.inf, 0)

    # Import the min-max scaler (done previously) and apply it to the sample:
    # min_max_scaler = pickle.load(open("min-max-scaler", "rb"))
    sample = pd.DataFrame(min_max_scaler.transform(sample), columns=sample.columns)

    # Import the SVM model (done previously):
    # svm = pickle.load(open("svm", "rb"))

    # Print its prediction:
    return (svm.predict(sample)[0])


# set production mode to 0 to use command line arguments, 1 to use the chrome extension
production_mode = 0

if not production_mode:
    if __name__ == '__main__':
        parser = argparse.ArgumentParser(description="Predict if a Youtube video is clickbait or not.")
        parser.add_argument(
            "--title", "-t",
            type=str, help="Title.", required=True)
        parser.add_argument(
            "--views", "-v",
            type=int, help="Number of views.", required=False)
        parser.add_argument(
            "--likes", "-l",
            type=int, help="Number of likes.", required=False)
        parser.add_argument(
            "--dislikes", "-d",
            type=int, help="Number of dislikes.", required=False)
        parser.add_argument(
            "--comments", "-c",
            type=int, help="Number of comments.", required=False)
        args = parser.parse_args()

    print(youtube_predictor(args.title, args.views, args.likes, args.dislikes, args.dislikes))

else:
    print("in production mode...")
