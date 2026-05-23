FROM python:3.11-slim

WORKDIR /app

RUN pip install requests prometheus-client

COPY app.py .

EXPOSE 8000

CMD ["python", "-u", "app.py"]