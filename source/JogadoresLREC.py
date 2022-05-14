
import sys
sys.path.insert(1, '/Users/rjantao/Experiment/Liga/NewLiga')
import requests
import pandas as pd
url = 'https://liga.record.pt/conteudos/estatisticas.aspx'

import Param
import os
from time import sleep
import bs4
import Connect
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.keys import Keys
from importlib import reload
import Configurations as cfg


def webPlantel(driver,iparams):
   Connect.loginLigaRecord(driver,iparams)
   urlplantel = iparams['urlplantel']
   ini        = int(iparams['inicioplantel'])
   fim        = int(iparams['fimplantel'])
   driver.get(urlplantel)
   sleep(15)
   #botaoPesquisar    = driver.find_element_by_class_name('btn btn-primary btn-lg do-search').click()
   botaoPesquisar    = driver.find_element_by_xpath('/html/body/form/section[5]/div/div[1]/button').click()
   sleep(5)
   for i in range(ini,fim):
       botaoCarregarMais = driver.find_element_by_xpath('/html/body/form/section[5]/div/div[2]/div[2]/button[1]')
       #Não e efetuada validacao e botao carrega mais, a sua ultima iteracao é realizada por tentativa erro,
       #sendo neste caso 36  carregamentos no carregar mais
       #Multiplar o nº de carregamentos por 15, verificar os que faltam e colocar no maxjog
       #if i==36:
          #print(botaoCarregarMais)
       if botaoCarregarMais!=None:
          botaoCarregarMais.click()    

   
   source_page       = driver.page_source
   plantel_page      = bs4.BeautifulSoup(source_page.encode(Param.enc), 'html.parser')
   search_page       = plantel_page.find("div", {"class":"results col-sm-9 col-md-9"})   
           #Onde está definida a jornada
   ljogador = []
   lposicao =[]
   lvalorva = []
   lvalorvi =[]
   lclube   =[]
   #numero de jogadores
   maxjog  = len(search_page.find_all("article"))
   nonBreakSpace = '\xc2\xa0'
   for jog in range(0,maxjog):
      article_pag = search_page.find_all("article")[jog]
      identity_tag = article_pag.find("div", {"class":"identity"})
      jogador      = identity_tag.find("h6").text
      posicao      = identity_tag.find("p", {"class":"position"}).text
      clube      =  identity_tag.find_all('p')[1].text 
      #clube      = identity_tag.find_all("p")[1].text
      value_tag = article_pag.find("div", {"class":"value"})
      v_aux_valor_va  = value_tag.find("div", {"class":"value-va"}).text
      valor_va      =   v_aux_valor_va.replace("€","")\
                       .replace('.','')\
                       .replace('VA','')\
                       .replace(nonBreakSpace,'')\
                       .strip()
      v_aux_valor_vi  = value_tag.find("div", {"class":"value-vi"}).text
      valor_vi      = v_aux_valor_vi.replace("€","")\
                       .replace('.','')\
                       .replace('VI','')\
                       .replace(nonBreakSpace,'')\
                       .strip()    
      
      ljogador.append(jogador)
      lposicao.append(posicao)
      lvalorva.append(valor_va)
      lvalorvi.append(valor_vi)
      lclube.append(clube)

   dfjogador =pd.DataFrame({'Jogador':ljogador
                          ,'Clube':lclube
                           ,'Posicao': lposicao
                           ,'ValorAtual':lvalorva
                           ,'ValorInicial': lvalorvi
                           })

   return dfjogador

#?t=-1&p=2&pos=GR'

def estatisticas(ipos,ibrowse,iparams):
   url       = iparams['urlestatisticas']
   urlartigo = url + '?pos=' + ipos+'&t=-1'
   ibrowse.get(urlartigo)
   source_page = ibrowse.page_source
   html_page     = bs4.BeautifulSoup(source_page.encode(Param.enc), 'html.parser')
   estatisticas_pag = html_page.find("section", {"class": "last premium estatisticas"})
   #paginas_pag = estatisticas_pag.find("div", {"class": "paging"})
   #field_pag = paginas_pag.find("input", {"class": "page-field"})
   #maxpage   = field_pag.get('max')+1
   ljogador = []
   lclube = []
   ljogos = []
   ljogos_tit = []
   ljogos_comp = []
   lminutos = []
   lpts_record = []
   lpts_liga = []
   lgol_mar = []
   lgol_sof = []
   lpen_mar = []
   lpen_sof = []
   lpen_def = []
   lautogolos = []
   lver_dir = []
   lver_acuml =[]
   lamarelos = []
   lmelhor_jornada = []
   lrondas_lesionado = []
   lrondas_castigado = []
   #for pag in (1, maxpage):
   urlartigonew = url + '?pos=' + ipos+'&t=-1'
   ibrowse.get(urlartigonew)
   source_page = ibrowse.page_source
   html_page     = bs4.BeautifulSoup(source_page.encode(cfg.enc), 'html.parser')
   estatisticas_pag = html_page.find("section", {"class": "last premium estatisticas"})
   jog = estatisticas_pag.find_all("li", {"class": "player pager-scroller"})
   indfim =len(jog) 
   for ind_jog in range(0, indfim):
        ident_jog_tag = estatisticas_pag.find_all("li", {"class": "player pager-scroller"})[ind_jog]
        jogador = ident_jog_tag.find('h6').text
        clube   = ident_jog_tag.find("p", {"class": "team"}).text
        jogos_tag    = estatisticas_pag.find_all("ul", {"class": "row"})[0]
        jogos       = jogos_tag.find_all("li", {"class": "pager-scroller"})[ind_jog].text
        jogos_tit_tag = estatisticas_pag.find_all("ul", {"class": "row"})[1]
        jogos_tit    = jogos_tit_tag.find_all("li", {"class": "pager-scroller"})[ind_jog].text
        jogos_comp_tag = estatisticas_pag.find_all("ul", {"class": "row"})[2]
        jogos_comp = jogos_comp_tag.find_all("li", {"class": "pager-scroller"})[ind_jog].text
        minutos_tag = estatisticas_pag.find_all("ul", {"class": "row"})[3]
        minutos = minutos_tag.find_all("li", {"class": "pager-scroller"})[ind_jog].text
        pts_record_tag = estatisticas_pag.find_all("ul", {"class": "row"})[5]
        pts_record = pts_record_tag.find_all("li", {"class": "pager-scroller"})[ind_jog].text
        pts_liga_tag = estatisticas_pag.find_all("ul", {"class": "row"})[6]
        pts_liga = pts_liga_tag.find_all("li", {"class": "pager-scroller"})[ind_jog].text
        gol_mar_tag = estatisticas_pag.find_all("ul", {"class": "row"})[7]
        gol_mar = gol_mar_tag.find_all("li", {"class": "pager-scroller"})[ind_jog].text
        gol_sof_tag = estatisticas_pag.find_all("ul", {"class": "row"})[8]
        gol_sof = gol_sof_tag.find_all("li", {"class": "pager-scroller"})[ind_jog].text
        pen_mar_tag = estatisticas_pag.find_all("ul", {"class": "row"})[9]
        pen_mar = pen_mar_tag.find_all("li", {"class": "pager-scroller"})[ind_jog].text
        pen_sof_tag = estatisticas_pag.find_all("ul", {"class": "row"})[10]
        pen_sof = pen_sof_tag.find_all("li", {"class": "pager-scroller"})[ind_jog].text
        pen_def_tag = estatisticas_pag.find_all("ul", {"class": "row"})[11]
        pen_def = pen_sof_tag.find_all("li", {"class": "pager-scroller"})[ind_jog].text
        autogolos_tag = estatisticas_pag.find_all("ul", {"class": "row"})[12]
        autogolos = autogolos_tag.find_all("li", {"class": "pager-scroller"})[ind_jog].text
        ver_dir_tag = estatisticas_pag.find_all("ul", {"class": "row"})[13]
        ver_dir = ver_dir_tag.find_all("li", {"class": "pager-scroller"})[ind_jog].text
        ver_acuml_tag = estatisticas_pag.find_all("ul", {"class": "row"})[14]
        ver_acuml = ver_acuml_tag.find_all("li", {"class": "pager-scroller"})[ind_jog].text
        amarelos_tag = estatisticas_pag.find_all("ul", {"class": "row"})[15]
        amarelos = amarelos_tag.find_all("li", {"class": "pager-scroller"})[ind_jog].text
        melhor_jornada_tag = estatisticas_pag.find_all("ul", {"class": "row"})[16]
        melhor_jornada = melhor_jornada_tag.find_all("li", {"class": "pager-scroller"})[ind_jog].text
        rondas_lesionado_tag = estatisticas_pag.find_all("ul", {"class": "row"})[17]
        rondas_lesionado = rondas_lesionado_tag.find_all("li", {"class": "pager-scroller"})[ind_jog].text
        rondas_castigado_tag = estatisticas_pag.find_all("ul", {"class": "row"})[18]
        rondas_castigado = rondas_castigado_tag.find_all("li", {"class": "pager-scroller"})[ind_jog].text
        ind_jog = 5
        ljogador.append(jogador)
        lclube.append(clube)
        ljogos.append(jogos)
        ljogos_tit.append(jogos_tit )
        ljogos_comp.append(jogos_comp)
        lminutos.append(minutos)
        lpts_record.append(pts_record)
        lpts_liga.append(pts_liga)
        lgol_mar.append(gol_mar)
        lgol_sof.append(gol_sof)
        lpen_mar.append(pen_mar)
        lpen_sof.append(pen_sof)
        lpen_def.append(pen_def)
        lautogolos.append(autogolos)
        lver_dir.append(ver_dir)
        lver_acuml.append(ver_acuml)
        lamarelos.append(amarelos)
        lmelhor_jornada.append(melhor_jornada)
        lrondas_lesionado.append(rondas_lesionado)
        lrondas_castigado.append(rondas_castigado)
   df_jogador =pd.DataFrame({'NomeJogador':ljogador
                              ,'Clube':lclube
                              ,'Jogos':ljogos
                              ,'JogosTitular': ljogos_tit
                              ,'JogosCompletos':ljogos_comp
                              ,'MinutosJogados' :lminutos
                              ,'PontosRecord':lpts_record
                              ,'PontosLiga':lpts_liga
                              ,'GolosMarcados':lgol_mar
                              ,'GolosSofridos':lgol_sof
                              , 'PenMarcados': lpen_mar
                              , 'PenSofridos': lpen_sof
                              , 'PenDefendidos': lpen_def
                              , 'PenMarcados': lpen_mar
                              , 'Autogolos': lautogolos
                              , 'VermelhosDiretos': lver_dir
                              , 'VermelhosAcumulados': lver_acuml
                               , 'Amarelos': lamarelos
                                , 'MelhorJornada': lmelhor_jornada
                                ,'RondasLesionado':lrondas_lesionado
                              , 'RondasCastigado': lrondas_castigado})
   df_jogador['Posicao'] = ipos
   return df_jogador

def WebEstatisticas(iparams):
   incrementproxy = 0
   proxies = cfg.getProxy()
   dfjogtot=pd.DataFrame([])
   posicaos = ['GR', 'DF', 'MD', 'AV']
   for pos in posicaos:
       browse = Param.runDriver(proxies,incrementproxy)
       Connect.loginLigaRecord(browse,iparams)
       df_jog  = pd.DataFrame([])
       df_jog = estatisticas(pos, browse,iparams)
       dfjogtot = dfjogtot.append(df_jog, ignore_index=True)
       browse.close()
       incrementproxy = incrementproxy +1

   return dfjogtot

def NomeFicheiro(iepoca,itipo):
   fich =None
   if itipo == 'VALORPLANTEL':
      fich = iepoca + itipo
   return  fich 


def readJogadoresLREC(iparams):
   listajoglrec     = iparams['dirdata'] + iparams['listajoglrec']
   dfjogadoresLREC  = Param.readFile(listajoglrec)
   dfjogadoresLREC  = dfjogadoresLREC .rename({'ValorAtual': 'valoratual'
                                            ,"ValorInicial": 'valorinicial'
                                            ,"Jogador": 'jogador'
                                            ,"Clube": 'clube'
                                            ,"Posicao": 'posicao'
                                   },axis=1) 
   dfjogadoresLREC["posicao"].replace("Guarda Redes", "GR", inplace=True) 
   dfjogadoresLREC["posicao"].replace("Defesa", "DF", inplace=True) 
   dfjogadoresLREC["posicao"].replace("Médio", "MD", inplace=True) 
   dfjogadoresLREC["posicao"].replace("Avançado", "AV", inplace=True)                                
   return dfjogadoresLREC


def writeValorPlantel(iepoca):
   incrementproxy = 0
   proxies = cfg.getProxy()
   #ultima jornada do campeonato
   browse = Param.runDriver(proxies,incrementproxy)
   dfjogador = webPlantel(browse)
   fichValorPlantel = NomeFicheiro(iepoca,'VALORPLANTEL')
   Param.fileGeneration(dfjogador, fichValorPlantel, iepoca)


def writePlantel(iparams):
  browse      = Param.runDriverProxy(0)  
  jogadoresLREC  = webPlantel(browse,iparams)
  print(jogadoresLREC)
  listajoglrec     = iparams['dirdata'] + iparams['listajoglrec']
  Param.writeTabularFile(jogadoresLREC, listajoglrec)


def writeEstatisticas(iparams):  
  jogadoresLREC         = WebEstatisticas(iparams)
  listajoglrecest       = iparams['dirdata'] + iparams['listajoglrecest']
  Param.writeTabularFile(jogadoresLREC, listajoglrecest)


if __name__ == "__main__":
  try:
   params = Param.config(Param.configFile, 'ligarecord')   
   writePlantel(params)
   #writeEstatisticas(params)
  except KeyboardInterrupt:
     print('\n')

