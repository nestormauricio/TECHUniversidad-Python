import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters('localhost')
)
channel = connection.channel()

channel.exchange_declare(exchange='topic_logs', exchange_type='topic')

result = channel.queue_declare('', exclusive=True)
queue_name = result.method.queue

# solo mensajes que empiecen por "app."
channel.queue_bind(exchange='topic_logs', queue=queue_name, routing_key='app.*')

print(" [*] Escuchando mensajes APP (app.*). CTRL+C para salir.")

def callback(ch, method, properties, body):
    print(f" [APP] {method.routing_key} : {body.decode()}")

channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()