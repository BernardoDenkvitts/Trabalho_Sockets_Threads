# TDE - Sockets e Threads

**Criado por:**  
Bernardo Arcari Denkvitts <193317@upf.br>  
Pedro Marcelo Roso Manica <173722@upf.br>

## Execução

Para executar os arquivos, utilize o comando:

```bash
python -u nome_do_arquivo.py
```

Não há uma ordem específica para a execução dos arquivos, permitindo que você execute qualquer arquivo desejado sem que outro esteja em execução.

## Consumidor (`consumidor.py`)

### Configurações

- **DIFUSOR_IP:** `'127.0.0.1'` (Endereço IPV4 do difusor)
- **DIFUSOR_PORT:** `5555` (Porta do difusor)

### Tentativas de Conexão

Caso o difusor não esteja conectado no momento da execução do consumidor, este tentará se conectar aleatoriamente em intervalos definidos:

- **TENTATIVA_DORMIR_MIN:** `3` segundos
- **TENTATIVA_DORMIR_MAX:** `7` segundos

Durante as tentativas, o consumidor "dormirá" dentro desse intervalo.

### Escuta

- **INTERVALO_ESCUTA:** `5` segundos (indica que o consumidor está escutando, caso o publicador tenha suas threads inativas/"dormindo').

### Seleção de Informação

Ao executar o consumidor, será solicitado o tipo de informação a ser recebida. A informação será capturada com base na entrada de um valor do tipo inteiro através do teclado. As opções disponíveis são:

1. "Esporte"
2. "Novidades da Internet"
3. "Eletrônicos"
4. "Política"
5. "Negócios"
6. "Viagens"

## Gerador (`gerador.py`)

### Configurações

- **DIFUSOR_IP:** `'127.0.0.1'` (Endereço IPV4 do difusor)
- **DIFUSOR_PORT:** `5000` (Porta do difusor)

### Intervalo de Mensagens

Após enviar ou tentar enviar uma mensagem, o gerador vai "dormir" por um intervalo definido:

- **DORMIR_MIN:** `1` segundo
- **DORMIR_MAX:** `7` segundos

### Geração de Valores

- **VALOR_MIN:** `1`
- **VALOR_MAX:** `100` (Intervalo para gerar números aleatórios).

### Finalização

Ao usar `CTRL + C`, o gerador finalizará as threads responsáveis pela geração das mensagens antes de encerrar completamente.

### Tipos de Mensagem

O tipo de informação/mensagem gerada pelo gerador é definido pela lista `tipos_a_enviar = [1, 3]`, que suporta o envio de um ou mais tipos. As opções disponíveis são as mesmas do consumidor:

1. "Esporte"
2. "Novidades da Internet"
3. "Eletrônicos"
4. "Política"
5. "Negócios"
6. "Viagens"

## Difusor (`difusor.py`)

O difusor aceita conexões com consumidores através do IPV4 usando a porta `5555` e usa a porta `5000` para se comunicar com os geradores.
