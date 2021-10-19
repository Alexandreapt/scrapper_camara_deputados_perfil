#Autor Alexandre P. Teixeira

from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

#Esse script captura informações sobre os deputados e faz um apurado ao final dizendo a quantidade ativo e inativo por partido

pagina_inicial = 1
pagina_maxima = 10
url_base = "https://www.camara.leg.br/deputados/quem-sao/resultado?search=&partido=&uf=&legislatura=56&sexo=&pagina="
resultados = {}

def printa_resultado():
    partidos = resultados.keys()
    
    print('{:^15}'.format('Partido') + " | " + '{:^15}'.format('Em exercício') + " | " + '{:^15}'.format('Afastado'))

    for p in partidos:
        print('{:^15}'.format(p) + " | " + '{:^15}'.format(str(resultados[p]['Em exercício'])) + " | " + '{:^15}'.format(str(resultados[p]['Afastado'])))

def apura_resultado(partido, em_exercicio):
    if not partido in resultados.keys():
        resultados.update({partido: {'Em exercício': 0, 'Afastado': 0}})

    if em_exercicio:
        resultados[partido]['Em exercício'] += 1
    else:
        resultados[partido]['Afastado'] += 1

def trata_captura(obj_pagina):
    objs_link_nome = obj_pagina.findAll(True, {'class':['lista-resultados__cabecalho']})
    if objs_link_nome:
        for obj_link_nome in objs_link_nome:
            texto_do_link = obj_link_nome.text.strip().upper()
            partido_estado = texto_do_link[texto_do_link.find("(")+1:texto_do_link.find(")")]
            partido = partido_estado.split("-")[0]
            em_exercicio = 'EM EXERCÍCIO' in texto_do_link
            apura_resultado(partido, em_exercicio)

def executa_captura(url):
    hdr = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'}
    req = Request(url, headers=hdr)
    page = urlopen(req)
    trata_captura(BeautifulSoup(page, 'html.parser'))

def inicia():
    print('Iniciando captura das informações')
    
    pagina_atual = 0
    while pagina_atual < pagina_maxima:
        pagina_atual += 1
        print('Capturando resultados da página ' + str(pagina_atual) + ' de ' + str(pagina_maxima))
        url = url_base + str(pagina_atual)
        executa_captura(url)

    print('Captura das informações finalizada')
    printa_resultado()


inicia()