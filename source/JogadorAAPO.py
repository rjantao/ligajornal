import os
import Configurations as cfg
aapoLnkPlantel='https://www.academiadasapostas.com/stats/competition/portugal-stats/63'
paginaPrincipal  = 'http://liga.record.pt/gerir-equipas/default.aspx'
ecranInicial     = 'https://aminhaconta.xl.pt/LoginNonio'
from   time import sleep
import bs4
import pandas as pd
import Param
import unidecode


def plantel_clube(driver,clube_pla): 
  sleep(10) 
  button = driver.find_element_by_css_selector('div.team-info:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > a:nth-child(2)')
  button.click()
  driver.refresh 
  sleep(10)

  shirtnumber=[]
  jogador    =[]
  minutos      =[]
  posicao  =[]
  clube    =[]
  data_saida =[]
  v_num     = 1                 
  v_num       = v_num +1 

  plantel_source= driver.page_source

  plantel_page= bs4.BeautifulSoup(plantel_source.encode(Param.enc), 'html.parser')  
  #table_plantel = plantel_page.find_all('table')[0]
  table_plantel = plantel_page.find("table", {"class": "team-players float-header"})
  
  tbody_plantel = table_plantel.find("tbody")   
  #tbody_plantel = plantel_page.find("tbody")
  num_plantel = len(tbody_plantel.find_all('tr'))
  v_num_pos = 0
  for aapo_tr in tbody_plantel.find_all('tr')[0:num_plantel]:       
     v_shirt =  aapo_tr.find_all('td')[0].text.strip() 
         
     v_pos = aapo_tr.find('strong')
     #Na tabela dos jogadores vai ser essencial
     #identificar a posicao do jogador, existindo um separador para cada 
     #uma das posições. Existe uma variável v_num_pos que vai ser utilizada para ajudar
     #identificar os treinadores , que são os primeiros.
     #O separador é identificado pela v_pos 
     #Sendo None é um valor para acrescentar
     #<strong>Goalkeeper</strong>,<strong>Defender</strong>,<strong>Midfielder</strong>,<strong>Attacker</strong>
     if v_num_pos == 0:
        if v_shirt == None or v_shirt =='ac' or v_shirt =='a' :
           v_posicao = 'TR'
        else:
           v_posicao = 'GR' 
     if v_pos == None:
        v_num_pos = v_num_pos +1
        v_data_sai = None
        shirtnumber.append(v_shirt)    
        v_aux_jog  = aapo_tr.find_all('td')[2].text.strip()         
        if  v_aux_jog.replace(chr(10),"")!=None: 
           v_aux_str =  v_aux_jog.replace(chr(10),"")
           v_tam      = v_aux_str.find('Saiu')
           if  v_tam ==-1: 
              v_jog = v_aux_jog.strip()
              v_data_sai=None 
           elif v_tam>0:
              v_loc_sai  = v_aux_str.find(':')  
              v_jog= v_aux_str[:v_tam].strip()
              v_data_sai = v_aux_str[v_loc_sai+2:].strip()                  
           else:
               v_jog= v_aux_jog
               
        jogador.append(v_jog)
        minutos.append(aapo_tr.find_all('td')[5].text.strip())
        posicao.append(v_posicao)
        clube.append(clube_pla)
        data_saida.append(v_data_sai)
     else:
        #linha separadora falada acima no que respeita a posição
        if  v_pos.text.strip()  =="Goalkeeper": 
           v_posicao = 'GR'
        elif  v_pos.text.strip()  =="Defender":
           v_posicao = 'DF' 
        elif  v_pos.text.strip()  =="Midfielder":
           v_posicao = 'MD'
        elif  v_pos.text.strip()  =="Attacker":
           v_posicao = 'AV'
              
  df_jog_pla=pd.DataFrame({'Jogador':jogador
               ,'Clube' : clube
                ,'Posicao' :posicao
                ,'Minutos':minutos
               ,'Data Saida':data_saida
               })           
  return  df_jog_pla


def webJogadorAapo(iparams):
  planteis_clubes= pd.DataFrame([])  
  fichlinksaapo =  iparams['dirdata']+ 'LinksPLAAAPO'

  df_lnk_pla_1 = Param.readFile(fichlinksaapo)
  if  iparams['teste'] == 'S':
     df_lnk_pla = df_lnk_pla_1 [df_lnk_pla_1['Clube']=='Porto'].reset_index(drop=True)     
  elif  iparams['teste'] == 'N': 
     df_lnk_pla = df_lnk_pla_1   


  #df_lnk_pla = df_lnk_pla_1 [df_lnk_pla_1['Clube']=='Tondela'].reset_index(drop=True)
  #df_lnk_pla = df_lnk_pla_1 [df_lnk_pla_1['Clube']=='Porto'].reset_index(drop=True)
  
  maxequipas = len(df_lnk_pla)
  incrementproxy = 0
  proxies = cfg.getProxy()
  planteis_clubes = pd.DataFrame([])
  for i in range(0,maxequipas):
     clube = df_lnk_pla.iloc[i]['Clube']
     #identclube = df_lnk_pla.iloc[i]['Identclube']
     browse = Param.runDriver(proxies,incrementproxy)
     lnk_cha=df_lnk_pla.iloc[i]['Link']  
     browse.get(lnk_cha)
     
     #print(lnk_cha) tivemos atrasar o carregamento para fazer download da tabela com os jogadores 
     df_clube  =  pd.DataFrame([]) 
     df_clube = plantel_clube(browse, clube)
     #fichlistaclube =  iparams['dirdata'] + identclube
     #Param.writeTabularFile(df_clube, fichlistaclube  )

     planteis_clubes = planteis_clubes.append(df_clube ,ignore_index=True)
     browse.close()
     incrementproxy  = incrementproxy  +1 
  
  
  if iparams['teste'] == 'S':
     fichlistajogclube =  iparams['dirdata'] + clube
     Param.writeTabularFile(planteis_clubes, fichlistajogclube  ) 
  else:
     fichlistajogaapo =  iparams['dirdata'] + iparams['listajogaapo']
     Param.writeTabularFile(planteis_clubes, fichlistajogaapo  )
  return planteis_clubes

def weblinksPlanteis(iparams): 
   incrementproxy = 0
   proxies = cfg.getProxy()
   df_link_pla=pd.DataFrame([])
   l_link_pla=[]
   l_clube   =[]
   l_href = []
   l_identclube  = []
   lnk_pag_pla = iparams['lnk_pag_pla']
   browse = Param.runDriver(proxies,incrementproxy)
   browse.get(lnk_pag_pla)
   source_page = browse.page_source
   plantel_page= bs4.BeautifulSoup(source_page.encode('UTF-8'),'html.parser')
   table_plantel = plantel_page.find("table",{"class":"competition-class"})
   tbody_plantel = table_plantel.find("tbody",{"class":"competition-quarts-padding"})

   #o lnkepoca esta com o id alfanumerico em vez do numerico, porque a lista de valores 
   # da epoca fica no ano anterior
   v_epoca = iparams['lnkepoca']


   for plaElem in tbody_plantel.find_all("tr"):
      aux_a    = plaElem.find('a') 
      v_clube  = aux_a.text.strip()

      v_identclube = unidecode.unidecode(str(v_clube).replace(" ","").lower())
      v_href   = aux_a.get('href') 
      v_tam_str  = len(v_href)-4
      v_tam      =  v_href[v_tam_str:]
      v_link_liga =  v_href  + '#tab=t_squad&team_id='+ v_tam +'&competition_id=63&page=1&season_id='  + v_epoca   
      v_link_liga =  v_href  + '#tab=t_squad&team_id='+ v_tam +'&competition_id=63&page=1&season_id='  + v_epoca      
      l_link_pla.append(v_link_liga)
      l_clube.append(v_clube)
      l_href.append(v_href)
      l_identclube.append(v_identclube)

   df_link_pla=pd.DataFrame({'Clube':l_clube
                            ,'Link_clube':l_href
                            ,'Link':l_link_pla
                           ,'Identclube':l_identclube
                              }) 
   fichlinksaapo =  iparams['dirdata'] + 'LinksPLAAAPO'
   Param.writeTabularFile(df_link_pla, fichlinksaapo )
   browse.close()
   return df_link_pla


if __name__ == "__main__":
  try:
   params = Param.config(Param.configFile, 'ligarecord')   
   linkplanteis = weblinksPlanteis(params)
   #print(linkplanteis)
   planteis = webJogadorAapo(params)
   #print(planteis)
   
   #writeEstatisticas(params)
  except KeyboardInterrupt:
     print('\n')


