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
DB_HOST=postgres
DB_NAME=test
DB_PASSWORD=test


index=0
mapfile result < <(PGPASSWORD=test $PSQL -X -h $DB_HOST -U $DB_USER -c "select t.id_task, t.username, t.filename_input, t.filename_output, u.email from task as t , public.user as u where t.username::text = u.id::text  and status = 'uploaded' " $DB_NAME )

echo ${result[0]%$'\t'*}
echo ${result[0]#*$'\t'}

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
    
    echo 'ffmpeg -i /tmp/uploads/'$input_file' /tmp/uploads/'$output_file''
    echo "update task set status='processed' where id_task='$id_task'"
    ffmpeg -i "/tmp/uploads/$input_file" "/tmp/uploads/$output_file" || true
    PGPASSWORD=test $PSQL -X -h $DB_HOST -U $DB_USER -c "update task set status='processed' where id_task='$id_task';" || true
done