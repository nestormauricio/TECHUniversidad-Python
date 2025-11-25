import threading
import time
import importlib
import sys

# Lista de tus módulos producer
producers = [
    "producer",
    "producer_logs",
    "producer_topic",
    "publisher_logs"
]

def run_producer(module_name):
    print(f"[+] Iniciando {module_name}...")
    try:
        # Recarga el módulo por si ya estaba cargado
        mod = importlib.import_module(module_name)
        importlib.reload(mod)
        # Ejecuta el módulo directamente (lo que está al nivel de script)
        if hasattr(mod, "__file__"):
            with open(mod.__file__, "r", encoding="utf-8") as f:
                code = f.read()
                exec(code, {"__name__": "__main__"})
        print(f"[-] {module_name} terminó.")
    except Exception as e:
        print(f"[!] Error en {module_name}: {e}")

threads = [threading.Thread(target=run_producer, args=(m,)) for m in producers]

# Inicia todos los hilos
for t in threads:
    t.start()
    time.sleep(0.5)  # pequeño delay opcional para no saturar

# Espera a que todos terminen
for t in threads:
    t.join()

print("[*] Todos los producers han terminado.")






















# import threading
# import time

# # Importa tus producers
# import producer
# import producer_logs
# import producer_topic
# import publisher_logs

# def run_producer(func, name):
#     print(f"[+] Iniciando {name}...")
#     func()
#     print(f"[-] {name} terminó.")

# # Crea hilos para cada producer
# threads = [
#     threading.Thread(target=run_producer, args=(producer.main, "producer.py")),
#     threading.Thread(target=run_producer, args=(producer_logs.main, "producer_logs.py")),
#     threading.Thread(target=run_producer, args=(producer_topic.main, "producer_topic.py")),
#     threading.Thread(target=run_producer, args=(publisher_logs.main, "publisher_logs.py"))
# ]

# # Inicia todos los hilos
# for t in threads:
#     t.start()
#     time.sleep(0.5)  # pequeño delay opcional para no saturar

# # Espera a que todos terminen
# for t in threads:
#     t.join()

# print("[*] Todos los producers han terminado.")