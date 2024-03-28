FROM python:3.8-alpine3.12

WORKDIR /usr/src/app

COPY main.py .
COPY generate_hash.py .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "main.py"]

