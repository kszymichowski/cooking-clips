run:
	env SECRET_KEY=$(shell grep SECRET_KEY credentials.txt | cut -d '=' -f2) uvicorn cooking-clips.main:app --reload
test:
	env SECRET_KEY=$(shell grep SECRET_KEY credentials.txt | cut -d '=' -f2) pytest