import pika

# Conexión con RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declaramos la cola, igual que el productor
channel.queue_declare(queue='hello')

def callback(ch, method, properties, body):
    print(f"[x] Recibido → {body.decode()}")

channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)

print("[*] Esperando mensajes… CTRL+C para salir")
channel.start_consuming()