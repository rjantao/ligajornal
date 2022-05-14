# -*- coding: utf-8 -*-
"""
Created on Sat Jul 07 22:11:55 2018

@author: rjantao
"""

import Configurations as cfg
from selenium.webdriver.common.action_chains import ActionChains
from   time import sleep
import bs4
import pandas as pd
import Param
import Connect

fileEquipa = "/Users/rjantao/Experiment/Liga/DataLiga/Liga1920/Equipa.json"
   
def webEquipas(driver,iparams):
   gerirEquipas = iparams['gerirequipas']
   driver.get(gerirEquipas)  
   sleep(15)   
   #Carregar no ver mais
   #driver.find_element_by_css_selector("a[href='../Common/UserControls/home/#']").click()
   equi_source = driver.page_source
   equi_page   = bs4.BeautifulSoup(equi_source.encode(cfg.enc),'html.parser')
   aux_list = equi_page.find("div", {"id": "topContainer_top_top_ctl00_listTeams"}) 
   nomeEquipa = []
   idEquipa   =[]
   for aux_ul in aux_list.find_all('ul'):
      aux_li= aux_ul.find('li')   
      aux_equipa  =   aux_li.find('input').get('value')
      aux_id_equipa = aux_li.find('input').get('id').replace('teamName','')  
      nomeEquipa.append(aux_equipa) 
      idEquipa.append(aux_id_equipa)   
   dfEquipa =pd.DataFrame({'idEquipa':idEquipa
                    , 'nomeEquipa': nomeEquipa}) 
   
   return dfEquipa


def webRankingsEquipaTotal(driver,iparams):  
   lnkrank = iparams['lnkrank']
   inirank = iparams['inicioranking']
   fimrank = iparams['fimranking']
   driver.get(lnkrank)
   ranking = []
   nomeEquipa = []
   pontos = []
   utilizador = []
   sleep(10)
   for i in range(inirank, fimrank):     
      menu = driver.find_element_by_link_text(str(i))
      actions = ActionChains(driver)
      actions.move_to_element(menu)
      actions.click(menu)
      actions.perform()
      source_page=driver.page_source
      driver.refresh
      jog_page = bs4.BeautifulSoup(source_page.encode(Param.enc), 'html.parser')
      list_page = jog_page.find("div", {"class": "lista-equipas"})
      for row_jog in list_page.find_all("article", {"class":"row_equipa"}):
         vRanking = row_jog.find("div", {"class": "posicao"}).text     
         vNomeEquipa   = row_jog.find("p", {"class": "nome"}).text
         vUtilizador    = row_jog.find("p", {"class": "user"}).text
         vPontosTotais = row_jog.find("div", {"class": "totais"}).text
         ranking.append(vRanking)
         nomeEquipa.append(vNomeEquipa)
         pontos.append(vPontosTotais)
         utilizador.append(vUtilizador)

   dfRankingEquipas =pd.DataFrame({'Ranking':ranking
                             ,'NomeEquipa':nomeEquipa
                             ,'PontosTotais':pontos
                             ,'Utilizador':utilizador})  
   

   #dfRankingEquipas.to_json(r"/Users/rjantao/Experiment/Liga/DataLiga/Liga1920/rankEquipa4jorn"+str(ini)+"_"+str(fim)+".json")
   return dfRankingEquipas

def readEquipas(iparams):
   dirData     = iparams['dirdata']
   fileEquipas = iparams['equipasfile']
   dirFile     = dirData + fileEquipas
   equipas     = pd.read_json (dirFile)
   equipas        = equipas.rename({'idEquipa': 'idequipa'
                                   },axis=1) 
   return equipas
# funcao de controle
def IdEquipa(iparams):
   NomeEquipas = readEquipas(iparams)
   #print(NomeEquipas)
   v_idEquipa = NomeEquipas.loc[1,'idEquipa'] 
   ##print(v_idEquipa)
   return v_idEquipa

def writeEquipas(iparams):
   browse  = Param.runDriverProxy(0)
   Connect.loginLigaRecord(browse,iparams)
   dirData = iparams['dirdata']
   fileEquipas = iparams['equipasfile']
   equipas = webEquipas(browse,iparams) 
   equipas.to_json(dirData+fileEquipas) 

if __name__ == "__main__":
  try:
   params = Param.config(Param.configFile, 'ligarecord')   
   writeEquipas(params)
   equipas = readEquipas(params)
   print(equipas)
   
  except KeyboardInterrupt:
     print('\n')

   



      


