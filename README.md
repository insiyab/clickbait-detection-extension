# ClickSafe
## A Chrome Extension to Avoid Clickbait YouTube Videos

Ever opened a video out of curiosity before you realized it was clickbait? Save your time and keep your computer secure by using ClickSafe, a Chrome extension that notifies you if a YouTube video link is clickbait while attempting to satisfy your curiosity in a safe manner.

The curiosity gap is the space between what we know and what we want or even need to know. This is what folks who create click-bait titles and thumbnails leverage to get users interested in their content—they write something very appealing at first glance, but not true to the actual video content. Let us introduce Clicksafe, a Google Chrome extension that warns users of clickbait content when they do inevitably click open intriguing videos. Additionally, it gives users the choice to satisfy some of their curiosity by giving a short description of what items are actually shown in the video, as well as an explicit content rating without actually proceeding to the video site.

ClickSafe's goal is to teach everyday users of technology how to spot clickbait content. While our current project is focused on clickbait YouTube videos, which are more irksome than actually dangerous, users that open links to clickbait articles can inadvertently install malicious software on their machines. Our next task is to extend ClickSafe so that it can work on all major social media sites, like Facebook, Twitter, Instagram and TikTok.

To try out this project for yourself, follow the instructions below in a bash shell command line:
(Note that you'll need a Google Cloud API - visit your [console](https://console.cloud.google.com/) to download it as a JSON file)

```
# Navigate to an empty directory
git clone https://github.com/insiyab/clickbait-detection-extension.git

# Download and copy your Google Cloud API JSON file into the directory
cp <api-file>.json clickbait-detect-extension/cloud-api.json

# Navigate inside the cloned directory and make the backend
make backend

# We're still working on the frontend, so you'll have to wait for the next steps!
```

### Inspirations

Our team wanted to build something to combat clickbait for ordinary Internet users while also teaching them how to spot and avoid clickbait titles.

### What Does ClickSafe Do?

Clicksafe is a Google Chrome extension that warns users of clickbait content when they do inevitably click open intriguing videos. It does this by a popup window that says "This looks like it may be clickbait!" and gives the user options to go back or proceed to the accessed page. By clicking a third option, "What's in the video?", the user can see what items were seen in the video or heard in the audio, kind of like video tags. The user can also get a rating on the explicit content in the video, from very explicit to none at all.

### How We Built It

Clicksafe leverages this [YouTube Clickbait Detector](https://github.com/alessiovierti/youtube-clickbait-detector) by [alessiovierti](https://github.com/alessiovierti) as well as the Google Cloud APIs for [Video Intelligence](https://cloud.google.com/video-intelligence/docs), [Vision](https://cloud.google.com/vision/docs), and [Natural Language Processing](https://cloud.google.com/natural-language/docs). We also built a lightweight Flask application

### Challenges

We'll answer that question when we get closer to finishing!

### Accomplishments

We'll answer that question when we get closer to finishing!
