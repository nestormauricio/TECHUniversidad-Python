import pika
import json

# Conexión a RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declaramos el exchange que estés usando (topic logs)
channel.exchange_declare(exchange='logs_topic', exchange_type='topic')

# Cola temporal exclusiva
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

# Escuchamos todo (#)
channel.queue_bind(exchange='logs_topic', queue=queue_name, routing_key='#')

print(f"[*] Esperando mensajes en {queue_name}. CTRL+C para salir")

def callback(ch, method, properties, body):
    mensaje = body.decode()
    print("\n--- NUEVO MENSAJE ---")
    print("Routing key:", method.routing_key)
    print("Raw body:", mensaje)
    
    # Intentamos parsear como JSON
    try:
        data = json.loads(mensaje)
        print("Es JSON ✅")
        print("Contenido:", json.dumps(data, indent=2))
    except json.JSONDecodeError:
        print("No es JSON ❌, es texto plano")

channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()