# Carpeta del proyecto
$projectDir = "C:\Proyectos\TECHUniversidad\Python"

# Lista de consumers
$consumers = @(
    "consumer.py",
    "consumer_all.py",
    "consumer_error.py",
    "consumer_info.py",
    "consumer_topic_all.py",
    "consumer_topic_app.py",
    "consumer_topic_errors.py",
    "consumer_warning.py"
)

# Iniciar cada consumer en un job separado
$jobs = @()
foreach ($consumer in $consumers) {
    $consumerPath = Join-Path $projectDir $consumer
    $job = Start-Job -ScriptBlock {
        param($path)
        python $path
    } -ArgumentList $consumerPath
    $jobs += $job
    Start-Sleep -Milliseconds 200  # pequeño delay para no saturar
}

Write-Host "[*] Todos los consumers deberían estar corriendo ahora..."

# Lista de producers
$producers = @(
    "producer.py",
    "producer_logs.py",
    "producer_topic.py",
    "publisher_logs.py"
)

# Ejecutar cada producer 3 veces (para pruebas)
foreach ($i in 1..3) {
    foreach ($producer in $producers) {
        Write-Host "[*] Ejecutando $producer (ciclo $i)..."
        python (Join-Path $projectDir $producer)
        Start-Sleep -Milliseconds 500
    }
}

Write-Host "[*] Todos los producers han enviado mensajes."

# Consultar SQLite y log de forma segura
$pythonCheck = @"
import sqlite3
import os

DB_FILE = r'$projectDir\mensajes.db'
LOG_FILE = r'$projectDir\mensajes.log'

print('\n[*] Últimos 10 registros en SQLite:')
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()
cursor.execute('SELECT id, routing_key, body, timestamp FROM mensajes ORDER BY id DESC LIMIT 10')
rows = cursor.fetchall()
for row in rows:
    print(row)
conn.close()

print('\n[*] Últimos 10 mensajes en log:')
if os.path.exists(LOG_FILE):
    with open(LOG_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines[-10:]:
            print(line.strip())
else:
    print('No existe el log')
"@

# Guardar y ejecutar el script Python de verificación
$checkFile = Join-Path $projectDir "check_db.py"
$pythonCheck | Out-File -FilePath $checkFile -Encoding UTF8
python $checkFile
Remove-Item $checkFile

Write-Host "`n[*] Prueba completada. Presiona CTRL+C para detener los consumers si quieres."

























# # Carpeta del proyecto
# $projectDir = "C:\Proyectos\TECHUniversidad\Python"

# # Lista de consumers
# $consumers = @(
#     "consumer.py",
#     "consumer_all.py",
#     "consumer_error.py",
#     "consumer_info.py",
#     "consumer_topic_all.py",
#     "consumer_topic_app.py",
#     "consumer_topic_errors.py",
#     "consumer_warning.py"
# )

# # Lista de producers
# $producers = @(
#     "producer.py",
#     "producer_logs.py",
#     "producer_topic.py",
#     "publisher_logs.py"
# )

# # Iniciar consumers en jobs separados
# $jobs = @()
# foreach ($consumer in $consumers) {
#     $consumerPath = Join-Path $projectDir $consumer
#     $job = Start-Job -ScriptBlock {
#         param($path)
#         python $path
#     } -ArgumentList $consumerPath
#     $jobs += $job
#     Start-Sleep -Milliseconds 200
# }

# Write-Host "[*] Todos los consumers deberían estar corriendo ahora..."

# # Ejecutar producers uno por uno
# foreach ($producer in $producers) {
#     Write-Host "[*] Ejecutando $producer..."
#     python (Join-Path $projectDir $producer)
#     Start-Sleep -Seconds 1
# }

# Write-Host "[*] Todos los producers han enviado mensajes."

# # Esperar a que los consumers procesen
# Start-Sleep -Seconds 3

# # Mostrar últimos 10 mensajes del log
# $logFile = Join-Path $projectDir "mensajes.log"
# Write-Host "`n[*] Últimos 10 mensajes en log ($logFile):"
# Get-Content $logFile -Tail 10

# # Mostrar últimos 10 registros en la DB SQLite
# Write-Host "`n[*] Últimos 10 registros en SQLite (mensajes.db):"
# $pythonCheck = @"
# import sqlite3
# conn = sqlite3.connect(r'$projectDir\mensajes.db')
# cursor = conn.cursor()
# cursor.execute('SELECT id, routing_key, body, timestamp FROM mensajes ORDER BY id DESC LIMIT 10')
# rows = cursor.fetchall()
# for row in reversed(rows):
#     print(row)
# conn.close()
# "@

# python -Command $pythonCheck

# Write-Host "`n[*] Prueba completada. Presiona CTRL+C para detener los consumers si quieres."