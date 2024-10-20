import socket
import time
from random import randint
import json

SPORTS = 1

# Função que gera e envia dados
def create_data():
    for _ in range(10):
        data = {
            "tipo": SPORTS,
            "val": randint(1, 100)
        }
        send_data(data)
        print(f"Data of type SPORTS sent: {data}")
        time.sleep(randint(1, 5))


def send_data(data):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(json.dumps(data).encode(), ("127.0.0.1", 81))
    sock.close()


if __name__ == '__main__':
    create_data()
    print("All data sent.")