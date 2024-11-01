import socket
import time
import random
import threading
import json
from datetime import datetime, timedelta

DIFUSOR_IP = '127.0.0.1'
DIFUSOR_PORT = 5555

TENTATIVA_DORMIR_MIN = 3
TENTATIVA_DORMIR_MAX = 7
INTERVALO_ESCUTA = 5

TIPOS_MENSAGENS = {
    1: "Esporte",
    2: "Novidades da Internet",
    3: "Eletrônicos",
    4: "Política",
    5: "Negócios",
    6: "Viagens"
}

def conectar_ao_difusor(tipo_mensagem):
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_socket:
                tcp_socket.settimeout(2)
                tcp_socket.connect((DIFUSOR_IP, DIFUSOR_PORT))
                
                descricao_tipo = TIPOS_MENSAGENS.get(tipo_mensagem, "Tipo desconhecido")
                print(f"[Consumidor: {datetime.now().strftime('%H:%M:%S')}] Conexão estabelecida com o Difusor {DIFUSOR_IP}:{DIFUSOR_PORT}")
                print(f"[Consumidor: {datetime.now().strftime('%H:%M:%S')}] Solicitação enviada: Tipo {tipo_mensagem} - {descricao_tipo}")

                tcp_socket.sendall(str(tipo_mensagem).encode())
                tempo_ultima_escuta = time.time()

                while True:
                    if time.time() - tempo_ultima_escuta >= INTERVALO_ESCUTA:
                        print(f"[Consumidor: {datetime.now().strftime('%H:%M:%S')}] Aguardando mensagens do Difusor...")
                        tempo_ultima_escuta = time.time()

                    tcp_socket.settimeout(1.0)
                    try:
                        dados = tcp_socket.recv(1024)
                        if dados:
                            mensagem = json.loads(dados.decode())
                            tipo = mensagem.get('tipo')
                            valor = mensagem.get('valor')
                            seq = mensagem.get('seq')
                            info_objeto = {"seq": seq, "tipo": tipo, "valor": valor}
                            print(f"[Consumidor: {datetime.now().strftime('%H:%M:%S')}] Mensagem recebida: {info_objeto}")

                            tempo_ultima_escuta = time.time()

                    except socket.timeout:
                        continue

        except (ConnectionRefusedError, OSError):
            horario_tentativa = datetime.now()
            tempo_dormir = random.randint(TENTATIVA_DORMIR_MIN, TENTATIVA_DORMIR_MAX)
            horario_acordar = horario_tentativa + timedelta(seconds=tempo_dormir)

            print(f"[Consumidor: {datetime.now().strftime('%H:%M:%S')}] Tentativa de conexão falhou | "
                  f"Dormir: {tempo_dormir}s | Acordar: {horario_acordar.strftime('%H:%M:%S')}")

            time.sleep(tempo_dormir)

def iniciar_consumidor():
    print(f"[Consumidor: {datetime.now().strftime('%H:%M:%S')}] Iniciando o Consumidor para se conectar ao Difusor {DIFUSOR_IP}:{DIFUSOR_PORT}")
    print("\nTipos de Mensagens Disponíveis:")
    for tipo, descricao in TIPOS_MENSAGENS.items():
        print(f"{tipo}: {descricao}")
    print("--------------")

    while True:
        try:
            tipo_mensagem = int(input("Digite o número do tipo de mensagem desejada (1 a 6): "))
            if tipo_mensagem not in TIPOS_MENSAGENS:
                print("Número de tipo inválido. Por favor, insira um número entre 1 e 6.")
                continue

            descricao_tipo = TIPOS_MENSAGENS[tipo_mensagem]
            print(f"[Consumidor: {datetime.now().strftime('%H:%M:%S')}] Tipo escolhido: {tipo_mensagem} - {descricao_tipo}")

            thread_conexao = threading.Thread(target=conectar_ao_difusor, args=(tipo_mensagem,))
            thread_conexao.start()
            thread_conexao.join()

        except ValueError:
            print(f"[Consumidor: {datetime.now().strftime('%H:%M:%S')}] Entrada inválida. Por favor, insira um número.")

if __name__ == "__main__":
    iniciar_consumidor()
