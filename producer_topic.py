import pika
import sys

connection = pika.BlockingConnection(
    pika.ConnectionParameters('localhost')
)
channel = connection.channel()

# Declarar exchange tipo topic
channel.exchange_declare(exchange='logs_topic', exchange_type='topic')

severity = sys.argv[1] if len(sys.argv) > 1 else 'sistema.info'
message = ' '.join(sys.argv[2:]) or 'Mensaje por defecto'

# Publicamos usando una routing key dinámica
channel.basic_publish(
    exchange='logs_topic',
    routing_key=severity,
    body=message
)

print(f"[x] Enviado {severity} → {message}")

connection.close()