import logging
from concurrent import futures
import os
import subprocess
import psycopg2
import sqlite3
import json
from google.cloud import storage
from google.cloud import pubsub_v1
from pydub import AudioSegment
from os import remove
from os import path

logging.basicConfig(level=logging.INFO)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]= 'storage.json'
project_id = "cloud-convertion-tool"
subscription_id = "cloud-convertion-tool-sub"
subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_id)

def get_connection():
    # connection = psycopg2.connect(user="test", password="test", host="10.127.0.3", port="5432", database="test")
    connection = sqlite3.connect('D:\\Personal\\MISO\\Onedrive\\OneDrive - Universidad de los Andes\\Trimestre 5\\cloud\\Proyecto\\cloud-convertion-tool\\api_rest\\instance\\data.db')
    return connection

def close_connection(connection):
    if connection:
        connection.close()
        print("Postgres connection is closed")
        
    
def convertidor(origen,destino):
    extension = os.path.basename(origen)
    extDestino = os.path.basename(destino)
    
    if extension.endswith('.wav'):
        song = AudioSegment.from_wav(origen)
        if extDestino.endswith('.ogg'):
            song.export(destino, format="ogg")
        elif extension.endswith('.mp3'):
            song.export(destino, format="mp3")
            
    elif extension.endswith('.mp3'):
        song = AudioSegment.from_mp3(origen)
        if extDestino.endswith('.ogg'):
            song.export(destino, format="ogg")
        elif extension.endswith('.wav'):
            song.export(destino, format="wav")
            
    elif extension.endswith('.ogg'):
        song = AudioSegment.from_ogg(origen)
        if extDestino.endswith('.mp3'):
            song.export(destino, format="mp3")
        elif extension.endswith('.wav'):
            song.export(destino, format="wav")
            
            

def download_blob( source_blob_name, destination_file_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket('cloud-convertion-tool-audio')
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)
    
def upload_blob( source_file_name, destination_blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket('cloud-convertion-tool-audio')
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)
        
    
def procesa_tarea(tarea):
    try:
        print(tarea)  
        y = json.loads(tarea) 
        llave= y["uuid"]
        miconexion = get_connection()
        cursor = miconexion.cursor()
        t = (llave,)
        #select_query = """select t.id_task, t.username, t.filename_input, t.filename_output, u.email,t.status from task as t , public.user as u where t.username::text = u.id::text  and status <> 'uploaded' and  t.id_task::text <> %s"""
        select_query = """select t.id_task, t.username, t.filename_input, t.filename_output, u.email,t.status from task as t , user as u where t.username = u.id  and status = 'uploaded' and  t.id_task = ?"""
        cursor.execute(select_query, t)
        row = cursor.fetchone()
        if row is not None:
            print("----------------Printing record--------------")
            print("id_task:", row[0], )
            print("username Name:", row[1])
            print("filename_input:", row[2])
            print("filename_output:", row[3])
            print("email:", row[4])
            print("status",row[5])
            download_blob( "archivos/originales/"+row[2] ,row[2] )
            #convertidor(row[2] , row[3])
            #upload_blob( row[3],"archivos/procesados/"+row[3] )
            upload_blob( row[2],"archivos/procesados/"+row[3] )
            
            if path.exists(row[2]):
                remove(row[2])
                
            #if path.exists(row[3]):    
            #   remove(row[3])
            update_query = """update task set status='processed' where id_task= ?"""
            cursor.execute(update_query, t)
            miconexion.commit()
            cursor.close()
            print("Record Updated successfully ")
        close_connection(miconexion)
    #except (Exception, psycopg2.Error) as error:
    except (Exception, sqlite3.Error) as error:
        print("Error trayendo datos. ", error)
    finally:
        if miconexion:
            miconexion.close()
            print("The SQLite connection is closed")
     
    
    
def callback(message):
    print("Received message: {}".format(message.data))
    procesa_tarea(str(message.data.decode("utf-8")))
    message.ack()
    
    
    
future = subscriber.subscribe(subscription_path, callback=callback)
with subscriber:
    try:
        future.result()
    except KeyboardInterrupt:
        future.cancel()  # Trigger the shutdown.
        
