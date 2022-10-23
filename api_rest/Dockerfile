
FROM python:3
RUN apt update
RUN apt install ffmpeg
RUN apt install postgresql-client
RUN mkdir /backend
WORKDIR /backend
RUN mkdir /tmp/uploads
ADD requirements.txt /backend/
RUN pip install -r requirements.txt
ADD * /backend/
EXPOSE 5000
