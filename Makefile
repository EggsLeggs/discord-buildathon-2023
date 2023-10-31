setup: src/requirements.txt
	pip install -r src/requirements.txt

dev:
	npx nodemon --watch src src/main.py