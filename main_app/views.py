from django.shortcuts import render
import time

# Create your views here.

def mainPage(request):
    return render(request,'paginas/home.html')

def dividePaginas(request,id):
    overflows=0
    colisoes=0

    dados = ['a', 'b', 'c','pedro', 'josé', 'ana', 'lana', 'joão', 'osvaldo', 'finn', 'gabriel', 'eduardo', 'davi', 'miguel', 'lara']

    dadosPorPagina = id

    def dividir_vetor(vetor, tamanho_subvetor):
        paginas = []
        for i in range(0, len(vetor), tamanho_subvetor):
            subvetor = vetor[i:i + tamanho_subvetor]
            paginas.append(subvetor)
        return paginas


        
    tamanho_bucket=5
    # Inicializa buckets como listas vazias
    buckets = [[] for _ in range(tamanho_bucket)]
    
    # Cria um mapeamento de dado para índice do subvetor (página)
    pagina_indices = {dado: i // dadosPorPagina for i, dado in enumerate(dados)}

    for dado in dados:
        # Obtém o valor ASCII do primeiro caractere do dado
        valor_ascii = ord(dado[0])
        # Calcula o índice do bucket com base no resto da divisão por 10
        indice_bucket = valor_ascii % tamanho_bucket
        # Obtém o índice da página
        indice_pagina = pagina_indices[dado]
        
        # Verifica se há um sub-bucket disponível ou precisa criar um novo
        if not buckets[indice_bucket]:
            buckets[indice_bucket].append([])
            

        elif len(buckets[indice_bucket][-1]) == 2:
            buckets[indice_bucket].append([])
            overflows=overflows+1

        #verifica se houve uma colisão
        if len(buckets[indice_bucket])>1:
            colisoes=colisoes+1
        
        # Adiciona a tupla ao último sub-bucket disponível
        buckets[indice_bucket][-1].append((dado, indice_pagina))
    

    # Divide os dados em páginas
    paginas = dividir_vetor(dados, dadosPorPagina)

    context={'buckets':buckets,'paginas':paginas,'colisoes':colisoes,'overflows':overflows}
    return render(request,'paginas/dados_organizados.html',context)


def busca(request,palavra,dadosPorPagina):
    dados = ['a', 'b', 'c', 'pedro', 'josé', 'ana', 'lana', 'joão', 'osvaldo', 'finn', 'gabriel', 'eduardo', 'davi', 'miguel', 'lara']


    pagina_indices = {dado: i // dadosPorPagina for i, dado in enumerate(dados)}
    


    #algoritmo serial
    start_time_serial = time.time()
    if palavra in pagina_indices:
        pagina = pagina_indices[palavra] + 1  # +1 para converter de índice (0-based) para número de página (1-based)
        mensagem_serial = f"codigo serial:A palavra '{palavra}' está na página {pagina}."
    else:
        mensagem_serial = f"codigo serial:A palavra '{palavra}' não foi encontrada."

    elapsed_time_serial = time.time() - start_time_serial
    mensagem_serial += f" (Tempo de execução: {elapsed_time_serial:.6f} segundos)"

    #algoritmo usando buckets
    start_time_serial = time.time()
    tamanho_bucket=5
    # Inicializa buckets como listas vazias
    buckets = [[] for _ in range(tamanho_bucket)]

    for dado in dados:
        # Obtém o valor ASCII do primeiro caractere do dado
        valor_ascii = ord(dado[0])
        # Calcula o índice do bucket com base no resto da divisão por 10
        indice_bucket = valor_ascii % tamanho_bucket
        # Obtém o índice da página
        indice_pagina = pagina_indices[dado]
        
        # Verifica se há um sub-bucket disponível ou precisa criar um novo
    tamanho_bucket = 5
    buckets = [[] for _ in range(tamanho_bucket)]

    for dado in dados:
        valor_ascii = ord(dado[0])
        indice_bucket = valor_ascii % tamanho_bucket
        indice_pagina = pagina_indices[dado]
        buckets[indice_bucket].append((dado, indice_pagina))

    encontrou_palavra = False
    indice_bucket_palavra = ord(palavra[0]) % tamanho_bucket

    for dado, indice_pagina in buckets[indice_bucket_palavra]:
        if dado == palavra:
            encontrou_palavra = True
            mensagem_bucket = f"codigo bucket: A palavra '{palavra}' está na página {indice_pagina + 1}."
            break

    if not encontrou_palavra:
        mensagem_bucket = f"codigo bucket: A palavra '{palavra}' não foi encontrada."

    elapsed_time_serial = time.time() - start_time_serial
    mensagem_bucket += f" (Tempo de execução: {elapsed_time_serial:.6f} segundos)"


    context = {'mensagem_serial': mensagem_serial, 'mensagem_bucket': mensagem_bucket}
    return render(request, 'paginas/busca_dado.html', context)