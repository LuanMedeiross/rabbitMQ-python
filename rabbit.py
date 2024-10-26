# Importando modulo do RabbitMQ
import pika
import requests

# Configurações do servidor AMQP (RabbitMQ)
AMQP = {
    'url': 'https://jackal.rmq.cloudamqp.com/',
    'host': "jackal-01.rmq.cloudamqp.com",
    'port': 5672,
    'username': "oejhcyan",
    'password': "sIsCKGekFXYFbmf5L4ssP_Vg--lq7yAM"
}

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

def enviar(usuario, data):
    channel.basic_publish(
        exchange='data_exchange',
        routing_key=usuario,
        body=data,
        properties=pika.BasicProperties(delivery_mode=2)
    )

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

channel = connection()
