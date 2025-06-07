FROM python:3.12-slim



# Install Poetry and export path explicitly
RUN pip install poetry

## Set environment variables for Poetry path in future layers
#ENV PATH="/root/.local/bin:$PATH"

# Set working directory
WORKDIR /app

# Copy pyproject.toml and poetry.lock (if available)
COPY pyproject.toml poetry.lock* ./

COPY README.md .

# Install
RUN poetry install --no-root

# Copy the rest of your code
COPY . .

RUN poetry install
