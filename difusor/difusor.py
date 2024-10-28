import signal
import socket
import json
import sys
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

consumer_connections = {
    SPORTS: [],
    MOVIES: [],
    TRAVEL: []
}

def consume_data():
    while True:
        #if len(data_types[SPORTS]) == 10 and len(data_types[MOVIES]) == 10 and len(data_types[TRAVEL]) == 10:
        #    break

        data, addr = sock.recvfrom(1024)
        data = json.loads(data.decode())

        tipo_literal = tipos_recebidos[data["tipo"]]
        print(f"Data received for type {tipo_literal}: {data}")

        new_data = Informacao(seq=len(data_types[data["tipo"]]), tipo=data["tipo"], val=data["val"])
        data_types[data["tipo"]].append(new_data)

        print(f"Data stored for type {tipo_literal}: {new_data.__dict__}")


# Função para notificar consumidores de um tipo específico quando novos dados são adicionados
def notify_consumers(data_type, new_data):
    for conn in consumer_connections[data_type]:
        serialized_data = json.dumps(new_data.__dict__).encode()
        conn.sendall(serialized_data)
        print(f"Sent data to consumer {conn.getpeername()}: {new_data.__dict__}")



# Função para atender um consumidor individualmente
def handle_consumer(conn, data_type):
    try:
        # Enviar dados existentes para o consumidor
        for data in data_types[data_type]:
            serialized_data = json.dumps(data.__dict__).encode()
            conn.sendall(serialized_data)

        # Adiciona o consumidor à lista de conexões interessadas
        consumer_connections[data_type].append(conn)

        # Mantém a conexão ativa e monitora mensagens do cliente
        while True:
            message = conn.recv(1024).decode()

            if "Exit" in message:
                print(f"Received 'Exit' from consumer {conn.getpeername()}. Closing connection.")
                conn.sendall("Connection closed by server.".encode())
                break

            time.sleep(1)  # Mantém a conexão aberta e ajusta o intervalo conforme necessário
    except Exception as e:
        print(f"Connection to consumer {conn.getpeername()} closed. Reason: {e}")
    finally:
        # Remover o consumidor ao final da conexão
        consumer_connections[data_type].remove(conn)
        conn.close()


# Função para aceitar novas conexões de consumidores
def accept_connections():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(("127.0.0.1", 5000))
        server_socket.listen()

        print("Awaiting consumer connections...")
        while True:
            conn, addr = server_socket.accept()
            print(f"Consumer connected: {addr}")

            data_type_request = int(conn.recv(1024).decode())

            # Criar uma thread para gerenciar a conexão do consumidor
            consumer_thread = threading.Thread(target=handle_consumer, args=(conn, data_type_request))
            consumer_thread.start()


if __name__ == '__main__':
    print("INICIANDO DIFUSOR")

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("127.0.0.1", 81))

    consumer_thread = threading.Thread(target=consume_data)
    consumer_thread.start()

    accept_connections_thread = threading.Thread(target=accept_connections)
    accept_connections_thread.start()

    consumer_thread.join()
    accept_connections_thread.join()

