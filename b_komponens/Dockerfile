FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install spyne==2.13.16 mysql-connector-python python-dotenv lxml
CMD ["python", "soap_server.py"]
