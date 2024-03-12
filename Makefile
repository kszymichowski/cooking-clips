run:
	. .venv/Scripts/activate && \
	export $$(grep -v '^#' ./credentials.txt | tr -d '\r' | xargs) && \
	uvicorn cooking_clips.main:app --reload
test:
	. .venv/Scripts/activate && \
	export $$(grep -v '^#' ./credentials.txt | tr -d '\r' | xargs) && \
	pytest -s

