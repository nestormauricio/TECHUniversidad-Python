import pika
import sqlite3
from concurrent.futures import ThreadPoolExecutor

TIPO_CONSUMER = 'error'  # Reemplazar por tipo del consumer
QUEUE = 'consumer_error'

def filtrar_mensaje(routing_key: str, tipo: str) -> bool:
    if tipo == "all":
        return True
    return routing_key.startswith(tipo)

def procesar_msg(msg):
    # Persistencia en SQLite
    conn = sqlite3.connect("mensajes.db", isolation_level=None, check_same_thread=False)
    conn.execute("PRAGMA journal_mode=WAL;")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO mensajes (routing_key, body, timestamp) VALUES (?, ?, datetime('now'))",
        (msg["routing_key"], msg["body"])
    )
    conn.close()
    print(f"[x] Procesado: {msg}")

def callback(ch, method, properties, body):
    msg = {"routing_key": method.routing_key, "body": body.decode()}
    if filtrar_mensaje(msg["routing_key"], TIPO_CONSUMER):
        executor.submit(procesar_msg, msg)

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()
channel.queue_declare(queue=QUEUE)

executor = ThreadPoolExecutor(max_workers=4)

channel.basic_consume(queue=QUEUE, on_message_callback=callback, auto_ack=True)
print(f"[*] Consumer '{TIPO_CONSUMER}' escuchando en 'consumer_error'...")
channel.start_consuming()
