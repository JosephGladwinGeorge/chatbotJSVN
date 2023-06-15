FROM rasa/rasa:latest

USER root

WORKDIR /app
COPY . .


CMD [ "run","--enable-api","--cors","*","--debug" ]