import json
from pprint import pprint

def pega_dados():
    with open('ano2018.json') as f:
        dados = json.load(f)
    return dados

dados2018 = pega_dados()


def nome_do_time(dados,id_numerica):
    return dados['equipes'][id_numerica]['nome-comum']


def id_campeao(dados):
    return dados['fases']['2700']['classificacao']['grupo']['Único'][0]


def nome_campeao(dados):
    return dados['equipes'][id_campeao(dados)]['nome-comum']
    

def qtos_libertadores(dados):
    qtdLiberta = dados['fases']['2700']['faixas-classificacao']['classifica1']['faixa'].split('-')
    return int(qtdLiberta[1])


def ids_dos_melhor_classificados(dados,numero_de_times):
    lista = dados['fases']['2700']['classificacao']['grupo']['Único']
    melhores = []
    for id in range(0, numero_de_times):
        melhores.append(lista[id])
    return melhores


def classificados_libertadores(dados):
    return ids_dos_melhor_classificados(dados,qtos_libertadores(dados))


def nomes_classificados_libertadores(dados):
    id = classificados_libertadores(dados)
    nome = []
    for i in id:
        nome.append(nome_do_time(dados, i))
    return nome


def ids_dos_times_de_um_jogo(dados,id_jogo):
    time1 = dados['fases']['2700']['jogos']['id'][id_jogo]['time1']
    time2 = dados['fases']['2700']['jogos']['id'][id_jogo]['time2']
    return time1,time2


def nomes_dos_times_de_um_jogo(dados,id_jogo):
    time1 = nome_do_time(dados,ids_dos_times_de_um_jogo(dados,id_jogo)[0])
    time2 = nome_do_time(dados,ids_dos_times_de_um_jogo(dados,id_jogo)[1])
    return time1, time2


def id_do_time(dados,nome_time):
    id = ''
    for i in dados['equipes']:
        if dados['equipes'][i]['nome-comum'] == nome_time:
            id = i
    if id == '':
        return 'nao encontrado'
    else:
        return id


def datas_de_jogo(dados):
    datas = []
    for i in dados['fases']['2700']['jogos']['data']:
        datas.append(i)
    return datas


def data_de_um_jogo(dados,id_jogo):
    if id_jogo in dados['fases']['2700']['jogos']['id']:
        return dados['fases']['2700']['jogos']['id'][id_jogo]['data']
    else:
        return 'nao encontrado'


def dicionario_id_estadio_e_nro_jogos(dados):
    dic = {}
    for i in dados['fases']['2700']['jogos']['id']:
        if dados['fases']['2700']['jogos']['id'][i]['estadio_id'] in dic.keys():
            dic[dados['fases']['2700']['jogos']['id'][i]['estadio_id']] += 1
        else:
            dic[dados['fases']['2700']['jogos']['id'][i]['estadio_id']] = 1
    return dic


def busca_imprecisa_por_nome_de_time(dados,nome_time):
    lista = []
    equipes = dados['equipes']
    for i in equipes:
        if nome_time in equipes[i]['nome-comum'] \
            or nome_time in equipes[i]['nome-slug'] \
            or nome_time in equipes[i]['sigla'] \
            or nome_time in equipes[i]['nome']:
            lista.append(i)
    return lista


def ids_de_jogos_de_um_time(dados,time_id):
    lista = []
    jogos = dados['fases']['2700']['jogos']['id']
    for i in jogos:
        if time_id == jogos[i]['time1'] or time_id == jogos[i]['time2']:
            lista.append(i)
    return lista


def datas_de_jogos_de_um_time(dados,nome_time):
    lista = []
    equipes = dados['equipes']
    jogos = dados['fases']['2700']['jogos']['id']
    for i in jogos:
        if nome_time == equipes[jogos[i]['time1']]['nome-comum'] \
            or nome_time == equipes[jogos[i]['time2']]['nome-comum']:
            lista.append(jogos[i]['data'])
    return lista


def dicionario_de_gols(dados):
    dic = {}
    jogos = dados['fases']['2700']['jogos']['id']
    for i in jogos:
        if jogos[i]['time1'] in dic.keys():
            dic[jogos[i]['time1']] += int(jogos[i]['placar1'])
        else:
            dic[jogos[i]['time1']] = int(jogos[i]['placar1'])
        if jogos[i]['time2'] in dic.keys():
            dic[jogos[i]['time2']] += int(jogos[i]['placar2'])
        else:
            dic[jogos[i]['time2']] = int(jogos[i]['placar2'])
    return dic


def time_que_fez_mais_gols(dados):
    gols_por_time = dicionario_de_gols(dados)
    gols = 0
    time = ''
    for i in gols_por_time:
        if int(gols_por_time[i]) > gols:
            gols = int(gols_por_time[i])
            time = i
    return time

'''
Da mesma forma que podemos obter a informacao dos times classificados
para a libertadores, também podemos obter os times na zona de rebaixamento

A proxima funcao recebe apenas o dicionário de dados do brasileirao,
e retorna uma lista com as ids dos times rebaixados.

Consulte a zona de rebaixamento do dicionário de dados, nao deixe
ela chumbada da função

    lista = dados['fases']['2700']['classificacao']['grupo']['Único']
    melhores = []
    for id in range(0, numero_de_times):
        melhores.append(lista[id])
    return melhores

'''
def rebaixados(dados):
    lista = dados['fases']['2700']['classificacao']['grupo']['Único']
    posicaoRebaixados = dados['fases']['2700']['faixas-classificacao']['classifica3']['faixa'].split('-')
    piores = []
    for i in range(int(posicaoRebaixados[0]) - 1, int(posicaoRebaixados[1])):
        piores.append(lista[i])
    return piores


def classificacao_do_time_por_id(dados,time_id):
    tabela = dados['fases']['2700']['classificacao']['grupo']['Único']
    classificacao = ''
    for i in tabela:
        if time_id == i:
            classificacao = tabela.index(i)+1
    if classificacao == '':
        return 'nao encontrado'
    else:
        return classificacao

print(rebaixados(dados2018))

