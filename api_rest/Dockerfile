
FROM python:3
RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get install -y ffmpeg
RUN apt-get install -y postgresql-client
RUN mkdir /backend
WORKDIR /backend
RUN mkdir /tmp/uploads
ADD requirements.txt /backend/
RUN pip install -r requirements.txt
ADD * /backend/
EXPOSE 5000
