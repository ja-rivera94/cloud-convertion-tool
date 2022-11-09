
FROM python:3
RUN mkdir /backend
RUN mkdir -p /nfs/general/uploads/
WORKDIR /backend
RUN mkdir /tmp/uploads
ADD requirements.txt /backend/
RUN pip install -r requirements.txt
ADD * /backend/
EXPOSE 5000
CMD ["python", "app.py"]
