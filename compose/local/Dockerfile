# Alias for the specific Python version
FROM python:3.11.6-slim-bookworm as python

# Build stage
FROM python as python-build-stage

# Install apt packages
RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential

# Copy requirements
COPY ./requirements.dev.txt .

# Create Python dependency wheels.
RUN pip wheel --wheel-dir /wheels \
    -r requirements.dev.txt

# Run stage
FROM python as python-run-stage

# Set env variables
ENV APP_HOME /app
ENV PORT 8000
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Expose default port
EXPOSE $PORT

# Set working directory
WORKDIR $APP_HOME

# Update and clean-up apt packages
RUN apt-get update && apt-get install --no-install-recommends -y \
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

# Copy dependency wheels from the build stage
COPY --from=python-build-stage /wheels /wheels/

# Install Python dependencies
RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
  && rm -rf /wheels/

# Set start script
COPY ./compose/local/start.sh $APP_HOME/start.sh
RUN sed -i 's/\r$//g' $APP_HOME/start.sh
RUN chmod +x $APP_HOME/start.sh

# Copy application code
COPY ./moodzify/ $APP_HOME/

# Set entrypoint for the container
ENTRYPOINT ["./start.sh"]