import socket
import threading
import time
from random import randint
import json

IP = "127.0.0.1"
PORT = 81
MOVIES = 2

V_MIN = 1
V_MAX = 100

SLEEP_MIN = 1
SLEEP_MAX = 5

TIPOS_MENSAGEM = {
    1: "SPORTS",
    2: "MOVIES",
    6: "TRAVEL"
}

def start_threads():
    threads = []
    for tipo in TIPOS_MENSAGEM:
        thread = threading.Thread(target=create_data, args=(tipo,))
        thread.start()
        threads.append(thread)

    return threads


def create_data(tipo: int):
    # Envia 10 dados do tipo especificado para o difusor
    for _ in range(11):
        data = {
            "tipo": tipo,
            "val": randint(V_MIN, V_MAX)
        }
        send_data(data)
        print(f"Data of type {TIPOS_MENSAGEM[tipo]} sent: {data}")
        time.sleep(randint(SLEEP_MIN, SLEEP_MAX))


def send_data(data):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(json.dumps(data).encode(), (IP, PORT))
    sock.close()


if __name__ == '__main__':
    print("Starting threads to send informations")
    threads = start_threads()

    for thread in threads:
        thread.join()

    print("All data sent.")