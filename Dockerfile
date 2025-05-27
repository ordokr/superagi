# Stage 1: Compile image
FROM python:3.10-slim-bullseye AS compile-image

WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install --no-install-recommends -y wget libpq-dev gcc g++ && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create and activate the virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy the requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Download NLTK resources
RUN python3.10 -c "import nltk; nltk.download('punkt')" && \
    python3.10 -c "import nltk; nltk.download('averaged_perceptron_tagger')"

# Copy the rest of the application
COPY . .

# Ensure scripts are executable
RUN chmod +x ./entrypoint.sh ./wait-for-it.sh ./install_tool_dependencies.sh ./entrypoint_celery.sh

# Stage 2: Build image
FROM python:3.10-slim-bullseye AS build-image

WORKDIR /app

# Install minimal system dependencies
RUN apt-get update && \
    apt-get install --no-install-recommends -y libpq-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy compiled environment, application, and NLTK data from compile-image
COPY --from=compile-image /opt/venv /opt/venv
COPY --from=compile-image /app /app
COPY --from=compile-image /root/nltk_data /root/nltk_data

# Ensure that the path is set to the virtual environment
ENV PATH="/opt/venv/bin:$PATH"

# Expose port for application to listen on
EXPOSE 8001

# Optional: Set entrypoint if needed
ENTRYPOINT ["./entrypoint.sh"]
