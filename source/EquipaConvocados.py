# -*- coding: utf-8 -*-
"""
Created on Fri Feb 08 22:04:39 2019

@author: rjantao
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Dec 01 09:16:10 2018

@author: rjantao
"""
import bs4
import pandas as pd
import Param
import Equipa
from time import sleep
import Connect
import Configurations as cfg
import numpy as np






def ConvocadosRonda(cnv_page,equipas,i,ronda):
   df_convocadosronda=pd.DataFrame([])   
   aux_team_jornada = cnv_page.find("div", {"id": "main_main_ctl00_divPlayersPlaying"})       
   ljogador =[]
   lposicao =[]
   ltipo    =[]  
   lequipa  =[]
   lronda =[] 
   lidequipa=[]
   lshirt   =[]
   lteam    =[]
   nomeequipa = equipas.iloc[i, 1]
   idequipa   = equipas.iloc[i, 0]
   position=["forward","midfield","defense","goalkeeper"]
   if aux_team_jornada!=None:   
      for i in position:
         aux_pos      = aux_team_jornada.find_all("div",{"data-position":i}) 
         for aux_jog in aux_pos:
            jog      = aux_jog.find('h6').text
            pos      = aux_jog.get('player-position')
            tp     = 'TIT'
            shirt   = aux_jog.get('data-shirt')  
            data_team_id= aux_jog.get('data-team-id')
            ljogador.append(jog)
            lposicao.append(pos)
            ltipo.append(tp) 
            lequipa.append(nomeequipa)
            lronda.append(ronda)
            lidequipa.append(idequipa)
            lshirt.append(shirt)
            lteam.append(data_team_id)
         #lclube.append(clube_tre)      
   aux_sup_page = cnv_page.find("ul", {"id": "main_main_ctl00_suplentes"}) 
   if aux_sup_page!=None:   
      aux_li = aux_sup_page.find_all("li")
      for aux_sup in aux_li: 
         jog          = aux_sup.find('h6').text
         pos          = aux_sup.get('player-position')
         data_shirt   = aux_sup.get('data-shirt')
         data_team_id = aux_sup.get('data-team-id')
         tp       ='SUP'
         ljogador.append(jog)
         lposicao.append(pos)
         ltipo.append(tp) 
         lequipa.append(nomeequipa)
         lronda.append(ronda)
         lidequipa.append(idequipa) 
         lshirt.append(data_shirt)
         lteam.append(data_team_id)
   df_convocadosronda =pd.DataFrame({'Jogador':ljogador
                                  ,'Shirt':lshirt
                                  ,'Posicao': lposicao
                                  ,'Tipo': ltipo
                                  ,'Equipa':lequipa
                                  ,'PlaId':lteam
                                  ,'IdEquipa':lidequipa
                                  ,'Ronda':lronda})

   return df_convocadosronda
 


def convocadosEquipa(driver,equipas,iron):
   ron = iron 
   max_val=len(equipas)
   df_convocados=pd.DataFrame([])   
   for i in range(0,max_val):
      driver.get(lnk_equi_ron+str(equipas.iloc[i, 0])+'&id_round='+str(ron))  
      equi_source = driver.page_source
      equi_page   = bs4.BeautifulSoup(equi_source.encode(Param.enc),'html.parser')        
      df_teamRonda = ConvocadosRonda(equi_page,equipas,i,ron)
      df_convocados=df_convocados.append(df_teamRonda,ignore_index=True)
        
   return df_convocados 


def capitao(html_man,equipa,idequipa,ronda):
   cap     = html_man.find("div",{"class":"name-team"})
   
   if cap != None:
      jog     = cap.find('h6').text
      pos     = 'CAP'
      tp      = 'CAP'
      clube   = cap.find('p').text
      pontos  = html_man.find("div",{"class":"points"})
      pts_tot = pontos.find("p",{"class":"player-points"}).text.replace("pts","")
      pts_rnd = pontos.find("p", {"class": "team-points"}).text.replace("pts", "")
   else:
      jog     = ''
      pos     = 'CAP'
      tp      = 'CAP'
      clube   = ''
      pontos  = 0
      pts_tot = 0
      pts_rnd = 0

   df_capitao =pd.DataFrame({'Jogador':[jog]
                              ,'Posicao':[pos]  
                              ,'Clube':[clube]
                              ,'PontosRonda':[pts_rnd]
                              ,'PontosTotal': [pts_tot]
                              ,'ValorInicial':[0]
                              ,'ValorAtual' :[0]
                              ,'IdEquipa':[idequipa]
                              ,'Equipa':[equipa]
                              ,'Ronda':[ronda]})   
                              
   return df_capitao



def treinador(html_man,equipa,idequipa,ronda): 
   df_treinador = pd.DataFrame([])   
   tre         = html_man.find("div",{"class":"name-team"})
   jog         = tre.find('h6').text
   pos         ='TRE'
   clube       = tre.find("p",{"class":"team"}).text
   #if clube=='-':
      #Conceito       ='Treinador' 
      #aux_exc        = iexc[( iexc['Tipo']==Param.lrec)
                       #&(iexc['Conceito']==Conceito)
                       #&(iexc['Detail']==jog)].reset_index(True)                      
      #if len(aux_exc)>0:
         #clube        = aux_exc['Master'][0]    
   pts         =  html_man.find("div",{"class":"points"})
   pts_tot     = pts.find("p",{"class":"player-points"}).text.replace("pts","")
   pts_rnd     =  pts.find("p",{"class":"team-points"}).text.replace("pts","")    
   df_treinador =pd.DataFrame({'Jogador':['TREINADOR']
                              ,'Posicao':[pos]  
                              ,'Clube':[clube]
                              ,'PontosRonda':[pts_rnd]
                              ,'PontosTotal': [pts_tot]
                              ,'ValorInicial':[0]
                              ,'ValorAtual' :[0]
                              ,'IdEquipa':[idequipa]
                              ,'Equipa':[equipa]
                              ,'Ronda':[ronda]
                              ,'FlexField':[jog]})                                 
   return df_treinador


def posicaoFormacao(html_pla,p_tipo,equipa,idequipa,ronda):
   lnome_jogador=[]
   lpos = []
   lclube =[]
   lpontos_ronda =[]
   lpontos_total =[]
   lronda=[]
   lequipa =[]
   lidequipa=[]
   lvalvi  =[]
   lvalva =[] 
   lflexfield =[]    
   lteamid =[]
   lshirt=[]
   df_posicao_formacao=pd.DataFrame([])
   try:
      aux_pos      = html_pla.find_all("div",{"data-position":p_tipo})  
      for lin in aux_pos:      
         aux_nome        = lin.find('h6').text
         aux_pos         = lin.get('player-position')
         aux_id          = lin.get('id')
         aux_data_team_id= lin.get('data-team-id')
         aux_data_shirt  = lin.get('data-shirt')       
         aux_clube       = lin.find("p",{"class":"team"}).text
         aux_pts_rou     = lin.find("span", {"class": "points-round"}).text
         aux_pts_tot     = lin.find("span", {"class": "points-total"}).text
         lnome_jogador.append(aux_nome)
         lpos.append(aux_pos)
         lclube.append(aux_clube)
         lpontos_ronda.append(aux_pts_rou)
         lpontos_total.append(aux_pts_tot)
         lronda.append(ronda)
         lidequipa.append(idequipa)
         lequipa.append(equipa)
         lflexfield.append(aux_id)     
         lteamid.append(aux_data_team_id)
         lshirt.append(aux_data_shirt)
         aux_cash   = lin.find_all("div", {"class": "cash"})    
         for d in aux_cash:
            x=0
            for p in d.find_all("p"):
               if x==0: 
                  va = str.replace(str.replace(str(p.text),'.',''),'VA','')
                  #non breakspace
                  vabr1 = va.replace('\xa0','').replace('\xc2','')
                  lvalva.append(vabr1)
               elif x==1:
                  vi = str.replace(str.replace(str(p.text),'.',''),'VI','')
                  vibr1 = vi.replace('\xa0','').replace('\xc2','')
                  lvalvi.append(vibr1)
               x=x+1
      df_posicao_formacao =pd.DataFrame({'Jogador':lnome_jogador
                              ,'Posicao': lpos
                              ,'Clube':lclube
                              ,'PontosRonda':lpontos_ronda
                              ,'PontosTotal': lpontos_total
                              ,'ValorInicial':lvalvi
                              ,'ValorAtual' :lvalva
                              ,'IdEquipa':lidequipa
                              ,'Equipa':lequipa
                              ,'Ronda':lronda
                              ,'FlexField':lflexfield
                              ,'PlaId':lteamid
                              ,'Shirt':lshirt})
   except:
      DebugFile = Param.openDebugFile('Debug')
      Param.writeDebugLines(DebugFile,p_tipo)
      Param.writeDebugLines(DebugFile,str(idequipa))
      Param.writeDebugLines(DebugFile,str(ronda))          
      Param.closeDebugFile(DebugFile)                        
   return df_posicao_formacao


def PlantelRonda(equiPage,iequipas,i,iron):
   df_formacao=pd.DataFrame([])
   aux_jog       = equiPage.find("div", {"class": "list"}) 
   if  aux_jog!=None:   
      df_gr         = posicaoFormacao(aux_jog,"goalkeeper",iequipas.iloc[i, 1],iequipas.iloc[i, 0],iron)
      df_formacao   = df_formacao.append(df_gr, ignore_index=True)
      df_df         = posicaoFormacao(aux_jog,"defense",iequipas.iloc[i, 1],iequipas.iloc[i, 0],iron)
      df_formacao   = df_formacao.append(df_df, ignore_index=True)
      df_md         = posicaoFormacao(aux_jog,"midfield",iequipas.iloc[i, 1],iequipas.iloc[i, 0],iron)
      df_formacao   = df_formacao.append(df_md, ignore_index=True)
      df_av         = posicaoFormacao(aux_jog,"forward",iequipas.iloc[i, 1],iequipas.iloc[i, 0],iron)
      df_formacao   = df_formacao.append(df_av, ignore_index=True)
   aux_tre       = equiPage.find("div", {"id": "main_main_ctl00_detailsManager"})         
   if  aux_tre!=None:   
      df_tre        = treinador(aux_tre,iequipas.iloc[i, 1],iequipas.iloc[i, 0],iron)          
      df_formacao   = df_formacao.append(df_tre, ignore_index=True)
   aux_cap       = equiPage.find("div", {"id": "main_main_ctl00_detailsCaptain"}) 
   if aux_tre!=None:   
      df_cap        = capitao(aux_cap,iequipas.iloc[i, 1],iequipas.iloc[i, 0],iron)
      df_formacao   = df_formacao.append(df_cap, ignore_index=True)
   return df_formacao


def WebConvocadosEquipas(driver,iparams,ron):
   lnk_equi_ron =  iparams['lnk_equi_ron']
   equipas = Equipa.readEquipas(iparams) 
   max_equipas = len(equipas)
   dfplantel=pd.DataFrame([])
   dfconvocados=pd.DataFrame([])
   #dfexc         =pd.read_excel(Param.dir_atual+'map_exc.xls', sheetname='Excepcoes')      
   for i in range(0,max_equipas):
      vEquipaData = True
      #No caso de existir uma ronda sem valores para cada equioa
      if vEquipaData ==True:
         driver.get(lnk_equi_ron+str(equipas.iloc[i, 0])+'&id_round='+str(ron))  
         equi_source     = driver.page_source
         sleep(10)
         equi_page       = bs4.BeautifulSoup(equi_source.encode(Param.enc),'html.parser')  
         dfplanteleqp    =pd.DataFrame([])
         dfconvocadoseqp =pd.DataFrame([])
         dfplanteleqp   = PlantelRonda(equi_page,equipas,i,ron)
         dfconvocadoseqp = ConvocadosRonda(equi_page,equipas,i,ron)
         dfplantel     = dfplantel.append(dfplanteleqp, ignore_index=True)
         dfconvocados  = dfconvocados.append(dfconvocadoseqp, ignore_index=True)
   return dfplantel, dfconvocados
   


def transferenciasPlantel(iepoca):
   dftottransfPlantel = pd.DataFrame([])
   for ron in range(1,10):
     dfPlantelB1 = readEquipaPlantel(iepoca,ron+1)
     dfPlantelA1 = readEquipaPlantel(iepoca,ron)
     dfPlantelB2 = dfPlantelB1[['NomeJogador', 'Clube', 'Equipa', 'IdEquipa', 'Posicao']]
     dfPlantelA2 = dfPlantelA1[['NomeJogador', 'Clube',  'IdEquipa', 'Posicao']]
     dftransfPlantelA =pd.merge(dfPlantelB2 ,dfPlantelA2,\
                            on=('IdEquipa','NomeJogador','Clube','Posicao'), indicator = True,how='left')\
                           .reset_index(drop=True)
     dftransfPlantelA = dftransfPlantelA[~dftransfPlantelA['Posicao'].isin(['TRE', 'CAP'])]
          
     dftransfPlantelB = dftransfPlantelA[dftransfPlantelA['_merge'] == 'left_only'].reset_index()
     if dftransfPlantelB.empty == False:
        dftransfPlantelB['Ronda'] = ron +1
        dftottransfPlantel = dftottransfPlantel.append(dftransfPlantelB, ignore_index=True)
               
   print(dftottransfPlantel)



def writeTotConvocados(iparams):
   ini = int(iparams['rondainicial']) 
   fim = int(iparams['rondafinal']) 
   dfplatotal = pd.DataFrame([])
   dfcnvtotal = pd.DataFrame([])
   for ronda in range(ini, fim):
      ficheiroPla = iparams['dirdata'] +'rnd' + str(ronda) + 'pla'
      ficheiroCnv = iparams['dirdata'] +'rnd' + str(ronda) + 'cnv'
      df_rnd_pla = Param.readFile(ficheiroPla)
      df_rnd_cnv = Param.readFile(ficheiroCnv)
      dfplatotal = dfplatotal.append(df_rnd_pla, ignore_index=True)
      dfcnvtotal = dfcnvtotal.append(df_rnd_cnv, ignore_index=True)

   ficheiroTotPla = iparams['dirdata'] +'totpla'   
   Param.writeTabularFile(dfplatotal,ficheiroTotPla)
   ficheiroTotCnv = iparams['dirdata'] +'totcnv' 
   Param.writeTabularFile(dfcnvtotal,ficheiroTotCnv)

def writeEquipaConvocados(iparams):
   ini = int(iparams['rondainicial']) 
   fim = int(iparams['rondafinal']) 
   #Modificar e ir para dentro do loop de forma a criar um ip diferente
   incrementproxy = 0
   proxies = cfg.getProxy()
   for ronda in range(ini, fim):
      browse = Param.runDriver(proxies,incrementproxy)
      Connect.loginLigaRecord(browse,iparams)
      dfPlantel, dfConvocados = WebConvocadosEquipas(browse,iparams,ronda)
      ficheiroPla  = iparams['dirdata'] +'rnd' + str(ronda) + 'pla'
      ficheiroConv = iparams['dirdata'] +'rnd' + str(ronda) + 'cnv'
      Param.writeTabularFile(dfPlantel,ficheiroPla)
      Param.writeTabularFile(dfConvocados,ficheiroConv)
      browse.close()
      incrementproxy = incrementproxy +1  

def readRondaPlantelConvocados(iparams,iron):
   ficheiroConv = iparams['dirdata'] +'rnd' + str(iron) + 'cnv'
   dfConvocadosRonda = Param.readFile(ficheiroConv)
   dfConvocadosRondaA = dfConvocadosRonda[['Jogador', 'Shirt','Tipo','IdEquipa','Ronda']]
   dfConvocadosRondaA.rename(columns={'Tipo': 'TipoLREC'}, inplace=True) 
   
   
   ficheiroPla = iparams['dirdata'] +'rnd' + str(iron) + 'pla'
   dfPlantelRonda = Param.readFile(ficheiroPla)
   dfPlantelRondaA = dfPlantelRonda  [['Jogador', 'Clube', 'Posicao','PontosRonda','IdEquipa','Equipa','ValorInicial','ValorAtual','Ronda','Shirt']] 
   
   dfPlantelConvocados = pd.merge(dfPlantelRondaA,dfConvocadosRondaA,\
                        on=('Jogador','IdEquipa','Ronda','Shirt'), how='left')\
                           .reset_index(drop=True)

   dfPlantelConvocados ['Condicao'] = dfPlantelConvocados.apply(lambda row: 'NU' if row['TipoLREC'] is np.NaN else row['TipoLREC'], axis=1)

   return dfPlantelConvocados

if __name__ == "__main__":
  try:
   params            = Param.config(Param.configFile, 'ligarecord')   
   inironda          = int(params['rondainicial']) 
   plantelconvocados = readRondaPlantelConvocados(params,inironda)
   benfiquistas             = Param.testedf(plantelconvocados,'Equipa','BENFIQUISTAS')
   
   #writeEquipaConvocados(params)

  except KeyboardInterrupt:
     print('\n')




