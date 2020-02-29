API_PATH="$(HOME)/Desktop/clickbait-detector/google_api.json"

all:
	echo "make"

install:
	pip3 install --upgrade emoji numpy pandas gensim
	pip3 install --upgrade google-cloud-videointelligence
	pip3 install --upgrade google-cloud-language
	# export GOOGLE_APPLICATION_CREDENTIALS=$(API_PATH) # doesn't work because it runs in subshell

# ideally want to make run a version which requires a link or video title from a user
# mainly for demo purposes

demo:
	@read -p "Enter Module Name:" module; \
  file=$(module); \
	touch $(file)
