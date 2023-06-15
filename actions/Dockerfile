FROM rasa/rasa-sdk:3.5.1

WORKDIR /app 
USER root
RUN python -m pip install --upgrade pip
# RUN pip install recognizers-text-suite
COPY .  /app/actions

WORKDIR /app/actions
RUN pip install -r requirements.txt
WORKDIR /app
USER 1000

EXPOSE 5055


