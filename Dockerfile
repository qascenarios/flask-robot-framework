FROM alpine:latest

COPY . /app
WORKDIR /app

RUN apk add --no-cache sqlite py3-pip
RUN pip install -r requirements.txt

ENV FLASK_PORT 8080
ENV FLASK_APP demo_app

CMD ["sh", "run.sh"]