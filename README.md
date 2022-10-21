# cloud-convertion-tool 

## Instalación

Los servicios de este proyecto requieren de *flask*, *docker* y *docker-compose*. Se debe clonar este repositorio y, en caso de usar Linux Ubuntu ejecutar el archivo install.sh para instalar las librerías y los servicios. Después de ejecutar el archivo se debe reiniciar la máquina virtual. Si usa un sistema operativo distinto, debe instalar las librerías requeridas de manera manual.

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

## POST METHOD ENDPOINT CREATE TEASK
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

