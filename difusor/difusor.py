import socket
import json
import threading
import time
from datetime import datetime


class Informacao:
    def __init__(self, seq: int, tipo: int, valor: int):
        self.seq = seq
        self.tipo = tipo
        self.valor = valor

# Vou deixar só os tipos que o produtor estiver enviando no final
ESPORTES = 1
NOVIDADES_DA_INTERNET = 2
ELETRONICOS = 3
POLITICA = 4
NEGOCIOS = 5
VIAGENS = 6

tipos_recebidos = {
    ESPORTES: "ESPORTES",
    NOVIDADES_DA_INTERNET: "NOVIDADES_DA_INTERNET",
    ELETRONICOS: "ELETRONICOS",
    POLITICA: "POLITICA",
    NEGOCIOS: "NEGOCIOS",
    VIAGENS: "VIAGENS"
}

seq_informacoes = {
    ESPORTES: 0,
    NOVIDADES_DA_INTERNET: 0,
    ELETRONICOS: 0,
    POLITICA: 0,
    NEGOCIOS: 0,
    VIAGENS: 0
}

conexao_consumidores = {
    ESPORTES: [],
    NOVIDADES_DA_INTERNET: [],
    ELETRONICOS: [],
    POLITICA: [],
    NEGOCIOS: [],
    VIAGENS: []
}

def consome_novas_informacoes():
    while True:
        data, addr = sock.recvfrom(1024)
        data = json.loads(data.decode())

        tipo_literal = tipos_recebidos[data["tipo"]]
        print(f"Recebido informacao do tipo {data['tipo']}-{tipo_literal}: {data}")

        # Caso nao tenha consumidores para esse tipo, descarta a mensagem
        if not len(conexao_consumidores[data["tipo"]]):
            print(f"Sem consumidores para o tipo {data['tipo']}. Descartando mensagem.")
            continue

        new_data = Informacao(seq=seq_informacoes[data["tipo"]], tipo=data["tipo"], valor=data["valor"])
        seq_informacoes[data["tipo"]] += 1

        notify_consumers(data["tipo"], new_data)


# Função para notificar consumidores de um tipo específico quando novos dados são adicionados
def notify_consumers(tipo_informacao, new_data):
    for conn in conexao_consumidores[tipo_informacao]:
        serialized_data = json.dumps(new_data.__dict__).encode()
        conn.sendall(serialized_data)
        print(f"({datetime.now().strftime('%H:%M:%S')}) Enviando informacao do tipo {tipo_informacao}-{tipos_recebidos[tipo_informacao]} para o consumidor {conn.getpeername()}: {new_data.__dict__}")



# Atende um consumidor individualmente
def handle_consumer(conn, tipo_informacao):
    informacoes_consumidor = [tipo_informacao]
    try:
        # Adiciona o consumidor a lista de informacao que ele quer receber
        conexao_consumidores[tipo_informacao].append(conn)
        
        # Mantém a conexão ativa e monitora mensagens do cliente
        while True:
            message = conn.recv(1024).decode()

            if "Exit" in message:
                print(f"Recebido 'Exit' do consumidor {conn.getpeername()}. Finalizando conexao.")
                conn.sendall("Conexao encerrada pelo servidor.".encode())
                break
            else:
                try:
                    nova_informacao = int(message)
                    print(f"{conn.getpeername()} adicionado para receber informacoes do tipo {nova_informacao}")
                    conexao_consumidores[nova_informacao].append(conn)
                    informacoes_consumidor.append(nova_informacao)
                except Exception as e:
                    print(f"Consumidor {conn.getpeername()} solicitou uma informacao que nao existe")
                    conn.sendall("Informacao nao existente".encode())

            time.sleep(1)
    except Exception as e:
        print(f"Conexão com o consumidor {conn.getpeername()} fechada. Motivo: {e}")
    finally:
        # Remover o consumidor de todas as informacoes que ele se inscreveu ao final da conexão
        for info in informacoes_consumidor:
            conexao_consumidores[info].remove(conn)

        conn.close()


# Função para aceitar novas conexões de consumidores
def aceita_conexoes():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(("127.0.0.1", 5555))
        server_socket.listen()

        print("Esperando conexoes..")
        while True:
            conn, addr = server_socket.accept()
            print(f"Consumidor conectado: {addr}")

            tipo_informacao = int(conn.recv(1024).decode())

            # Criar uma thread para gerenciar a conexão do consumidor
            thread_consumidor = threading.Thread(target=handle_consumer, args=(conn, tipo_informacao))
            thread_consumidor.start()


if __name__ == '__main__':
    print("INICIANDO DIFUSOR")

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("127.0.0.1", 5000))

    thread_consumidor = threading.Thread(target=consome_novas_informacoes)
    thread_consumidor.start()

    aceita_conexoes_thread = threading.Thread(target=aceita_conexoes)
    aceita_conexoes_thread.start()

    thread_consumidor.join()
    aceita_conexoes_thread.join()

