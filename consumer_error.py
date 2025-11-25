import pika
import sqlite3
import json
from datetime import datetime

DB_FILE = "mensajes.db"
LOG_FILE = "mensajes.log"
EXCHANGE_NAME = "logs_topic"
EXCHANGE_TYPE = "topic"
ROUTING_KEYS = ["#", "sistema.info", "sistema.warning", "*.error", "app.*"]

# Conectar SQLite y crear tabla si no existe
# conn = sqlite3.connect(DB_FILE)
conn = sqlite3.connect(DB_FILE, timeout=10, check_same_thread=False)

cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS mensajes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    routing_key TEXT,
    body TEXT,
    timestamp TEXT
)
""")
conn.commit()

# Conexión RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type=EXCHANGE_TYPE)
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

# Bind a todas las routing keys
for key in ROUTING_KEYS:
    channel.queue_bind(exchange=EXCHANGE_NAME, queue=queue_name, routing_key=key)

print(f"[*] Esperando mensajes en {queue_name}. CTRL+C para salir")

def callback(ch, method, properties, body):
    routing_key = method.routing_key
    text = body.decode()
    is_json = False
    try:
        parsed = json.loads(text)
        is_json = True
    except json.JSONDecodeError:
        parsed = None

    if is_json:
        print(f"--- NUEVO MENSAJE ---\nRouting key: {routing_key}\nJSON: {parsed}\n")
    else:
        print(f"--- NUEVO MENSAJE ---\nRouting key: {routing_key}\nRaw body: {text}\nNo es JSON ❌\n")

    # Guardar en SQLite
    cursor.execute(
        "INSERT INTO mensajes (routing_key, body, timestamp) VALUES (?, ?, ?)",
        (routing_key, text, datetime.now().isoformat())
    )
    conn.commit()

    # Guardar en log
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now().isoformat()} | {routing_key} | {text}\n")

channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
channel.start_consuming()