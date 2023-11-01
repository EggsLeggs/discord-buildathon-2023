FROM python:3.10-slim

# Set pip to have cleaner logs and no saved cache.
ENV PIP_NO_CACHE_DIR=false \
    POETRY_VIRTUALENVS_CREATE=false

# Install Poetry
RUN pip install --upgrade poetry

WORKDIR /app

# Copy dependencies and lockfile.
COPY ../pyproject.toml ../poetry.lock ./

# Install dependencies and lockfile, excluding development dependencies.
RUN poetry install --no-dev --no-interaction

# Copy the src directory into the container.
COPY ../src/ ./src/

# Start the bot.
CMD ["poetry", "run", "python", "src/bot.py"]