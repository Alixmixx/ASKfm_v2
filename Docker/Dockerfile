# Use Alpine Linux with Python 3 installed
FROM python:3.8-alpine3.12

WORKDIR /usr/src/app

COPY main.py .
COPY generate_hash.py .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Command to run on container start (modify as per your script's entry point)
CMD [ "/bin/sh" ]
