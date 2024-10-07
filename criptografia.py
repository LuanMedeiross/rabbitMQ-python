# Converte cada caractere da string em seu valor numérico (valor ASCII)
def dex(texto):
    return [ord(t) for t in texto]  # 'ord' converte um caractere em um número inteiro ASCII

# Converte cada número da lista de volta para o caractere correspondente (usando os valores ASCII)
def text(decimal):
    return [chr(d) for d in decimal]  # 'chr' converte um número inteiro de volta em um caractere

# Junta todos os caracteres em uma única string
def f(texto):
    return ''.join(texto)  # 'join' junta a lista de caracteres em uma única string

# Função que criptografa a entrada usando uma chave
def encrypt(entrada, chave):
    saida = []  # Lista que armazenará os valores criptografados
    entrada_f, chave_f = dex(entrada), dex(chave)  # Converte a entrada e a chave para listas de valores ASCII

    # Para cada caractere na entrada, aplicamos a chave inteira usando XOR
    for caractere in entrada_f:
        char = caractere  # Começamos com o valor original do caractere

        # Aplicamos o XOR entre o caractere e cada valor da chave
        for c in chave_f:
            char = c ^ caractere  # XOR entre o caractere e o valor atual da chave

        saida.append(char)  # Adiciona o resultado final à lista de saída

    return f(text(saida))  # Converte os números criptografados de volta para caracteres

if __name__ == '__main__':

    chave = "?:><,#.;/^}]~`[$\\]-=+_!@%¨&*()"

    mensagem_criptografada = encrypt("te amo linda", chave)
    print(f(mensagem_criptografada))
