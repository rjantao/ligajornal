import Param
import os
from importlib import reload
import pandas as pd
import bs4
import sys
import Configurations as cfg
from time import sleep
import math

# Informação importada do site academia Apostas


def equipa(jog_page):
   team_name=[]
   for aux_nome in  jog_page.find_all("div", {"class": "stats-game-head-teamname"}):
      for team in aux_nome.find_all('a'):
         len_team = len(team.text.strip())
         if len_team>0:
            team_name.append(team.text.strip())
   return team_name

def ronda(i_jornada):
  aux_jornada = int(i_jornada.replace('Jornada', '').strip())
  aux_ronda   = aux_jornada 
  v_ronda     = aux_ronda -3
  return v_ronda


#dados do jogo do site academia de apostas
def game(jog_page,team_name,jogo,link,ijornada,iron):
  inf_jogo    =jog_page.find("td", {"class":"stats-game-head-date"})
  resultado   = inf_jogo.find("li",{"class":"f-score odd"}) 
  v_data_jogo = inf_jogo.find_all("li",{"class":"gamehead"})[1].b.text.strip() 
  v_epoca     = inf_jogo.find_all("li",{"class":"gamehead"})[3].a.text.strip()
  v_txt_jornada   = inf_jogo.find_all("li",{"class":"gamehead"})[4].a.text.strip()
  v_ind_jor = v_txt_jornada.index('-') 
  #v_jornada =v_txt_jornada[v_ind_jor+1:].strip()
  v_aux_arb =  jog_page.find_all('table', {"id":"linups"})[1]  
  v_arb     = v_aux_arb.find_all('a')[0].text.strip()    
  #v_ronda   = ronda(v_jornada)
  v_ronda    = iron
  v_jornada = ijornada
  df_lin_jog=pd.DataFrame({'Jogo':[str(jogo)]
               , 'Clubecasa':[team_name[0]]
               , 'Clubefora':[team_name[1]]
               , 'Data' :[v_data_jogo]
               ,'Epoca':[v_epoca]
               ,'Jornada':[v_jornada]
               ,'Arbitro':[v_arb]
               ,'Link':[link]
               ,'Ronda':[v_ronda]
               })  
  
 # v_lin_jog = +','+team_name[0]+','+team_name[1]+','+v_data_jogo+','+v_epoca+','+v_jornada+','+v_arb+','+link
  return df_lin_jog

#estatisticas do jogo do site academia de apostas 
def estatisticas(jog_page,team_name,ijogo):
  items = ['possession','goals','shots_on_target','shots_woodwork','shots_blocked'
                  ,'shots_off_target','attacks','dangerous_attacks','penalties','yellow_red_cards'
                  ,'yellow_cards','fouls','free_kicks','goal_kicks','throw_ins'
                  ,'substitutions','corners','red_cards']
  stat         =[]
  value_stat   =[]
  team         =[]
  item_stat = []
  ljogo = []
  df_stat = pd.DataFrame([])  
  for item in items:  
    lin_stat  =jog_page.find("tr", {"class":item})
    if lin_stat!=None:     
       lin_value_A =lin_stat.find("td", {"class":"stat_value_number_team_A"}).text.strip()
       value_stat.append(lin_value_A) 
       item_stat.append(item) 
       team.append(team_name[0])
       ljogo.append(ijogo)
      # stat.append(lin_value_A+','+item+','+team_name[0]+','+str(jogo))
       lin_value_B =lin_stat.find("td", {"class":"stat_value_number_team_B"}).text.strip()
       value_stat.append(lin_value_B) 
       item_stat.append(item) 
       team.append(team_name[1])
       ljogo.append(ijogo)
      #stat.append(lin_value_B+','+item+','+team_name[1]+','+str(jogo))

  df_stat =pd.DataFrame({'Clube':team
                    , 'Estatistica':item_stat
                    , 'Valor': value_stat
                    ,'Jogo':ljogo})  
  
  #df_stat["Jogo"] = ijogo
  return df_stat
# analise das ocorrencias que existiram no jogo
def sumario(jog_page,parte,team_name,ijogo):
  first_part  =jog_page.find("table", {"id":parte})
  teams       =[]   
  nome_jog    = []
  minutes     = [] 
  ocorrencia  = []
  ljogo = []
  df_lin_ocor = pd.DataFrame([])  
  for row_ocor in first_part.find_all("tr"):                     
     for lin_td in row_ocor.find_all("td",{"class":"match-sum-wd-description"}): 
        aux_style=lin_td.find("div")
        if aux_style!=None:        
           aux_team =aux_style.get("style")
           if aux_team!=None:
              if aux_team=="float:left":
                 team=team_name[0]
              elif aux_team=="float:right":
                 team=team_name[1]
        v_ind = 0 
        for lin_jog in lin_td.find_all('a'):                   
           if lin_jog!= None:
              v_nome_jog = lin_jog.text.strip() 
              nome_jog.append(v_nome_jog)
              teams.append(team)
              for v_minute in row_ocor.find_all("td",{"class":"match-sum-wd-minute"}):         
                 len_minute = len(v_minute.text.strip())          
                 if len_minute>0:
                    minutes.append(v_minute.text.replace("'",""))             
              for v_symbol in row_ocor.find_all("td",{"class":"match-sum-wd-symbol"}):                 
                    v_aux_symbol =  v_symbol.find('span')   
                    if v_aux_symbol!= None:                                                 
                       if v_ind == 0:                       
                          v_ocorrencia= v_aux_symbol.get("title")   
                          ocorrencia.append(v_ocorrencia) 
                       elif v_ind == 1:
                          ocorrencia.append('Substitute out')                     
                       if v_aux_symbol.get("title")=="Substitute in":   
                          v_ind = v_ind +1
 
  df_lin_ocor =pd.DataFrame({'Jogador':nome_jog
                    , 'Minuto':minutes
                    , 'Ocorrencia':ocorrencia
                    , 'Clube': teams})  
  df_lin_ocor["Jogo"] = int(ijogo)
  return df_lin_ocor  

# formacao titulares e suplentes
def formacao_clube(lineup_page,tipo_lineup,tipo,team_name,ijogo):
  teams      =[]
  jogadores  =[]
  posicoes   =[]
  nacionalidades=[]
  ljogo   = []
  jor_lineup = lineup_page.find("table", {"id": tipo_lineup})  
  index_team = 0  
  df_lin_form=pd.DataFrame([])     
  for lin_tbody in jor_lineup.find_all("tbody", {"class": "stat-zero-padding"}):  
     for tr_jog in lin_tbody.find_all("tr"): 
        for lin_td in tr_jog.find_all("td",{"class":"match-team-wd-76" }):    
           jog      =  lin_td.find('a')        
           if jog!=None:
              jogadores.append(jog.text.strip())
              teams.append(team_name[index_team])
              ljogo.append(ijogo)
        for lin_pos in  tr_jog.find_all("td", {"class": "match-team-wd-8"}):                             
           if len(lin_pos.text.strip())>0:
              posicoes.append(lin_pos.text) 
           elif len(lin_pos.text.strip())==0:
              aux_nac = lin_pos.find('span')
              nacionalidades.append (aux_nac.get('title'))  
     index_team = index_team +1  
  v_len_form = len(jogadores)
    
  df_lin_form = pd.DataFrame({'Jogador':jogadores
                    , 'Posicao':posicoes
                    , 'Nacionalidade':nacionalidades
                    , 'Clube': teams
                    ,'Jogo':ljogo}) 
  df_lin_form["Tipo"] = tipo
  #df_lin_form["Jogo"] = ijogo

  return  df_lin_form


def webJogos(driver,ijogini,ijogfim,iron,ijornada,iparams):
  fichlinksaapo =   iparams['dirdata'] + iparams['linkjogosaapo']
  df_lnk      =  Param.readFile(fichlinksaapo)
  print(df_lnk )
  o_formacao    =pd.DataFrame([])
  o_ocorrencias =pd.DataFrame([])
  o_jogos        =pd.DataFrame([])
  o_estatisticas = pd.DataFrame([])
  for jogo in range(ijogini,ijogfim):
    jogo_lnk = df_lnk['Link'][jogo]
    driver.get(jogo_lnk+'/1/live')  
    sleep(5)
    jor_source = driver.page_source
    jor_page = bs4.BeautifulSoup(jor_source.encode(Param.enc),'html.parser')
    teams    =[]
    #k          = i+1
    teams      = equipa(jor_page) 
    titulares  = formacao_clube(jor_page,"team-lineups",'T',teams,jogo)
    suplentes = formacao_clube(jor_page, "team-sub-lineups", 'S', teams, jogo)
    o_formacao = o_formacao.append(titulares, ignore_index=True)
    o_formacao =o_formacao.append(suplentes, ignore_index=True)   
    sum_1P = sumario(jor_page, "first-half-summary", teams, jogo)
    sum_2P = sumario(jor_page, "second-half-summary", teams, jogo)
    o_ocorrencias = o_ocorrencias.append(sum_1P, ignore_index=True)
    o_ocorrencias = o_ocorrencias.append(sum_2P, ignore_index=True)
    stat_jog = estatisticas(jor_page, teams, jogo)
    o_estatisticas= o_estatisticas.append(stat_jog,ignore_index=True)
    jogo = game(jor_page, teams, jogo, jogo_lnk,ijornada,iron)
    o_jogos       = o_jogos.append(jogo,ignore_index=True)    
  fichjogos = iparams['dirdata'] + iparams['jogos']  + iparams['jornadas'] + str(ijornada)
  Param.writeTabularFile(o_jogos, fichjogos )
  fichformacao =iparams['dirdata'] + iparams['formacao']  + iparams['jornadas'] + str(ijornada)
  Param.writeTabularFile(o_formacao, fichformacao )
  fichocorrencias = iparams['dirdata'] + iparams['ocorrencias'] + iparams['jornadas'] + str(ijornada)
  Param.writeTabularFile(o_ocorrencias, fichocorrencias )
  fichestatisticas = iparams['dirdata'] + iparams['estatisticas'] + iparams['jornadas'] + str(ijornada)
  Param.writeTabularFile(o_estatisticas, fichestatisticas ) 
  #writer.save()

  return o_jogos, o_formacao, o_ocorrencias, o_estatisticas

def retornajogos(jornada):
  inc = 9
  if jornada == 1:
     jogini = 0
     jogfim = 9   
  else:
     jogini = jornada *inc - 9
     jogfim = jornada *inc    
  return  int(jogini),  int(jogfim) 



def writeJogosJornadas(iparams):
  jornadaini = int(iparams['jornadaini']) 
  jornadafim = int(iparams['jornadafim'])
  jornadalrec = int(iparams['jornadalrec'])
  incrementproxy = 0
  proxies = cfg.getProxy()
  for jornada in range(jornadaini, jornadafim): 
     browse = Param.runDriver(proxies,incrementproxy)
     # jogo inicial da jornada e fim da jornada
     jogini, jogfim = retornajogos(jornada)
     ronda = jornada - jornadalrec
     webJogos(browse, jogini, jogfim, ronda, jornada,iparams)
     browse.close()
     incrementproxy  = incrementproxy  +1


def writeJornadasTotal(iparams): 
  #jornadaini = int(iparams['jornadaini']) 
  jornadaini = 1
  jornadafim = int(iparams['jornadafim']) 
  o_jogosfinal        =pd.DataFrame([])
  o_formacaofinal    =pd.DataFrame([])
  o_ocorrenciasfinal =pd.DataFrame([])
  o_estatisticasfinal = pd.DataFrame([])
  for jornada in range(jornadaini, jornadafim): 
     jogini, jogfim = retornajogos(jornada)
     ronda = jornada - 3
     fichjogos =iparams['dirdata'] + iparams['jogos']  + iparams['jornadas'] + str(jornada)
     fichformacao = iparams['dirdata'] + iparams['formacao']  + iparams['jornadas'] + str(jornada)
     fichocorrencias = iparams['dirdata'] + iparams['ocorrencias']  + iparams['jornadas'] + str(jornada)
     fichestatisticas = iparams['dirdata'] + iparams['estatisticas']  + iparams['jornadas'] + str(jornada)
     df_jogos           = pd.DataFrame([])
     df_formacao        = pd.DataFrame([])
     df_ocorrencias     = pd.DataFrame([])
     df_estatisticas    = pd.DataFrame([])
     dfjogos            = Param.readFile(fichjogos)
     df_formacao        = Param.readFile(fichformacao)
     df_estatisticas    = Param.readFile(fichestatisticas)
     df_ocorrencias     = Param.readFile(fichocorrencias)  
     o_jogosfinal        =o_jogosfinal.append(df_jogos, ignore_index=True)
     o_formacaofinal = o_formacaofinal.append(df_formacao, ignore_index=True)
     o_ocorrenciasfinal =o_ocorrenciasfinal.append(df_ocorrencias, ignore_index=True)
     o_estatisticasfinal = o_estatisticasfinal.append(df_estatisticas, ignore_index=True)

  fichjogos = iparams['dirdata'] + iparams['jogos'] + 'final'
  Param.writeTabularFile(o_jogosfinal, fichjogos )
  fichformacao = iparams['dirdata'] + iparams['formacao'] + 'final'
  Param.writeTabularFile(o_formacaofinal, fichformacao ) 
  fichocorrencias = iparams['dirdata'] + iparams['ocorrencias'] + 'final'
  Param.writeTabularFile(o_ocorrenciasfinal, fichocorrencias )
  fichestatisticas = iparams['dirdata'] + iparams['estatisticas'] + 'final'
  Param.writeTabularFile(o_estatisticasfinal, fichestatisticas) 



def writeLinkJogos(iparams):
   weblinkepoca = iparams['linkallgames']
   incrementproxy = 0
   proxies = cfg.getProxy()
   browse = Param.runDriver(proxies,incrementproxy)
   df_jogos=pd.DataFrame([])
   lt_jogos=[]
   for i in range(1,3):
      browse.get(weblinkepoca+'/page/'+str(i))
      jornadas = browse.page_source
      jornadas = bs4.BeautifulSoup(jornadas.encode('UTF-8'),'html.parser')
      aux_jorn = jornadas.find('tbody')
        #for jornElem in aux_jorn.find_all("td",{"class":"darker tipsy-active nowrap "}):
      for jornElem in aux_jorn.find_all("td",{"width":"3%"}):
         aux_a    = jornElem.find('a')     
         v_href =  aux_a.get('href')    
         lt_jogos.append(v_href)
   df_jogos=pd.DataFrame(lt_jogos, columns=["Link"]) 
   fichlinkjogosaapo =  iparams['dirdata'] + iparams['linkjogosaapo']
   Param.writeTabularFile(df_jogos, fichlinkjogosaapo )

if __name__ == "__main__":
  try:
   params = Param.config(Param.configFile, 'ligarecord')   
   writeJogosJornadas(params)
   #writeJornadasTotal(params)
   #linkjogos = writeLinkJogos(params)
 
   #Gerar os links dos jogos primeiro (writeLinkJogos)
   #Gerar os ficheiros jogos,ocorrencias,formacao,estatisticas por jornada
   #Gerar os ficheiros que agrupam as jornadas todas


  except KeyboardInterrupt:
     print('\n')
     