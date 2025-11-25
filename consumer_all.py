import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters("localhost")
)
channel = connection.channel()

# Exchange topic
channel.exchange_declare(exchange="logs_topic", exchange_type="topic")

# Cola exclusiva temporal (solo debe quedarse mientras esté el consumidor vivo)
result = channel.queue_declare(queue="", exclusive=True)
queue_name = result.method.queue

# Bind: el consumidor escucha TODO lo que llegue al exchange
channel.queue_bind(exchange="logs_topic", queue=queue_name, routing_key="#")

print(f"[*] Esperando mensajes en {queue_name}. Para salir presiona CTRL+C")

def callback(ch, method, properties, body):
    print(f"[x] Recibido ({method.routing_key}): {body.decode()}")

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

# # Declarar el exchange que ya existe
# channel.exchange_declare(exchange="logs_direct", exchange_type="direct")

# # Crear una cola exclusiva
# result = channel.queue_declare(queue="", exclusive=True)
# queue_name = result.method.queue

# # Enlazar esta cola a TODAS las severidades
# severidades = ["info", "warning", "error"]

# for sev in severidades:
#     channel.queue_bind(
#         exchange="logs_direct",
#         queue=queue_name,
#         routing_key=sev
#     )

# print("[*] Esperando TODOS los mensajes… CTRL+C para salir")

# def callback(ch, method, properties, body):
#     print(f"[{method.routing_key.upper()}] {body.decode()}")

# channel.basic_consume(
#     queue=queue_name,
#     on_message_callback=callback,
#     auto_ack=True
# )

# channel.start_consuming()