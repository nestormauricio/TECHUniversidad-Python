import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters('localhost')
)
channel = connection.channel()

channel.exchange_declare(exchange='logs_topic', exchange_type='topic')

result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

channel.queue_bind(
    exchange='logs_topic',
    queue=queue_name,
    routing_key='sistema.warning'
)

print("[WARN] Esperando warnings… CTRL+C para salir")

channel.basic_consume(
    queue=queue_name,
    on_message_callback=lambda ch, method, properties, body: print(f"[WARN] {body.decode()}"),
    auto_ack=True
)

channel.start_consuming()