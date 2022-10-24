# cloud-convertion-tool

## Instalación

Para ejecutar el proyecto localmente, es necesario instalar [Oracle VirtualBox](https://www.virtualbox.org/wiki/Downloads) en su pc. Una vez instalado, se debe descargar la imagen de la máquina virtual ([MISW4202-FotoAlpes-Microservicios.zip](https://uniandes-my.sharepoint.com/:u:/g/personal/ci_cortesg_uniandes_edu_co/EQMbaoWx1yZOl5cMyrQ-8rgBqzCjd4HWqfLmfYs1vbWFZQ?e=16NHt7)) e importarla en Virtualbox. Para importar la imagen se deben seguir los siguientes pasos:

1. Descargar el archivo mv.zip

2. Descomprimir el archivo descargado en el paso anterior

3. Abrir Oracle Virtualbox e ir al menú Máquina --> Añadir

   <img src="https://github.com/ja-rivera94/cloud-convertion-tool/wiki/image/Agregar_VM.png" alt="Agregar_VM" style="zoom:75%;" />

4. Ubicar la carpeta donde se descomprimió el archivo zip y seleccionar el archivo MISW4202-FotoAlpes-Microservicios-New.ovdx

   <img src="https://github.com/ja-rivera94/cloud-convertion-tool/wiki/image/Seleccionar_Archivo_VM.png" alt="Seleccionar_Archivo_VM" style="zoom:75%;" />

5. En el menú izquierdo debe aparecer la máquina con el nombre del archivo seleccionado

6.  Dar clic en el botón Iniciar ubicado en la parte superior

   <img src="https://github.com/ja-rivera94/cloud-convertion-tool/wiki/image/Iniciar_VM.png" alt="Iniciar_VM" style="zoom:75%;" />

16. Una vez la máquina termine de cargar, debe visualizar la pantalla de inicio

17. Ingresar con el usuario **estudiante** y la contraseña **Estudiante2021**


18. Ubíquese en el directorio cloud-convertion-tool ejecutando el siguiente comando:

   ```
   cd cloud/cloud-convertion-tool
   ```

20. Para ejecutar los servicios, corra el siguiente comando:

    ```
    sudo docker-compose up -d
    ```

## Pruebas

Una vez los servicios se estén ejecutando podemos hacer pruebas de las funciones expuestas por estos. El ejemplo no implementa una interfaz de usuario por lo que debemos utilizar un programa que permita consumir servicios REST. Se sugiere utilizar [Postman](https://www.postman.com/downloads/) para ejecutar los servicios del ejemplo, por lo que debe descargarlo haciendo clic sobre el enlace anterior.

Para consumir alguno de los servicios implementados, importe la siguiente Collection:

<a href="https://github.com/ja-rivera94/cloud-convertion-tool/wiki/image/api-rest.postman_collection.json"> </a>


