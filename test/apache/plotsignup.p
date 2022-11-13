set terminal png size 600
set output "reporte_signup.png"
set title "1000 peticiones, 40 peticiones concurrentes"
set size ratio 0.6
set grid y
set xlabel "Nro Peticiones"
set ylabel "Tiempo de respuesta (ms)"
plot "signup.csv" using 9 smooth sbezier with lines title "GCP"