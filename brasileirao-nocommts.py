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


import unittest
try:
    from brasileirao_gabarito import *
except:
    pass
class TestClientes(unittest.TestCase):
    
    def test_000_nome_do_time(self):
        dados = pega_dados()
        self.assertEqual(nome_do_time(dados,'1'),'Flamengo')
        self.assertEqual(nome_do_time(dados,'695'),'Chapecoense')
    
    def test_001_id_campeao(self):
        dados = pega_dados()
        self.assertEqual(id_campeao(dados),'17')
        #vou falsificar os dados pra testar se vc esta lendo direito da estrutura
        dados['fases']['2700']['classificacao']['grupo']['Único'].pop(0)
        self.assertEqual(id_campeao(dados),'1')
    
    def test_002_nome_campeao(self):
        dados = pega_dados()
        self.assertEqual(nome_campeao(dados),'Palmeiras')
        #vou falsificar os dados pra testar se vc esta lendo direito da estrutura
        dados['fases']['2700']['classificacao']['grupo']['Único'].pop(0)
        self.assertEqual(nome_campeao(dados),'Flamengo')
    
    def test_003_qtos_libertadores(self):
        dados = pega_dados()
        self.assertEqual(qtos_libertadores(dados),6)
        #vou falsificar os dados pra testar se vc esta lendo direito da estrutura
        dados['fases']['2700']['faixas-classificacao']['classifica1']['faixa']='1-8'
        self.assertEqual(qtos_libertadores(dados),8)

    
    def test_004_ids_dos_melhor_classificados(self):
        dados = pega_dados()
        self.assertEqual(ids_dos_melhor_classificados(dados,10),["17","1","15","13","24","4","3","9","5","22"])
        self.assertEqual(ids_dos_melhor_classificados(dados,5),["17","1","15","13","24"])
        self.assertEqual(ids_dos_melhor_classificados(dados,3),["17","1","15"])
    
    def test_005_classificados_libertadores(self):
        dados = pega_dados()
        self.assertEqual(classificados_libertadores(dados),["17","1","15","13","24","4"])
        #vou falsificar os dados pra testar se vc esta lendo direito da estrutura
        dados['fases']['2700']['faixas-classificacao']['classifica1']['faixa']='1-8'
        self.assertEqual(classificados_libertadores(dados),["17","1","15","13","24","4","3","9"])
    
    def test_006_nomes_classificados_libertadores(self):
        dados = pega_dados()
        #vou falsificar os dados pra testar se vc esta lendo direito da estrutura
        dados['fases']['2700']['faixas-classificacao']['classifica1']['faixa']='1-3'
        self.assertEqual(nomes_classificados_libertadores(dados),["Palmeiras","Flamengo","Internacional"])
    
    def test_007_ids_dos_times_de_um_jogo(self):
        dados = pega_dados()
        t1,t2 = ids_dos_times_de_um_jogo(dados,'102099')
        self.assertTrue(t1 in ['5','17'])
        self.assertTrue(t2 in ['5','17'])
        t1,t2 = ids_dos_times_de_um_jogo(dados,'102109')
        self.assertTrue(t1 in ['1','26'])
        self.assertTrue(t2 in ['1','26'])
    
    def test_008_nomes_dos_times_de_um_jogo(self):
        dados = pega_dados()
        t1,t2 = nomes_dos_times_de_um_jogo(dados,'102099')
        self.assertTrue(t1 in ['Botafogo','Palmeiras'])
        self.assertTrue(t2 in ['Botafogo','Palmeiras'])
        t1,t2 = nomes_dos_times_de_um_jogo(dados,'102106')
        self.assertTrue(t1 in ['Chapecoense','Vasco'])
        self.assertTrue(t2 in ['Chapecoense','Vasco'])
    
    def test_009_id_do_time(self):
        dados = pega_dados()
        self.assertEqual(id_do_time(dados,'Cruzeiro'),'9')
        self.assertEqual(id_do_time(dados,'Athletico'),'3')
    
    

    def test_010_datas_de_jogo(self):
        dados = pega_dados()
        datas = datas_de_jogo(dados)
        self.assertEqual(len(datas), 107)
        self.assertTrue('2018-04-14' in datas)
        self.assertTrue('2018-07-26' in datas)
        self.assertTrue('2018-10-26' in datas)

    def test_011_datas_de_jogo_teste_2(self):
        dados = pega_dados()
        #deleto a data '14 de abril'
        del dados['fases']['2700']['jogos']['data']['2018-04-14']
        #e todos os jogos que ocorreram nela
        del dados['fases']['2700']['jogos']['id']['102094']
        del dados['fases']['2700']['jogos']['id']['102097']
        del dados['fases']['2700']['jogos']['id']['102101']
        datas = datas_de_jogo(dados)
        self.assertEqual(len(datas), 106)
        self.assertFalse('2018-04-14' in datas)
        self.assertTrue('2018-07-26' in datas)
        self.assertTrue('2018-10-26' in datas)

    def test_012_data_de_um_jogo(self):
        dados = pega_dados()
        self.assertEqual(data_de_um_jogo(dados,'102132'),'2018-05-06')
        self.assertEqual(data_de_um_jogo(dados,'102187'),'2018-06-06')
        self.assertEqual(data_de_um_jogo(dados,'102540'),'nao encontrado')

    def test_013_dicionario_id_estadio_e_nro_jogos(self):
        dados = pega_dados()
        estadios = dicionario_id_estadio_e_nro_jogos(dados)
        self.assertEqual(estadios['72'],16)
        #vou falsificar os dados pra testar se vc esta lendo direito da estrutura
        dados['fases']['2700']['jogos']['id']['102097']['estadio_id']='72'
        estadios = dicionario_id_estadio_e_nro_jogos(dados)
        self.assertEqual(estadios['72'],17)
    
    def test_014_busca_imprecisa_por_nome_de_time(self):
        dados = pega_dados()
        ids_times = busca_imprecisa_por_nome_de_time(dados,'Paulo')
        self.assertTrue('24' in ids_times)
        ids_times = busca_imprecisa_por_nome_de_time(dados,'SPA')
        self.assertTrue('24' in ids_times)
        ids_times = busca_imprecisa_por_nome_de_time(dados,'anto')
        self.assertTrue('22' in ids_times)
    
    def test_015_ids_de_jogos_de_um_time(self):
        dados = pega_dados()
        jogos_chapeco = ids_de_jogos_de_um_time(dados,'695')
        self.assertEqual(len(jogos_chapeco),38)
        self.assertTrue('102330' in jogos_chapeco)
        self.assertTrue('102422' in jogos_chapeco)
        jogos_santos = ids_de_jogos_de_um_time(dados,'22')
        self.assertEqual(len(jogos_santos),38)
        self.assertTrue('102208' in jogos_santos)
        self.assertTrue('102259' in jogos_santos)
    
    def test_016_datas_de_jogos_de_um_time(self):
        dados = pega_dados()
        datas_santos = datas_de_jogos_de_um_time(dados,'Santos')
        self.assertEqual(len(datas_santos),38)
        self.assertTrue('2018-04-21' in datas_santos)
        self.assertTrue('2018-10-13' in datas_santos)
        datas_chapeco = datas_de_jogos_de_um_time(dados,'Chapecoense')
        self.assertEqual(len(datas_chapeco),38)
        self.assertTrue('2018-11-25' in datas_chapeco)
        self.assertTrue('2018-12-02' in datas_chapeco)
    
    def test_017_dicionario_de_gols(self):
        dados = pega_dados()
        dic_gols = dicionario_de_gols(dados)

        self.assertEqual(dic_gols['695'],34)
        #vou falsificar os dados pra testar se vc esta lendo direito da estrutura
        dados['fases']['2700']['jogos']['id']['102330']['placar2']=1
        dic_gols = dicionario_de_gols(dados)
        self.assertEqual(dic_gols['695'],35)
        dados['fases']['2700']['jogos']['id']['102422']['placar2']=2
        dic_gols = dicionario_de_gols(dados)
        self.assertEqual(dic_gols['695'],36)
        dados['fases']['2700']['jogos']['id']['102422']['placar2']=12
        dic_gols = dicionario_de_gols(dados)
        self.assertEqual(dic_gols['695'],46)
    
    def test_018_time_que_fez_mais_gols(self):
        dados = pega_dados()
        time = time_que_fez_mais_gols(dados)
        self.assertEqual(time,'17')
        #vou falsificar os dados pra testar se vc esta lendo direito da estrutura
        dados['fases']['2700']['jogos']['id']['102422']['placar2']=120
        time = time_que_fez_mais_gols(dados)
        self.assertEqual(time,'695')


    def test_019_rebaixados(self):
        dados = pega_dados()
        self.assertEqual(rebaixados(dados),['76', '26', '21', '18'])
        #vou falsificar os dados pra testar se vc esta lendo direito da estrutura
        dados['fases']['2700']['faixas-classificacao']['classifica3']['faixa']='15-20'
        self.assertEqual(rebaixados(dados),['33','25','76', '26', '21', '18'])

    def test_020_classificacao_do_time_por_id(self):
        dados = pega_dados()
        self.assertEqual(classificacao_do_time_por_id(dados,'17'),1)
        self.assertEqual(classificacao_do_time_por_id(dados,'30'),11)
        self.assertEqual(classificacao_do_time_por_id(dados,'695'),14)
        self.assertEqual(classificacao_do_time_por_id(dados,'1313'),'nao encontrado')


def runTests():
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestClientes)
        unittest.TextTestRunner(verbosity=2,failfast=True).run(suite)

def pega_dados():
    with open('ano2018.json') as f:
        dados = json.load(f)
    return dados

dados2018 = pega_dados()

if __name__ == '__main__':
    runTests()
