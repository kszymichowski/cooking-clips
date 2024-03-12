.PHONY: run test
run:
	env SECRET_KEY=$(grep SECRET_KEY credentials.txt | cut -d '=' -f2) uvicorn cooking_clips.main:app --reload
test:
	env SECRET_KEY=$(grep SECRET_KEY credentials.txt | cut -d '=' -f2) pytest -s