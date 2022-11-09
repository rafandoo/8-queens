import numpy as np

# Número de indivíduos que serão selecionados para reprodução
TAMANHO_POPULACAO = 100

# Número de gerações que serão geradas
NUMERO_GERACOES = 10000

# Número de estados possíveis para cada rainha
ESTADOS = 8

# Probabilidade de mutação
MUTACAO = 0.5

# Taxa de cruzamento
TAXA_CRUZAMENTO = 0.5

def gerarPopulacaoInicial(tamanho_populacao, estados):
    """Gera uma população inicial de tamanho = tamanho_populacao com estados = ESTADOS"""
    populacao = []
    for i in range(tamanho_populacao):
        populacao.append(np.random.randint(0, estados, size=estados))
    return populacao

def fitness(populacao):
    """ 
    Calcula o fitness de cada indivíduo da população
    
    O fitness é calculado tendo como base o número de colisões/ataques
    que cada rainha tem sobre as demais. Levendo em consideração que
    as rainhas não podem estar na mesma linha, coluna ou diagonal, 
    para que o individuo seja perfeito, o fitness deve ser 0.
    """
    fit = []
    for individuo in populacao:
        colisoes = 0
        for i in range(len(individuo)):
            for j in range(i + 1, len(individuo)):
                if individuo[i] == individuo[j]:
                    colisoes += 1
                if individuo[i] - individuo[j] == i - j:
                    colisoes += 1
                if individuo[i] - individuo[j] == j - i:
                    colisoes += 1
        fit.append(colisoes)
    return fit

def fitnessIndividuo(individuo):
    # função de fitness por indivíduo
    colisoes = 0
    for i in range(len(individuo)):
        for j in range(i + 1, len(individuo)):
            if individuo[i] == individuo[j]:
                colisoes += 1
            if individuo[i] - individuo[j] == i - j:
                colisoes += 1
            if individuo[i] - individuo[j] == j - i:
                colisoes += 1
    return colisoes

def selecaoCrossover(populacao):
    """
    Seleciona os indivíduos que serão reproduzidos e realiza o crossover
    
    A seleção dos pais, ou seja os indivíduos que serão reproduzidos, é feita
    tendo como base o fitness de cada indivíduo. Os indivíduos com fitness menor
    são selecionados, após isto o fitness do indivíduo selecionado é atribuido o valor
    de 1000 para que ele não seja selecionado novamente. O crossover é realizado 
    com base na taxa de cruzamento, e pelo ponto de corte (é escolhido aleatoriamente,
    dentro do tamanho do indivíduo) é feito o cruzamento dos indivíduos selecionados.
    
    Os filho gerados são adicionados a uma nova população que será retornada.
    """
    fit = fitness(populacao)
    populacao = np.array(populacao)
    
    pais = []
    for i in range(len(populacao)):
        pais.append(populacao[np.argmin(fit)])
        fit[np.argmin(fit)] = 1000
    pais = np.array(pais)
    
    filhos = []
    for i in range(0, len(pais), 2):
        if np.random.random() < TAXA_CRUZAMENTO:
            ponto_corte = np.random.randint(1, ESTADOS)
            filho1 = np.concatenate((pais[i, :ponto_corte], pais[i + 1, ponto_corte:]))
            filho2 = np.concatenate((pais[i + 1, :ponto_corte], pais[i, ponto_corte:]))
            filhos.append(filho1)
            filhos.append(filho2)
        else:
            filhos.append(pais[i])
            filhos.append(pais[i + 1])

    return filhos

def mutacao(populacao):
    """
    Realiza a mutação dos indivíduos da população
    tendo como base a probabilidade de mutação,
    logo se o número aleatório gerado (entre {0.0 e 1.0})
    for menor que a probabilidade de mutação, o indivíduo
    sofrerá mutação. Esta qual consiste em trocar o valor 
    de um dos estados do indivíduo por um valor aleatório.
    """
    for i in range(len(populacao)):
        if np.random.random() < MUTACAO:
            populacao[i][np.random.randint(0, ESTADOS)] = np.random.randint(0, ESTADOS)
    return populacao

def imprimeTabuleiro(individuo):
    # Essa função imprime o tabuleiro especificado com as rainhas posicionadas
    tabuleiro = np.zeros((ESTADOS, ESTADOS))
    for i in range(len(individuo)):
        tabuleiro[individuo[i]][i] = 1
    
    # trocar 1 por 👑
    tabuleiro = np.where(tabuleiro == 1, '👑', tabuleiro)

    # trocar 0 por 🟦
    tabuleiro = np.where(tabuleiro == '0.0', '🟦', tabuleiro)

    return tabuleiro

def estatisticas(geracao, melhorIndividuo):
    print('Numero de gerações: ', geracao)
    print('Numero de individuos gerados: ', geracao * TAMANHO_POPULACAO)
    print('Melhor indivíduo: ', melhorIndividuo)
    print('Fitness do melhor indivíduo: ', fitnessIndividuo(melhorIndividuo))
    print('Tabuleiro: ')
    print(imprimeTabuleiro(melhorIndividuo))

def algoritmoGenetico():
    populacao = gerarPopulacaoInicial(TAMANHO_POPULACAO, ESTADOS)
    geracao = 0
    for i in range(NUMERO_GERACOES):
        filhos = selecaoCrossover(populacao)
        filhos = np.array(filhos)
        filhos = mutacao(filhos)
        populacao = filhos
        if np.min(fitness(populacao)) == 0:
            break
        # print("Geração: ", i)
        # print("Melhor indivíduo: ", populacao[np.argmin(fitness(populacao))])
        geracao += 1
    return geracao, populacao[np.argmin(fitness(populacao))]

ag = algoritmoGenetico()
estatisticas(ag[0], ag[1])
