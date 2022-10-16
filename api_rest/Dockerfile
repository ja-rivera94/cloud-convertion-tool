FROM python:3
RUN mkdir /usr/src/app/
COPY . /usr/src/app/
WORKDIR /usr/src/app/
ADD requirements.txt /usr/src/app/
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "app.py"]
