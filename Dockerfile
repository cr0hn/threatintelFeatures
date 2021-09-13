FROM python:3.8-slim
RUN apt-get -y update && apt-get -y install git && apt-get clean && \
    pip install  --disable-pip-version-check --no-cache-dir -U wheel pip gunicorn && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /usr/share/man/?? /usr/share/man/??_*

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# This token is needed to download doxion-core form GitHub
ENV APP_HOME /app
ENV PORT 8080

WORKDIR $APP_HOME

COPY ./requirements.txt /requirements.txt
RUN pip install --disable-pip-version-check --no-cache-dir -r /requirements.txt && \
    pip install --disable-pip-version-check --no-cache-dir gunicorn

COPY ./thread_intel_features /app/thread_intel_features

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
CMD exec gunicorn --bind :$PORT -w 4 --timeout 0 thread_intel_features.app:app
