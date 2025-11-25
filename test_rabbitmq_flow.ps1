# --- Variables ---
$projectDir = "C:\Proyectos\TECHUniversidad\Python"
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
$producers = @(
    "producer.py",
    "producer_logs.py",
    "producer_topic.py",
    "publisher_logs.py"
)

# --- 1. Moverse al proyecto ---
Set-Location $projectDir
Write-Host "[*] Ubicado en carpeta del proyecto: $projectDir"

# --- 2. Ejecutar todos los consumers en jobs ---
$jobs = @()
foreach ($consumer in $consumers) {
    $consumerPath = Join-Path $projectDir $consumer
    $job = Start-Job -ScriptBlock {
        param($path)
        python $path
    } -ArgumentList $consumerPath
    $jobs += $job
    Start-Sleep -Milliseconds 200
}
Write-Host "[*] Todos los consumers deberían estar corriendo ahora..."

# --- 3. Ejecutar todos los producers ---
foreach ($producer in $producers) {
    Write-Host "[*] Ejecutando $producer..."
    python (Join-Path $projectDir $producer)
    Start-Sleep -Seconds 1
}
Write-Host "[*] Todos los producers han enviado mensajes."

# --- 4. Consultar últimos 10 registros en SQLite ---
Write-Host "[*] Últimos 10 registros en SQLite:"
python -c "
import sqlite3
conn = sqlite3.connect(r'$projectDir\mensajes.db', isolation_level=None, check_same_thread=False)
cursor = conn.cursor()
cursor.execute('SELECT id,routing_key,body,timestamp FROM mensajes ORDER BY id DESC LIMIT 10')
for row in cursor.fetchall():
    print(row)
conn.close()
"

# --- 5. Consultar últimos 10 mensajes en log ---
Write-Host "[*] Últimos 10 mensajes en log:"
Get-Content "$projectDir\mensajes.log" -Tail 10

Write-Host "[*] Script de prueba completado. Presiona CTRL+C para detener los consumers si deseas."























# # --- Variables ---
# $projectDir = "C:\Proyectos\TECHUniversidad\Python"

# $consumers = @(
#     "consumer_info.py",
#     "consumer_warning.py",
#     "consumer_error.py"
# )

# $producer = "producer_logs.py"  # Producer tipo direct
# $severities = @("info", "warning", "error")
# $message = "Mensaje de prueba"

# # --- 1. Ejecutar todos los consumers en jobs separados ---
# Write-Host "[*] Iniciando consumers..."
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

# # --- 2. Ejecutar el producer para cada severidad ---
# foreach ($sev in $severities) {
#     Write-Host "[*] Ejecutando producer con severidad: $sev"
#     python (Join-Path $projectDir $producer) $sev $message
#     Start-Sleep -Seconds 1
# }

# # --- 3. Verificar últimos 10 registros en SQLite ---
# Write-Host "`n[*] Últimos 10 registros en SQLite:"
# python - <<<'import sqlite3; conn=sqlite3.connect("mensajes.db"); cursor=conn.cursor(); cursor.execute("SELECT id,routing_key,body,timestamp FROM mensajes ORDER BY id DESC LIMIT 10"); [print(row) for row in cursor.fetchall()]; conn.close()'

# # --- 4. Verificar últimos 10 mensajes en log ---
# Write-Host "`n[*] Últimos 10 mensajes en log:"
# Get-Content "$projectDir\mensajes.log" -Tail 10

# Write-Host "`n[*] Prueba completada. Presiona CTRL+C para detener los consumers si deseas."