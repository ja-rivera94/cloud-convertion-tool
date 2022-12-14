# cloud-convertion-tool 

## Instalación

Si usted descargó la imagen de la máquina virtual para Virtual Box omita esta sección y pase a la sección Ejecución. Los servicios de este proyecto requieren de *flask*, *docker* y *docker-compose*. Se debe clonar este repositorio y, en caso de usar Linux Ubuntu ejecutar el archivo install.sh para instalar las librerías y los servicios. Después de ejecutar el archivo se debe reiniciar la máquina virtual. Si usa un sistema operativo distinto, debe instalar las librerías requeridas de manera manual.

```
sh install.sh
```

## Ejecución

Para correr la aplicación se debe ejecutar el siguiente comando:


```
docker-compose up
```

O si prefiere correr la aplicación en background se debe ejecutar el siguiente comando:

```
docker-compose up -d
```
## Descripción de los servicios

### GET METHOD ENDPOINT API STATUS
```
curl --location --request GET 'http://127.0.0.1:5000/api/status'
```

### POST METHOD ENDPOINT SIGNUP
```
curl --location --request POST 'http://127.0.0.1:5000/api/auth/signup' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username": "carlos",
    "password1": "123",
    "password2": "123",
    "email": "carlos@gmail.com"
}'
```

### POST METHOD ENDPOINT LOGIN
```
curl --location --request POST 'http://127.0.0.1:5000/api/auth/login' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username": "carlos",
    "password": "123"
}'
```

### POST METHOD ENDPOINT CREATE TEASK
```
curl --location --request POST 'http://127.0.0.1:5000/api/tasks' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY2NjM4NDY0OCwianRpIjoiYzlhMDkxMmMtZGVkYi00ZmNiLWI5MGYtMmM1MjVmZTkzOGQ4IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MTIsIm5iZiI6MTY2NjM4NDY0OCwiZXhwIjoxNjY2Mzg1NTQ4fQ.rPjBjno95bnIV07sY7pCiP5Bifm24w6d0XvYwjXszLs' \
--form 'fileName=@"/Users/jael.rivera/Documents/miso/cloud-convertion-tool/audios-test/sample4.wma"' \
--form 'newFormat="aac"'
```

### GET METHOD TO FETCH ALL TASK
```
curl --location --request GET 'http://127.0.0.1:5000/api/tasks/' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY2NjM4ODM5MywianRpIjoiMjg5YjZkY2MtNmQwMy00ZWM2LThiNjctMDFhZTIyOTE5N2MyIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MTIsIm5iZiI6MTY2NjM4ODM5MywiZXhwIjoxNjY2Mzg5MjkzfQ.eFFCIrr39Ym7Xr8Hz8_cC5m6IlxaVRrh277qLQJj08E'
```

### GET METHOD TO GET SPECIFIC TASK 

```
curl --location --request GET 'http://127.0.0.1:5000/api/tasks/116' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY2NjM4ODM5MywianRpIjoiMjg5YjZkY2MtNmQwMy00ZWM2LThiNjctMDFhZTIyOTE5N2MyIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MTIsIm5iZiI6MTY2NjM4ODM5MywiZXhwIjoxNjY2Mzg5MjkzfQ.eFFCIrr39Ym7Xr8Hz8_cC5m6IlxaVRrh277qLQJj08E'
```

### PUT METHOD TO SPECIFIC TASK 
```
curl --location --request PUT 'http://127.0.0.1:5000/api/tasks/13' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY2NjU2NjgzOCwianRpIjoiZjQ2MmUxNjktZDZhMC00ZGQyLWJjOTItMWNhODg2ZDczY2Y5IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MiwibmJmIjoxNjY2NTY2ODM4LCJleHAiOjE2NjY1Njc3Mzh9.OgRRazYWaZ5mHK6MPBSvPsX8VxinKQ33JZwRIyA5RMQ' \
--header 'Content-Type: application/json' \
--data-raw '{
    "newFormat": "aac"
}'
```

### DELETE METHOD TO SPECIFIC TASK 
```
curl --location --request DELETE 'http://127.0.0.1:5000/api/tasks/10' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY2NjU1Nzg0NSwianRpIjoiMWQ0NTAzYmItZDYyNS00NDczLWEyY2ItMzcyZDdkMDQyM2EyIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MiwibmJmIjoxNjY2NTU3ODQ1LCJleHAiOjE2NjY1NTg3NDV9.qLlMwyb1nRRol-OioHChzcU2kpmp1Z4bco2v50FwTqI'
```

### GET METHOD TO DOWNLOAD FILE
```
curl --location --request GET 'http://127.0.0.1:5000/api/files/5bf0618e-e92d-4da1-abeb-783f587f25c8-file_example_MP3_5MG.mp3.aac' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY2NjU1Nzg0NSwianRpIjoiMWQ0NTAzYmItZDYyNS00NDczLWEyY2ItMzcyZDdkMDQyM2EyIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MiwibmJmIjoxNjY2NTU3ODQ1LCJleHAiOjE2NjY1NTg3NDV9.qLlMwyb1nRRol-OioHChzcU2kpmp1Z4bco2v50FwTqI'
```

## Pruebas

Una vez los servicios se estén ejecutando podemos hacer pruebas de las funciones expuestas por estos. El ejemplo no implementa una interfaz de usuario por lo que debemos utilizar un programa que permita consumir servicios REST. Se sugiere utilizar [Postman](https://www.postman.com/downloads/) para ejecutar los servicios del ejemplo, por lo que debe descargarlo haciendo clic sobre el enlace anterior.

Para consumir alguno de los servicios implementados, importe la siguiente Collection:

[api-rest.postman_collection.json](https://github.com/ja-rivera94/cloud-convertion-tool/wiki/image/api-rest.postman_collection.json) 


## Docker ejecucion

crear la imagen 

```
docker build -t cloud-convertion-tool_api-service .
```

correr el contenedor 
```
docker run -t -d -v /nfs/general:/nfs/general -p 5000:5000 --name cloud-convertion-tool-service cloud-convertion-tool_api-service:latest
```


## configuracion job 

instalar crontab

ejecutar crontab -e y crear el siguiente job 

```
*/2 * * * * sudo /bin/bash /app/cloud-convertion-tool/api_rest/job_convert_audios.sh >> /var/logs/audios_convert 2>&1
```
