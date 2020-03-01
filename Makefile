API_PATH="$(HOME)/Desktop/clickbait-detector/cloud_api.json"

all: backend

backend: install server

install:
	pip3 install --upgrade flask emoji numpy pandas gensim
	pip3 install -U scikit-learn==0.19.0
	pip3 install --upgrade google-cloud-videointelligence
	pip3 install --upgrade google-cloud-language
	pip3 install --upgrade google-cloud-vision

server:
	export GOOGLE_APPLICATION_CREDENTIALS=$(API_PATH) && \
		export FLASK_APP=backend.py && flask run

clean:
	rm -rf __pycache__ .DS_store
