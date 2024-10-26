#!/usr/bin/env python
import pika
import requests
import json

from time import sleep
from os import system
from threading import Thread
from criptografia import encrypt # Funções de criptografia 

# Configurações do servidor AMQP (RabbitMQ)
AMQP = {
    'url': 'https://jackal.rmq.cloudamqp.com/',
    'host': "jackal-01.rmq.cloudamqp.com",
    'port': 5672,
    'username': "oejhcyan",
    'password': "sIsCKGekFXYFbmf5L4ssP_Vg--lq7yAM"
}

# Cores para formatação no terminal
COR = {
    'vermelho': '\033[3;31m',
    'verde': '\033[3;32m',
    'amarelo': '\033[3;33m',
    'azul': '\033[3;34m',
    'x': '\033[m'
}

# Chave para criptografia
CHAVE = "asdjASsdfASC12D1@"

# Histórico de mensagens
historico = []

def connection():
    """
    Estabelece conexão com o servidor RabbitMQ e retorna o canal.
    """
    connection_parameters = pika.ConnectionParameters(
        host=AMQP['host'],
        port=AMQP['port'], 
        credentials=pika.PlainCredentials(
            username=AMQP['username'],
            password=AMQP['password']
        ),
        virtual_host=AMQP['username']
    )

    connection = pika.BlockingConnection(connection_parameters)
    return connection.channel()

def main():
    """
    Função principal do programa. Inicializa o banner, solicita o nome do usuário,
    estabelece conexão com o RabbitMQ e inicia o menu de opções.
    """
    banner()
    nome = input("\n\nUsername: ").lower()
    global usuario

    channel = connection()
    menu(nome, channel)
    start_chat(channel, nome, usuario)
    show_chat(nome, usuario)

def start_chat(channel, nome, usuario):
    """
    Inicia duas threads para consumo e publicação de mensagens no chat.

    Args:
        channel: Canal de comunicação RabbitMQ.
        nome: Nome do usuário local.
        usuario: Nome do usuário remoto.
    """
    Thread(target=consumir, args=(channel, nome, usuario,)).start()
    Thread(target=publicar, args=(channel, usuario, nome,)).start()

def show_chat(nome, usuario):
    """
    Exibe o histórico do chat em tempo real, limpando a tela a cada 2 segundos.

    Args:
        nome: Nome do usuário local.
        usuario: Nome do usuário remoto.
    """
    while True:
        sleep(2)
        #system('cls')  # No Linux, use 'clear' em vez de 'cls'

        print(COR['verde'] + '=' * 20 + '\t' + nome + '  |  ' + usuario + '\t' + '=' * 20 + '\n' + COR['x'])

        for mensagem in historico:
            print(mensagem)

def publicar(channel, usuario, nome):
    """
    Função para enviar mensagens criptografadas no chat.

    Args:
        channel: Canal de comunicação RabbitMQ.
        usuario: Nome do usuário remoto.
        nome: Nome do usuário local.
    """
    while True:
        mensagem = input(": ")
        mensagem_criptografada = encrypt(mensagem, chave=CHAVE)

        data = json.dumps({'quem_enviou': nome, 'mensagem': mensagem_criptografada})

        channel.basic_publish(
            exchange='data_exchange',
            routing_key=usuario,
            body=data,
            properties=pika.BasicProperties(delivery_mode=2)
        )

        linha = f'{COR["azul"]}[{nome}] {mensagem}{COR["x"]}'
        historico.append(linha)

def consumir(channel, nome, usuario):
    """
    Função para consumir mensagens do chat de forma criptografada e adicionar ao histórico.

    Args:
        channel: Canal de comunicação RabbitMQ.
        nome: Nome do usuário local.
        usuario: Nome do usuário remoto.
    """
    def callback(ch, method, properties, body):

        print(body)
        data = json.loads(body)

        quem_enviou = data['quem_enviou']
        mensagem = data['mensagem']
        mensagem_descriptografa = encrypt(mensagem, chave=CHAVE)

        if quem_enviou == usuario:
            linha = f'{COR["amarelo"]}[{usuario}] {mensagem_descriptografa}{COR["x"]}'
            historico.append(linha)

    channel.basic_consume(queue=nome, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

def get_usuarios():
    """
    Retorna uma lista de usuários registrados no servidor RabbitMQ.
    
    Returns:
        List[str]: Lista de nomes de usuários registrados.
    """
    url = AMQP['url'] + '/api/queues/' + AMQP['username']
    response = requests.get(url, auth=(AMQP['username'], AMQP['password']))
    
    usuarios = [q['name'] for q in response.json()]
    return usuarios

def configure_chat(nome, channel):
    """
    Configura as filas e trocas para o chat entre dois usuários.

    Args:
        nome: Nome do usuário local.
        channel: Canal de comunicação RabbitMQ.
    """
    print(f'\n{COR["vermelho"]}{nome} iniciou um chat com {usuario}')

    channel.exchange_declare(exchange='data_exchange', durable=True, exchange_type='direct')
    channel.queue_declare(queue=usuario, durable=True)
    channel.queue_declare(queue=nome, durable=True)
    channel.queue_bind(queue=usuario, exchange="data_exchange", routing_key=usuario)
    channel.queue_bind(queue=nome, exchange="data_exchange", routing_key=nome)

def usuarioExiste(usuarios):
    """
    Verifica se um usuário existe na lista de usuários registrados.

    Args:
        usuarios: Lista de nomes de usuários registrados.

    Returns:
        bool: Verdadeiro se o usuário existe, Falso caso contrário.
    """
    usuario_cadastrado = False
    for u in usuarios:
        if u == usuario:
            usuario_cadastrado = True
    return usuario_cadastrado

def banner():
    """
    Exibe um banner ASCII no terminal.
    """
    print(COR['verde'])
    print('    ____        __    __    _ __  __  _______  ________  _____  ______')
    print('   / __ \\____ _/ /_  / /_  (_) /_/  |/  / __ \\/ ____/ / / /   |/_  __/')
    print('  / /_/ / __ `/ __ \\/ __ \\/ / __/ /|_/ / / / / /   / /_/ / /| | / /   ')
    print(' / _, _/ /_/ / /_/ / /_/ / / /_/ /  / / /_/ / /___/ __  / ___ |/ /    ')
    print('/_/ |_|\\__,_/_.___/_.___/_/\\__/_/  /_/\\___\\_\\____/_/ /_/_/  |_/_/  ')
    print(COR['x'])

def menu(nome, channel):
    """
    Exibe o menu de opções do chat e lida com as interações do usuário.

    Args:
        nome: Nome do usuário local.
        channel: Canal de comunicação RabbitMQ.
    """
    while True:
        #system('cls')  # No Linux, use 'clear'
        banner()

        print(COR['verde'])
        print('\n')
        print("Usuário:", nome)
        print('\n')
        print("[1] - Listar usuários")
        print("[2] - Iniciar chat")
        print("[3] - Sair")

        opcao = int(input('\n\nOpção: '))
        usuarios = get_usuarios()

        if opcao == 1:
            print('\n ----------- LISTA DE USUÁRIOS REGISTRADOS -----------' + COR['amarelo'])
            for user in usuarios:
                print(user)
            input(COR['x'] + '\nPressione ENTER')

        elif opcao == 2:
            global usuario
            usuario = input("\nDigite o nome do usuário: ").lower()

            if usuarioExiste(usuarios):
                configure_chat(nome, channel)
                break
            else:
                print('\nEste usuário não existe!\n')
                input('Pressione ENTER')

        elif opcao == 3:
            print(f"\nVolte sempre {nome}:)\n")
            input("Pressione ENTER para sair ")
            quit()

    print(COR['x'])

if __name__ == "__main__":
    main()
