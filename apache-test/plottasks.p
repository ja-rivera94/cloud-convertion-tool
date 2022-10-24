set terminal png size 600
set output "reporte_tasks.png"
set title "1000 peticiones, 50 peticiones concurrentes"
set size ratio 0.6
set grid y
set xlabel "Nro Peticiones"
set ylabel "Tiempo de respuesta (ms)"
plot "tasks_get.csv" using 9 smooth sbezier with lines title "maquina virtual"