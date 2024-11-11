FROM python:3.11-slim
# Директория
WORKDIR /usr/src/app
COPY requirements.txt .
COPY src/ .
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "./features.py"]