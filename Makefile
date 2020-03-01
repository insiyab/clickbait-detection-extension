API_PATH="$(HOME)/Desktop/clickbait-detector/google_api.json"

all:
	echo "make"

install:
	pip3 install --upgrade emoji numpy pandas gensim
	pip3 install -U scikit-learn==0.19.0
	pip3 install --upgrade google-cloud-videointelligence
	pip3 install --upgrade google-cloud-language
	# export GOOGLE_APPLICATION_CREDENTIALS=$(API_PATH) # doesn't work because it runs in subshell

server:
	export FLASK_APP=backend.py && flask run

clean:
	rm -rf __pycache__ .DS_store
