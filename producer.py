import pika
import sys

# Conexión con RabbitMQ en localhost
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declaramos la cola (si ya existe, no pasa nada)
channel.queue_declare(queue='hello')

# Mensaje desde argumentos o por defecto
message = ' '.join(sys.argv[1:]) or "Hello RabbitMQ!"

channel.basic_publish(
    exchange='',
    routing_key='hello',
    body=message
)

print(f"[x] Enviado → {message}")

connection.close()