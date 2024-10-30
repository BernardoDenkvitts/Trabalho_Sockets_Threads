import json
import socket
import time
import random
import threading
from datetime import datetime, timedelta

# Parâmetros
DIFUSOR_IP = '127.0.0.1'  # endereço IP do Difusor. Mudar para um qualquer para testar a falha
DIFUSOR_PORT = 5000  # porta do Difusor

# Range para valores e para o tempo de espera entre mensagens
VALOR_MIN = 1
VALOR_MAX = 100
DORMIR_MIN = 1  # seg
DORMIR_MAX = 7  # seg

# Tipos de mensagem
TIPOS_MENSAGEM = {
    1: "Esporte",
    2: "Novidades da Internet",
    3: "Eletrônicos",
    4: "Política",
    5: "Negócios",
    6: "Viagens"
}

# Evento de parada para controle das threads
evento_parar = threading.Event()


# Função de thread para enviar mensagens
def enviar_mensagem(tipo_mensagem):
    while not evento_parar.is_set():
        try:
            # Cria o socket UDP
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
                # Gera um valor aleatório e escolhe um tempo de espera aleatório
                valor = random.randint(VALOR_MIN, VALOR_MAX)
                tempo_dormir = random.randint(DORMIR_MIN, DORMIR_MAX)

                # Prepara a mensagem com tipo e valor
                mensagem = {
                    "tipo": tipo_mensagem,
                    "val": random.randint(VALOR_MIN, VALOR_MAX)
                }

                # Obtém o horário atual e calcula o horário para acordar
                horario_envio = datetime.now()
                udp_socket.sendto(json.dumps(mensagem).encode(), (DIFUSOR_IP, DIFUSOR_PORT))  # Envia a mensagem para o Difusor
                horario_acordar = horario_envio + timedelta(seconds=tempo_dormir)

                # Log de envio de mensagem (em caso de sucesso)
                print(
                    f"Sucesso: Enviada mensagem do tipo {tipo_mensagem}-{TIPOS_MENSAGEM[tipo_mensagem]} para o difusor "
                    f"{DIFUSOR_IP}:{DIFUSOR_PORT} | Hora: {horario_envio} | "
                    f"Valor: {valor} | Dormir: {tempo_dormir}s | Acordar: {horario_acordar.strftime('%H:%M:%S')}")
                print("--------------")

        except Exception as e:
            # Caso o Difusor esteja offline (caso de falha)
            horario_falha = datetime.now().strftime('%H:%M:%S')
            horario_acordar = datetime.now() + timedelta(seconds=tempo_dormir)
            print(
                f"Falha em mensagem {tipo_mensagem}-{TIPOS_MENSAGEM[tipo_mensagem]}: O difusor {DIFUSOR_IP}:{DIFUSOR_PORT} não está conectado. Tentativa às {horario_falha} | Dormir: {tempo_dormir}s "
                f"| Acordar: {horario_acordar.strftime('%H:%M:%S')}")
            print("--------------")

        # Espera antes de enviar outra mensagem, a menos que o evento de parada seja acionado
        if not evento_parar.wait(tempo_dormir):
            time.sleep(tempo_dormir)


# Início do processo Gerador/Pub
def iniciar_gerador(tipos_selecionados):
    # Inicia uma thread para cada tipo de mensagem selecionado
    threads = []
    for tipo in tipos_selecionados:
        if tipo in TIPOS_MENSAGEM:
            thread = threading.Thread(target=enviar_mensagem, args=(tipo,))
            thread.start()
            threads.append(thread)
    return threads


# Função para encerrar o gerador e as threads
def parar_gerador(threads):
    # Sinaliza para todas as threads pararem
    evento_parar.set()

    # Aguarda todas as threads finalizarem
    for thread in threads:
        thread.join()
    print("Todas as threads foram finalizadas com sucesso.")


# Exemplo de uso
if __name__ == "__main__":
    tipos_a_enviar = [1, 3]  # Tipos de mensagem que o Gerador enviará para o difusor

    #   1: "Esporte",
    #   2: "Novidades da Internet",
    #   3: "Eletrônicos",
    #   4: "Política",
    #   5: "Negócios",
    #   6: "Viagens"

    threads = iniciar_gerador(tipos_a_enviar)

    try:
        # Mantém o processo principal ativo até a interrupção do usuário
        while True:
            time.sleep(1)
    except KeyboardInterrupt:  # CTRL + C para parar o processo e finalizar as threads
        print("\nEncerrando o gerador...")
        parar_gerador(threads)