# Projeto de Chat Criptografado

Este projeto é um sistema de chat criptografado que utiliza RabbitMQ para comunicação entre os usuários. A criptografia é realizada com uma chave fornecida, garantindo a segurança das mensagens trocadas.

## Funcionalidades

- **Chat em Tempo Real:** Usuários podem enviar e receber mensagens em tempo real.
- **Criptografia das Mensagens:** Todas as mensagens são criptografadas antes de serem enviadas, garantindo a privacidade.
- **Interface de Usuário Simples:** O sistema possui um menu de opções fácil de usar.

## Requisitos

Certifique-se de ter as seguintes dependências instaladas:

```
pika==1.3.2
requests==2.32.2
```

Você pode instalar as dependências usando o seguinte comando:

```bash
pip install -r requirements.txt
```

## Como Usar

1. **Configuração do Servidor RabbitMQ:** Antes de executar o programa, verifique se você possui acesso a um servidor RabbitMQ. Atualize as informações de conexão no arquivo `app.py`.

2. **Executando o Programa:**
   Execute o arquivo `app.py` para iniciar o sistema de chat.

   ```bash
   python app.py
   ```

3. **Interagindo com o Sistema:**
   - Ao iniciar o programa, você verá um banner e será solicitado a inserir seu nome de usuário.
   - O menu apresentará opções para listar usuários registrados, iniciar um chat ou sair do programa.
   - Selecione a opção desejada e siga as instruções exibidas.

## Estrutura do Projeto

- `app.py`: Contém a lógica principal do chat, incluindo a conexão com o RabbitMQ e a manipulação de mensagens.
- `criptografia.py`: Implementa funções para criptografar e descriptografar mensagens.
- `requirements.txt`: Lista as dependências necessárias para o projeto.

## Como Funciona a Criptografia

A criptografia das mensagens é feita usando uma chave específica. O processo utiliza a operação XOR entre os valores ASCII da entrada e da chave, garantindo que apenas quem possui a chave possa descriptografar as mensagens.

## Colaboradores 
- Aliffer Corrêa
- Paulo Moretti
- Fabricio
- Felipe Feitosa
- João Avelino
- Kauan Rodrigues

## Considerações Finais

Sinta-se à vontade para modificar e melhorar este projeto. Para dúvidas ou sugestões, entre em contato.
