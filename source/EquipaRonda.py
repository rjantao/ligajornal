# -*- coding: utf-8 -*-
"""
Created on Sat Dec 01 08:55:45 2018

@author: rjantao
"""
import os
import bs4
import pandas as pd
import Param
import Equipa
from time import sleep
import Connect
import Configurations as cfg

def webEquipaRonda(driver,iparams,ron):
   equipas = Equipa.readEquipas(iparams)  
   lnk_equi_ron =  iparams['lnk_equi_ron']
   max_val=len(equipas) 
   lidequipa   =[]  
   lranking   =[]
   ltact    =[]
   lvar     =[]
   lpts_tot =[]
   lpts_ron =[]
   lsld_disp=[]
   lval11_titular=[]
   lval_plantel=[] 
   lronda      =[] 

   for i in range(0,max_val):
      driver.get(lnk_equi_ron+str(equipas.iloc[i, 0])+'&id_round='+str(ron)) 
      sleep(15)
      equi_source = driver.page_source
      equi_page   = bs4.BeautifulSoup(equi_source.encode(Param.enc),'html.parser') 
      nonBreakSpace = '\xc2\xa0'
      html_ative =  equi_page.find("div", {"class": "teams active"})
              
      pts_tot = html_ative.find("h3",{"id":"main_main_ctl00_pointsTotal"}).text
      pts_rnd = html_ative.find("h3",{"id":"main_main_ctl00_pointsRound"}).text
      
      rank_tag =html_ative.find("li", {"id": "main_main_ctl00_rank"})
      ranking     =rank_tag.find('h3').text.replace("º","").replace("\xa0","").replace("\xc2","")
      var      =rank_tag.find('i').text 
      tact_tag     =html_ative.find("div",{"id":"main_main_ctl00_teamFormation"})
      tact     =tact_tag.find('p').text
      team_details  = equi_page.find("div", {"id": "main_main_ctl00_teamDetails"}) 
      sld_disp      =team_details.find_all('b')[-1].text.replace("€","").replace("\xa0","").replace("\xc2","")
      val11_titular =team_details.find_all('b')[0].text.replace("€","").replace("\xa0","").replace("\xc2","")
      val_plantel   =team_details.find_all('b')[1].text.replace("€","").replace("\xa0","").replace("\xc2","")         
      lidequipa.append(equipas.iloc[i, 0])
      lranking.append(ranking)
      ltact.append(tact) 
      lvar.append(var)
      lpts_tot.append(pts_tot)
      lpts_ron.append(pts_rnd)
      lsld_disp.append(sld_disp)
      lval11_titular.append(val11_titular)
      lval_plantel.append(val_plantel) 
      lronda.append(str(ron))
                 
         
   equipaRonda =pd.DataFrame({'IdEquipa':lidequipa
                          ,'Ranking': lranking
                          ,'Tactica':ltact
                          ,'Variacao':lvar
                          ,'PontosRonda':lpts_ron
                          ,'PontosTotal':lpts_tot 
                          ,'SaldoDisponivel':lsld_disp
                          ,'Val11titular':lval11_titular
                          ,'ValorPlantel':lval_plantel                                
                          ,'Ronda':lronda})
   
   #equipaRonda.to_csv(Param.dirPathData+str(equipas.iloc[i, 0]+str(ron)+'.csv',index=False, encoding='utf-8')
   return equipaRonda

def readTotRondas(iparams):
   ini = 1 
   fim =int(iparams['rondafinal']) 
   dfranktotal = pd.DataFrame([])
   for ronda in range(ini, fim):
      ficheiroRank = iparams['dirdata'] +'rnd' + str(ronda) + 'rank' 
      df_rnd = Param.readFile(ficheiroRank)
      dfranktotal = dfranktotal.append(df_rnd, ignore_index=True) 
   return  dfranktotal


def writeTotRondas(iparams):
   ini = int(iparams['rondainicial']) 
   fim =int(iparams['rondafinal']) 
   dfranktotal = pd.DataFrame([])
   for ronda in range(ini, fim):
      ficheiroRank = iparams['dirdata'] +'rnd' + str(ronda) + 'rank' 
      df_rnd = Param.readFile(ficheiroRank)
      dfranktotal = dfranktotal.append(df_rnd, ignore_index=True)
   print(dfranktotal) 
   ficheiroTotRank = iparams['dirdata'] +'totrank'  
   Param.writeTabularFile(dfranktotal, ficheiroTotRank)    

def readEquipaRonda(iparams):
   ronda           = int(iparams['rondaatual']) 
   fichEquipaRonda = iparams['dirdata'] +'rnd' + str(ronda) + 'rank' 
   dfequiparonda   = Param.readFile(fichEquipaRonda)
   dfequiparonda        = dfequiparonda.rename({'IdEquipa': 'idequipa'
                                   ,'Ranking': 'ranking'
                                   ,'Tactica': 'tactica'
                                   ,'Variacao': 'variacao'                              
                                   ,'PontosRonda':'pontosronda'
                                   ,'PontosTotal':'pontostotal'
                                 ,'SaldoDisponivel':'saldodisponivel'
                                 ,'Val11titular':'val11titular'
                                 ,'ValorPlantel':'Valorplantel'
                                   ,'Ronda':'ronda'                                   
                                   },axis=1) 
   return dfequiparonda




def writeEquipaRondas(iparams):
   ini = int(iparams['rondainicial']) 
   fim = int(iparams['rondafinal']) 
   #Modificar e ir para dentro do loop de forma a criar um ip diferente
   incrementproxy = 0
   proxies        = cfg.getProxy()
   for ronda in range(ini, fim):
      browse = Param.runDriver(proxies,incrementproxy)
      Connect.loginLigaRecord(browse,iparams)
      dfrondaEquipas = webEquipaRonda(browse ,iparams,ronda)
      ficheiroRank  =iparams['dirdata'] +'rnd' + str(ronda) + 'rank'
      Param.writeTabularFile(dfrondaEquipas, ficheiroRank)
      incrementproxy = incrementproxy +1
   browse.close()   


if __name__ == "__main__":
  try:
   params = Param.config(Param.configFile, 'ligarecord')   
   writeEquipaRondas(params)
   #writeTotRondas(params)
  except KeyboardInterrupt:
     print('\n')