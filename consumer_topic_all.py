import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters('localhost')
)
channel = connection.channel()

channel.exchange_declare(exchange='topic_logs', exchange_type='topic')

result = channel.queue_declare('', exclusive=True)
queue_name = result.method.queue

# suscripción a todo
channel.queue_bind(exchange='topic_logs', queue=queue_name, routing_key='#')

print(" [*] Esperando TODOS los mensajes de topic_logs (#). CTRL+C para salir.")

def callback(ch, method, properties, body):
    print(f" [Topic-ALL] {method.routing_key} : {body.decode()}")

channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()