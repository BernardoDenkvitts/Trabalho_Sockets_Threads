import socket
import time
import random
import threading
import json
from datetime import datetime, timedelta

DIFUSOR_IP = '127.0.0.1'
DIFUSOR_PORT = 5000

VALOR_MIN = 1
VALOR_MAX = 100
DORMIR_MIN = 1  # seg
DORMIR_MAX = 7  # seg

TIPOS_MENSAGEM = {
    1: "Esporte",
    2: "Novidades da Internet",
    3: "Eletrônicos",
    4: "Política",
    5: "Negócios",
    6: "Viagens"
}

evento_parar = threading.Event()

def enviar_mensagem(tipo_mensagem):
    while not evento_parar.is_set():
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
                valor = random.randint(VALOR_MIN, VALOR_MAX)
                tempo_dormir = random.randint(DORMIR_MIN, DORMIR_MAX)
                
                mensagem = json.dumps({"tipo": tipo_mensagem, "valor": valor})

                horario_envio = datetime.now()
                udp_socket.sendto(mensagem.encode(), (DIFUSOR_IP, DIFUSOR_PORT)) 
                horario_acordar = horario_envio + timedelta(seconds=tempo_dormir)              
                
                print(f"[Gerador: {datetime.now().strftime('%H:%M:%S')}] Sucesso ao enviar mensagem {mensagem} para o difusor "
                      f"{DIFUSOR_IP}:{DIFUSOR_PORT} | "
                      f"Dormir: {tempo_dormir}s | Acordar: {horario_acordar.strftime('%H:%M:%S')}")
                
        except Exception as e:
            horario_acordar = datetime.now() + timedelta(seconds=tempo_dormir)
            
            print(f"[Gerador: {datetime.now().strftime('%H:%M:%S')}] Falha ao enviar em mensagem {mensagem} o difusor "
                  f"{DIFUSOR_IP}:{DIFUSOR_PORT} não está conectado | Dormir: {tempo_dormir}s "
                  f"| Acordar: {horario_acordar.strftime('%H:%M:%S')}")
        
        if not evento_parar.wait(tempo_dormir):
            time.sleep(tempo_dormir)

def iniciar_gerador(tipos_selecionados):
    print(f"[Gerador: {datetime.now().strftime('%H:%M:%S')}] Iniciando o Gerador para se conectar ao Difusor {DIFUSOR_IP}:{DIFUSOR_PORT}")
    threads = []
    for tipo in tipos_selecionados:
        if tipo in TIPOS_MENSAGEM:
            thread = threading.Thread(target=enviar_mensagem, args=(tipo,))
            thread.start()
            threads.append(thread)
    return threads

def parar_gerador(threads):
    evento_parar.set()
    
    for thread in threads:
        thread.join()
    print(f"[Gerador: {datetime.now().strftime('%H:%M:%S')}] Todas as threads foram finalizadas com sucesso.")

if __name__ == "__main__":
    tipos_a_enviar = [1, 3]  #tipos de mensagem que o Gerador enviará para o difusor

    #   1: "Esporte",
    #   2: "Novidades da Internet",
    #   3: "Eletrônicos",
    #   4: "Política",
    #   5: "Negócios",
    #   6: "Viagens"
    
    threads = iniciar_gerador(tipos_a_enviar)
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt: #CTRL + C para parar o processo e finalizar as threads
        print(f"[Gerador: {datetime.now().strftime('%H:%M:%S')}] Encerrando o gerador...")
        parar_gerador(threads)
