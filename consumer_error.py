import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost")
)
channel = connection.channel()

# Declaramos el mismo exchange
channel.exchange_declare(exchange="logs_direct", exchange_type="direct")

# Creamos una cola exclusiva para este consumer
result = channel.queue_declare(queue="", exclusive=True)
queue_name = result.method.queue

# Enlazamos la cola solo a mensajes con routing key = "error"
channel.queue_bind(
    exchange="logs_direct",
    queue=queue_name,
    routing_key="error"
)

print("[*] Esperando errores… CTRL+C para salir")

def callback(ch, method, properties, body):
    print(f"[ERROR] {body.decode()}")

channel.basic_consume(
    queue=queue_name,
    on_message_callback=callback,
    auto_ack=True
)

channel.start_consuming()



















# import pika

# connection = pika.BlockingConnection(
#     pika.ConnectionParameters(host="localhost")
# )
# channel = connection.channel()

# # Declaramos el mismo exchange
# channel.exchange_declare(exchange="logs_direct", exchange_type="direct")

# # Creamos una cola exclusiva para este consumer
# result = channel.queue_declare(queue="", exclusive=True)
# queue_name = result.method.queue

# # Enlazamos la cola solo a mensajes con routing key = "error"
# channel.queue_bind(
#     exchange="logs_direct",
#     queue=queue_name,
#     routing_key="error"
# )

# print("[*] Esperando errores… CTRL+C para salir")

# def callback(ch, method, properties, body):
#     print(f"[ERROR] {body.decode()}")

# channel.basic_consume(
#     queue=queue_name,
#     on_message_callback=callback,
#     auto_ack=True
# )

# channel.start_consuming()