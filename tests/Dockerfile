# Use the official Python image as the base image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /tests

# Copy the poetry.lock and pyproject.toml files to the container
COPY pyproject.toml poetry.lock /tests/

# Install Poetry and project dependencies
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev

# Copy the rest of the application code to the container
COPY . /tests

CMD ["pytest"]
