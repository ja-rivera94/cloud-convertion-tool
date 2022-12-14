#!/bin/bash
set -e
set -u

declare -a arr_task=()
declare -a arr=("element1" "element2" "element3")

arr_user=()
arr_file_input=()
arr_file_output=()

PSQL=/usr/bin/psql

DB_USER=test
DB_HOST=10.127.0.3
DB_NAME=test
DB_PASSWORD=test


index=0
mapfile result < <(PGPASSWORD=test $PSQL -X -h $DB_HOST -U $DB_USER -c "select t.id_task, t.username, t.filename_input, t.filename_output, u.email from task as t , public.user as u where t.username::text = u.id::text  and status = 'uploaded' " $DB_NAME )

for row in "${result[@]}";do
    echo  $row
    echo "-------"
    
    IFS='|' read -ra ADDR <<< "$row"
    index=0
    for i in "${ADDR[@]}"; do 
        i=`echo $i | sed 's/ *$//g'`
        if [ $index -eq 0 ]
        then
            id_task=$i
        elif [ $index -eq 1 ]
        then
            id_user=$i
        elif [ $index -eq 2 ]
        then
            input_file=$i
        elif [ $index -eq 3 ]
        then
            output_file=$i
        elif [ $index -eq 4 ]
        then
            email=$i
        fi
        ((index=index+1))
    done
    
    re='^[0-9]+$'
    if ! [[ $id_task =~ $re ]] ; 
    then
        echo "error: Not a number" >&2; 
    else
        echo "update task set status='processed' where id_task='$id_task'"
        gcloud auth activate-service-account --key-file /app/cloud-convertion-tool/api_rest/storage.json
        gsutil cp "gs://cloud-convertion-tool-audio/archivos/originales/$input_file" "/tmp/$input_file"
        ffmpeg -i "/tmp/$input_file" "/tmp/$output_file" || true
        gsutil cp "/tmp/$output_file" "gs://cloud-convertion-tool-audio/archivos/procesados/$output_file"
        rm "/tmp/$input_file"
        rm "/tmp/$output_file"        
        PGPASSWORD=test $PSQL -X -h $DB_HOST -U $DB_USER -c "update task set status='processed' where id_task='$id_task'" || true
        python3 /app/cloud-convertion-tool/api_rest/SendMail_API.py "Task processed"
    fi

done
