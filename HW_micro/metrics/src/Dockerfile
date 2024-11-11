FROM python:3.11-slim
WORKDIR /usr/src/app
COPY requirements.txt .
COPY src/ .
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "./metric.py"]