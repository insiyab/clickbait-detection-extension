# Youtube Clickbait Detector

Automatically detect clickbait Youtube videos from their metadata, with a 96% F1 score.

## Testing the model

### Python script

The `predict.py` script shows an example of how the clickbait detection is done:

```
usage: predict.py [-h] --title TITLE [--views VIEWS] [--likes LIKES]
                  [--dislikes DISLIKES] [--comments COMMENTS]
```

Provide the script with the title of the video to analyze and, if known, the number of views, likes, dislikes, and comments. The script will print the model prediction: 1 if the video is probably clickbait, 0 otherwise.

#### Dependencies

* `numpy`
* `pandas`
* `pickle`
* `gensim`
* `emoji`

### Web app

Alternatively, you can test it with [this](https://youtubeclickbaitdetector.herokuapp.com) webapp.

## How does it work?

The prediction is made through the following pipeline:

1. Tokenize the title through a custom tokenizer.
2. Embed the title into a vector representation by computing the mean vector representation of the title tokens from a Word2Vec model. If no token is present in the Word2Vec model use the mean vector representation previously computed on the train set (`mean-title-embedding`).
3. If the number of views, likes, dislikes and comments are known, compute their logarithm. If any value is unknown, replace it with the mean value previously computed on the train set (`mean-log-video-views`, `mean-log-video-likes`, `mean-log-video-dislikes`, `mean-log-video-comments`).
4. Apply min-max scaling using a scaler previously trained on the train set (`min-max-scaler`).
5. Use a SVM (`svm`), previously trained on the train set, to get the prediction: 1 if the video is probably clickbait, 0 otherwise.

> You can read more on how the models have been trained in the `Youtube Clickbait Detector - Training` Jupyter Notebook.

> You can read more on how the models are actually used in the `predict.py` script.

### Tokenizer

The following code shows how a title is tokenized (transformed into a list of tokens):

```Python
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
```

### Word2Vec model

The Word2Vec model was trained on the train set and is used to get from a token it's vector representation.

Studying the variation of accuracy of the SVM model by using different parameters for the training of the Word2Vec model revealed the following points:
- The accuracy slightly decreases when the vector size increases;
- The accuracy slightly increases when the window size increases;
- The accuracy increases when the epochs number increases.

For these reasons the final hyperparameters which were chosen for the Word2Vec model were the following:

```Python
{
	"size": 25,
	"window": 20,
	"min_count": 1,
	"epochs": 30
}
```

The very small size of the vector representation (just 25 components) implicates a very small model size (only 4MB!) and then very small memory-loading and training times.

#### Why not using just the title of the video?

Since the Word2Vec model has been trained on a limited number of samples, it is possible that a title can contain unknown tokens (with respect to the Word2Vec model). For this reason, when the title of the video is completely unknown to the model, the other video metadata could potentially help the model to give a good prediction anyway.

### Logarithm computation and min-max scaling

#### Why is it computed the logarithm of the numeric values?

As it is shown below, the logarithm of the numeric parameters is generally normally distributed.

#### Why is it applied feature scaling?

The ML model used for the prediction is a SVM. SVMs assume that the data it works with is in a standard range.

## Train set

The train set is composed by more than 28 thousand samples where roughly one half are clickbait examples and the other one are non-clickbait examples.

### Where is the data from?

I hand-picked a [list of clickbait channels](https://gist.github.com/alessiovierti/99e2427ef3ea4d7cb453708220bf3018) and a [list of non-clickbait channels](https://gist.github.com/alessiovierti/eb39480a28e2de72e4ff21e39f43f131) and then obtained the video metadata of their videos (ordered by views) though the Youtube API. For each channel was used roughly the same number of videos and for the non-clickbait examples were chosen channels from a variety of categories.

You can use the already sanitized data by importing with `pickle` the `pandas` dataframes `clickbait-df`, `non-clickbait-df`. These dataframes contain also some statistical data about the channels, which is not used by the models but could potentially be used for other analysis.

The train set which was used to train the Word2Vec model, the min-max scaler, and the SVM is the couple `x-train` (features), `x-test` (label).

> You can read more on how the analysis has been done in the `Youtube Clickbait Detector - Analysis` Jupyter Notebook.

> You can analyze the datasets yourself by importing the dataframes with `pickle` and by using `pandas`.

### Distribution of the numeric data

![Views log distribution](/plots/views-distribution-log.png)

![Likes log distribution](/plots/likes-distribution-log.png)

![Dislikes log distribution](/plots/dislikes-distribution-log.png)

![Comments log distribution](/plots/comments-distribution-log.png)

> Note: when computing the logarithm null values were replaced with 0. This explains the peaks in the distributions for the 0 value (those videos didn't have any like, dislike, or comment).

### Most popular tokens in clickbait titles

![Top 30 clickbait tokens](/plots/top-30-clickbait-tokens.png)

## Accuracy of the model

The SVM model has been trained on more than 28 thousand samples and tested on more than 7 thousand samples.

#### Best parameters

```
C: 3.7
gamma: 4.1
```

#### Cross-validation F1 score

```
0.9691136727049655
```

### Performance on the test set (7200 samples)

```
Accuracy Score: 0.9676388888888889
Area Under ROC Curve: 0.9676185993394858
Classification report (on the test set):
         precision    recall  f1-score   support

      0       0.96      0.97      0.97      3620
      1       0.97      0.96      0.97      3580

avg / total       0.97      0.97      0.97      7200
```

## Authors

* **Alessio Vierti** - *Initial work*

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
