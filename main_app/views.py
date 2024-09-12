from django.shortcuts import render
import timeit

# Create your views here.

def mainPage(request):
    return render(request,'paginas/home.html')

def dividePaginas(request,id):
    overflows=0
    colisoes=0

    dados = []

    arquivo = open('C:/Users/gabriel.linhares/Desktop/gabriel/django/projeto_db/main_app/words_alpha(1).txt', 'r')
    for linha in arquivo:
        dados.append(linha.strip())

    dadosPorPagina = id

    def dividir_vetor(vetor, tamanho_subvetor):
        paginas = []
        for i in range(0, len(vetor), tamanho_subvetor):
            subvetor = vetor[i:i + tamanho_subvetor]
            paginas.append(subvetor)
        return paginas


    def hash_custom(dado, tamanho_bucket):
        hash_valor = 0
        p = 31  # Um número primo
        m = 10**9 + 9  # Outro número primo grande para modulo
        
        for i, caractere in enumerate(dado):
            # Multiplica o código ASCII elevado a uma potência de p para espalhar os valores
            hash_valor = (hash_valor + (ord(caractere) * p**i)) % m
        
        return hash_valor % tamanho_bucket

        
    tamanho_bucket=100000
    # Inicializa buckets como listas vazias
    buckets = [[] for _ in range(tamanho_bucket)]
    
    # Cria um mapeamento de dado para índice do subvetor (página)
    pagina_indices = {dado: i // dadosPorPagina for i, dado in enumerate(dados)}


    for dado in dados:
        # Calcula o índice do bucket usando a nova função de hash
        indice_bucket = hash_custom(dado, tamanho_bucket)
        
        # Restante do código continua o mesmo
        indice_pagina = pagina_indices[dado]
            
        # Verifica se há um sub-bucket disponível ou precisa criar um novo
        if not buckets[indice_bucket]:
            buckets[indice_bucket].append([])

        elif len(buckets[indice_bucket][-1]) == 6:
            buckets[indice_bucket].append([])
            overflows += 1

        if len(buckets[indice_bucket]) > 1:
            colisoes += 1
            
        # Adiciona a tupla ao último sub-bucket disponível
        buckets[indice_bucket][-1].append((dado, indice_pagina+1))
    

    # Divide os dados em páginas
    paginas = dividir_vetor(dados, dadosPorPagina)

    context={'buckets':buckets,'paginas':paginas,'colisoes':colisoes,'overflows':overflows}
    return render(request,'paginas/dados_organizados.html',context)


def busca(request, palavra, dadosPorPagina):
    dados = []

    with open('C:/Users/gabriel.linhares/Desktop/gabriel/django/projeto_db/main_app/words_alpha(1).txt', 'r') as arquivo:
        for linha in arquivo:
            dados.append(linha.strip())

    pagina_indices = {dado: i // dadosPorPagina for i, dado in enumerate(dados)}

    # Medindo o tempo com timeit para o algoritmo serial
    start_time_serial = timeit.default_timer()
    if palavra in pagina_indices:
        pagina = pagina_indices[palavra] + 1  
        mensagem_serial = f"Código serial: A palavra '{palavra}' está na página {pagina}."
    else:
        mensagem_serial = f"Código serial: A palavra '{palavra}' não foi encontrada."
    elapsed_time_serial = timeit.default_timer() - start_time_serial
    mensagem_serial += f" (Tempo de execução: {elapsed_time_serial:.8f} segundos)"

    # Função de hash customizada
    def hash_custom(dado, tamanho_bucket):
        hash_valor = 0
        p = 31  # Um número primo
        m = 10**9 + 9  # Outro número primo grande para modulo
        for i, caractere in enumerate(dado):
            hash_valor = (hash_valor + (ord(caractere) * p**i)) % m
        return hash_valor % tamanho_bucket

    # Algoritmo usando buckets
    tamanho_bucket = 100000
    buckets = [[] for _ in range(tamanho_bucket)]

    # Adicionar dados aos buckets
    for dado in dados:
        indice_bucket = hash_custom(dado, tamanho_bucket)
        indice_pagina = pagina_indices[dado]

        if not buckets[indice_bucket]:
            buckets[indice_bucket].append([])

        elif len(buckets[indice_bucket][-1]) == 6:
            buckets[indice_bucket].append([])

        buckets[indice_bucket][-1].append((dado, indice_pagina + 1))

    encontrou_palavra = False
    indice_bucket_palavra = hash_custom(palavra, tamanho_bucket)

    # Medindo o tempo com timeit para o algoritmo de buckets
    start_time_bucket = timeit.default_timer()
    
    for sub_bucket in buckets[indice_bucket_palavra]:
        for dado, indice_pagina in sub_bucket:
            if dado == palavra:
                encontrou_palavra = True
                mensagem_bucket = f"Código bucket: A palavra '{palavra}' está na página {indice_pagina}."
                break
        if encontrou_palavra:
            break

    if not encontrou_palavra:
        mensagem_bucket = f"Código bucket: A palavra '{palavra}' não foi encontrada."

    elapsed_time_bucket = timeit.default_timer() - start_time_bucket
    mensagem_bucket += f" (Tempo de execução: {elapsed_time_bucket:.8f} segundos)"

    context = {'mensagem_serial': mensagem_serial, 'mensagem_bucket': mensagem_bucket}
    return render(request, 'paginas/busca_dado.html', context)