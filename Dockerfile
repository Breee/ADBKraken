FROM python:3.7-alpine

# Working directory for the application
WORKDIR /usr/src/app
COPY kraken /usr/src/app

RUN apk --no-cache update && apk add gcc python3-dev linux-headers git
RUN apk --update-cache --repository http://dl-3.alpinelinux.org/alpine/edge/testing/ add android-tools

RUN cd /usr/src/app && python3 -m pip install -U -r requirements.txt

# Set Entrypoint with hard-coded options
ENTRYPOINT ["python3"]
CMD ["./start_bot.py"]

