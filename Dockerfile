FROM python:3.6-alpine

WORKDIR /app/
ADD requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
ADD . /app/

COPY start.py .
COPY dopewars/ ./dopewars/
COPY tests/ ./tests/

ENTRYPOINT ["python", "start.py"]