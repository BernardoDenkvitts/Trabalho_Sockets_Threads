import socket
import json

# TODO thread que recebe dados dos produtores
# TODO thread que vai enviar os dados pros consumidores
# TODO colocar os atributos esperados pelo professor na classe Data

class Data:
    def __init__(self, seq: int, tipo: str, val: int):
        self.seq = seq
        self.seq += 1
        self.tipo = tipo
        self.val = val


SPORTS = 1
MOVIES = 2

# Dicionário para armazenar os dados recebidos
data_types = {
    SPORTS: [],
    MOVIES: [],
}


def consume_data():
    while True:
        if len(data_types[SPORTS]) == 10 and len(data_types[MOVIES]) == 10:
            break

        data, addr = sock.recvfrom(1024)
        data = json.loads(data.decode())

        tipo_literal = "SPORTS" if data["tipo"] == SPORTS else "MOVIES"

        print(f"Data received for type {tipo_literal}: {data}")

        new_data = Data(seq=len(data_types[data["tipo"]]), tipo=tipo_literal, val=data["val"])
        data_types[data["tipo"]].append(new_data)

        print(f"Data stored for type {tipo_literal}: {new_data.__dict__}")


if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("127.0.0.1", 81))

    consume_data()

    for v in data_types[SPORTS]:
        print(v.__dict__)

    print("-----\n")

    for v in data_types[MOVIES]:
        print(v.__dict__)
