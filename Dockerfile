FROM python:3.12-slim



# Install Poetry
RUN pip install poetry


# Set working directory
WORKDIR /app

# Copy pyproject.toml and poetry.lock
COPY pyproject.toml poetry.lock* ./

COPY README.md .

# Install
RUN poetry install --no-root

# Copy the rest code
COPY . .

RUN poetry install
