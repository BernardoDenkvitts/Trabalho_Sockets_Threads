import socket
import json
import threading
import time


# TODO thread que recebe dados dos produtores
# TODO thread que vai enviar os dados pros consumidores
# TODO colocar os atributos esperados pelo professor na classe Data

class Informacao:
    def __init__(self, seq: int, tipo: int, val: int):
        self.seq = seq
        self.tipo = tipo
        self.val = val




SPORTS = 1
MOVIES = 2
TRAVEL = 6

tipos_recebidos = {
    SPORTS: "SPORTS",
    MOVIES: "MOVIES",
    TRAVEL: "TRAVEL"
}

# Dicionário para armazenar os dados recebidos
data_types = {
    SPORTS: [],
    MOVIES: [],
    TRAVEL: []
}


def consume_data():
    while True:
        if len(data_types[SPORTS]) == 10 and len(data_types[MOVIES]) == 10 and len(data_types[TRAVEL]) == 10:
            break

        data, addr = sock.recvfrom(1024)
        data = json.loads(data.decode())

        tipo_literal = tipos_recebidos[data["tipo"]]
        print(f"Data received for type {tipo_literal}: {data}")

        new_data = Informacao(seq=len(data_types[data["tipo"]]), tipo=data["tipo"], val=data["val"])
        data_types[data["tipo"]].append(new_data)

        print(f"Data stored for type {tipo_literal}: {new_data.__dict__}")
        print(len(data_types[data["tipo"]]), len(data_types[SPORTS]), len(data_types[MOVIES]), len(data_types[TRAVEL]))


if __name__ == '__main__':
    print("INICIANDO DIFUSOR")

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("127.0.0.1", 81))

    consumer_thread = threading.Thread(target=consume_data)
    consumer_thread.start()

    consumer_thread.join()

    for v in data_types[SPORTS]:
        print(v.__dict__)

    print("-----\n")

    for v in data_types[MOVIES]:
        print(v.__dict__)

    print("-----\n")

    for v in data_types[TRAVEL]:
        print(v.__dict__)
