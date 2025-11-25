import pika
import sys

# Conexión a RabbitMQ
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost")
)
channel = connection.channel()

# Declaramos el mismo exchange usado por los consumers
channel.exchange_declare(exchange="logs_direct", exchange_type="direct")

# Obtenemos la severidad desde línea de comandos
# Ejemplo: python publisher_logs.py error "Algo salió mal"
severity = sys.argv[1] if len(sys.argv) > 1 else "info"
message = " ".join(sys.argv[2:]) or "Mensaje por defecto"

channel.basic_publish(
    exchange="logs_direct",
    routing_key=severity,
    body=message.encode()
)

print(f"[x] Enviado '{message}' con severity '{severity}'")

connection.close()