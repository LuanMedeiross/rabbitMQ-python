#!/usr/bin/env python
import json

from chat import * # Importando funções de chat
from time import sleep
from threading import Thread
from criptografia import encrypt, CHAVE  # Importando criptografia pelo criptografia.py
from rabbit import channel, enviar, get_usuarios # Importando conexão e configuração pelo rabbit.py

# Histórico de mensagens
historico = []

def main():
    """
    Função principal do programa. Inicializa o banner, solicita o nome do usuário,
    estabelece conexão com o RabbitMQ e inicia o menu de opções.
    """
    try:
        banner()
        p_green("Username: ", end='')
        nome = input().lower()
        global usuario

        menu(nome)
        
        start_chat(nome, usuario)
        show_chat(nome, usuario)
    except KeyboardInterrupt:
        p_red("Encerrando programa ...")
        channel.stop_consuming()
        exit()


def start_chat(nome, usuario):
    """
    Inicia duas threads para consumo e publicação de mensagens no chat.

    Args:
        channel: Canal de comunicação RabbitMQ.
        nome: Nome do usuário local.
        usuario: Nome do usuário remoto.
    """
    Thread(target=consumir, args=(nome, usuario,)).start()
    Thread(target=publicar, args=(usuario, nome,)).start()

def show_chat(nome, usuario):
    """
    Exibe o histórico do chat em tempo real, limpando a tela a cada 2 segundos.

    Args:
        nome: Nome do usuário local.
        usuario: Nome do usuário remoto.
    """
    while True:
        sleep(2)
        clear()

        p_green('=' * 25 + '   \t' + nome + '  |  ' + usuario + '\t\t' +  25 * '=')
        p_red('/sair para sair\n\n')

        for mensagem in historico:
            if mensagem.split()[0] == f'[{nome}]':
                p_blue(mensagem)
            else:
                p_yellow(mensagem)

def publicar(usuario, nome):
    """
    Função para enviar mensagens criptografadas no chat.

    Args:
        channel: Canal de comunicação RabbitMQ.
        usuario: Nome do usuário remoto.
        nome: Nome do usuário local.
    """
    try:
        while True:
            mensagem = input(": ")
            
            mensagem_criptografada = encrypt(mensagem, chave=CHAVE)

            data = json.dumps({'quem_enviou': nome, 'mensagem': mensagem_criptografada})

            enviar(usuario, data)

            linha = f'[{nome}] {mensagem}'
            historico.append(linha)
    except EOFError:
        pass

def consumir(nome, usuario):
    """
    Função para consumir mensagens do chat de forma criptografada e adicionar ao histórico.

    Args:
        channel: Canal de comunicação RabbitMQ.
        nome: Nome do usuário local.
        usuario: Nome do usuário remoto.
    """
    def callback(ch, method, properties, body):

        data = json.loads(body)

        quem_enviou = data['quem_enviou']
        mensagem = data['mensagem']
        mensagem_descriptografa = encrypt(mensagem, chave=CHAVE)

        if quem_enviou == usuario:
            linha = f"[{usuario}] {mensagem_descriptografa}"
            historico.append(linha)

    channel.basic_consume(queue=nome, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

def configure_chat(nome, channel):
    """
    Configura as filas e trocas para o chat entre dois usuários.

    Args:
        nome: Nome do usuário local.
        channel: Canal de comunicação RabbitMQ.
    """
    p_yellow(f"\n{nome} iniciou um chat com {usuario}")

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
    
def menu(nome):
    """
    Exibe o menu de opções do chat e lida com as interações do usuário.

    Args:
        nome: Nome do usuário local.
        channel: Canal de comunicação RabbitMQ.
    """
    while True:
        clear()
        banner()
        
        p_yellow("Usuário: " + nome)
        p_green("\n[1] - Listar usuários")
        p_green("[2] - Iniciar chat")
        p_green("[3] - Sair")

        p_yellow("\n[opt]: ", end='')
        opcao = input()
        usuarios = get_usuarios()

        if opcao == '1':
            p_green('\n ---------------------- LISTA DE USUÁRIOS REGISTRADOS ----------------------\n')
            for user in usuarios:
                p_yellow(user)
            p_yellow('\nPressione ENTER')
            input()

        elif opcao == '2':
            global usuario
            p_yellow("\nChat: ", end='')
            usuario = input().lower()

            if usuarioExiste(usuarios):
                configure_chat(nome, channel)
                break
            else:
                p_red('\nEste usuário não existe!\n')
                p_yellow('Pressione ENTER')
                input()

        elif opcao == '3':
            p_yellow(f"\nVolte sempre, {nome} :)\n")
            quit()
        
        else:
            p_red("\nOpção invalida [ENTER]")
            input()

if __name__ == "__main__":
    main()
