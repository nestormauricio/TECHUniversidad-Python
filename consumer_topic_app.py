import pika
import sqlite3
from concurrent.futures import ThreadPoolExecutor

TIPO_CONSUMER = 'app'  # Tipo del consumer: info, warning, error, all, app
QUEUE = 'consumer_topic_app'          # Nombre de la cola
TODAS_CLAVES = ['info', 'warning', 'error']  # Routing keys que existen

def filtrar_mensaje(routing_key: str, tipo: str) -> bool:
    if tipo == "all":
        return True
    return routing_key.startswith(tipo)

def procesar_msg(msg):
    # Persistencia en SQLite
    conn = sqlite3.connect("mensajes.db", isolation_level=None, check_same_thread=False)
    conn.execute("PRAGMA journal_mode=WAL;")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO mensajes (routing_key, body, timestamp) VALUES (?, ?, datetime('now'))",
                   (msg["routing_key"], msg["body"]))
    conn.close()
    # Guardar también en log
    with open("mensajes.log", "a", encoding="utf-8") as f:
        f.write(f"{msg['routing_key']} | {msg['body']}\n")
    print(f"[x] Procesado: {{msg}}")

def callback(ch, method, properties, body):
    msg = {"routing_key": method.routing_key, "body": body.decode()}
    if filtrar_mensaje(msg["routing_key"], TIPO_CONSUMER):
        executor.submit(procesar_msg, msg)

# Conexión y canal
connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

# Declarar exchange tipo direct
channel.exchange_declare(exchange="logs_direct", exchange_type="direct")

# Declarar cola y bind al exchange
channel.queue_declare(queue=QUEUE)
if TIPO_CONSUMER == "all":
    for rk in TODAS_CLAVES:
        channel.queue_bind(exchange="logs_direct", queue=QUEUE, routing_key=rk)
else:
    channel.queue_bind(exchange="logs_direct", queue=QUEUE, routing_key=TIPO_CONSUMER)

executor = ThreadPoolExecutor(max_workers=4)

channel.basic_consume(queue=QUEUE, on_message_callback=callback, auto_ack=True)
print(f"[*] Consumer '{{TIPO_CONSUMER}}' escuchando en '{QUEUE}'...")
channel.start_consuming()
