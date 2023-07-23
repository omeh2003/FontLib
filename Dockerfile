# Using multi-stage builds
# Stage 1: build
FROM python:3.10-slim-buster as build

# Update system packages and install dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends fontforge fontforge-extras && \
    pip install -U pip wheel setuptools

# Copy python requirements file
COPY requirements.txt /tmp/

# Install python dependencies
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /tmp -r /tmp/requirements.txt

# Install other python libraries

# Stage 2: runtime
FROM python:3.10-slim-buster

COPY --from=build /usr/local /usr/local
COPY --from=build /tmp/*.whl /tmp/

RUN pip install --no-cache /tmp/*.whl && \
    rm -rf /tmp/*.whl

# Clean up
RUN apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/*

COPY ./my_generate.py /app/
WORKDIR /app/

# Run your application
CMD ["python", "./my_generate.py"]
