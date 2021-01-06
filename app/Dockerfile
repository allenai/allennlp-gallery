FROM python:3.8.6

# Setup a spot for the app code
WORKDIR /usr/local/src/skiff/app

# Install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy over the source code
COPY app app/
COPY start.py .

# This enables the Flask debugger and activates code that restarts the
# API as you make changes
ARG FLASK_ENV=development
ENV FLASK_ENV $FLASK_ENV

# Kick things off
ENTRYPOINT [ "python" ]
CMD [ "start.py" ]
