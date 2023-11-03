dev:
	npx nodemon --watch src --exec poetry run python src/bot.py

install: poetry.lock pyproject.toml
	curl -sSL https://install.python-poetry.org | python3 -
	poetry install

build: poetry.lock pyproject.toml
	docker build -f ./docker/Dockerfile .

start: poetry.lock pyproject.toml
	docker-compose -f docker/docker-compose.yml up --build -d

start-alt: poetry.lock pyproject.toml
	docker compose -f docker/docker-compose.yml up --build -d