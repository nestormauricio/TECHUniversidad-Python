import pika
import sys

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost")
)

channel = connection.channel()

# 1. Declarar un exchange tipo direct
channel.exchange_declare(exchange="logs_direct", exchange_type="direct")

# 2. Tomar la severidad desde el argumento: info, warning, error
severity = sys.argv[1] if len(sys.argv) > 1 else "info"
message = " ".join(sys.argv[2:]) or "Mensaje de prueba"

# 3. Publicar en el exchange con una routing key
channel.basic_publish(
    exchange="logs_direct",
    routing_key=severity,
    body=message
)

print(f"[x] Enviado: {severity} → {message}")
connection.close()