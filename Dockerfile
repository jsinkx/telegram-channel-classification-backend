FROM python:3.10-slim-buster as runner
WORKDIR /telegram-channel-classification
RUN apt-get update && apt-get install -y gcc 
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
ENV FLASK_APP=app.py
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]