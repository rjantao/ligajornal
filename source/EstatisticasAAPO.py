import Param
import pandas as pd
import numpy as np
import Mapeamento



def calculanaomapeado(idffor,idfoco,iestatisticas):
   dffornaomapeado       = idffor[(idffor['Match'] == 'N')]


   dffornaomapeadoA  = dffornaomapeado[['Jogador','Posicao' ,'Nacionalidade' ,'Clube' ,'Jogo', 'Tipo'
                                        ,'JogadorFOR','SplitFORA' , 'SplitFORB' ,'Ronda']]   
   
   dfoconaomapeado            = pd.merge(idfoco,iestatisticas,\
                            on=('JogadorOCO','Clube','Jogo'), how='left')\
                           .reset_index(drop=True)
   dfoconaomapeado['Match']     = dfoconaomapeado.apply(lambda row: 'N' if row['Jogador'] is np.NaN else 'Y', axis=1)

   dfoconaomapeadoA              = dfoconaomapeado[(dfoconaomapeado['Match'] == 'N')]
   
   dfoconaomapeadoB              = dfoconaomapeadoA[['JogadorOCO','SplitOCOA_x','SplitOCOB_x','JogadorOCOfinal_x'
                                                     ,'Clube' ,'Jogo','Goal_x','Penalty goal_x','Own goal_x'           
                                                    ,'Penalty missed_x','Penalty save_x','Yellow card_x'        
                                                    ,'Red card_x','Yellow 2nd/RC_x','Substitute in_x','Substitute out_x'     
                                                   ]] 
   dfoconaomapeadoB.rename(columns={'SplitOCOA_x': 'SplitOCOA'
                                   ,'SplitOCOB_x':'SplitOCOB'
                                   ,'JogadorOCOfinal_x':'JogadorOCOfinal'
                                   ,'Goal_x':'Goal'
                                   ,'Penalty goal_x':'Penalty goal'
                                   ,'Own goal_x':'Own goal'
                                   ,'Penalty missed_x':'Penalty missed'
                                   ,'Penalty save_x':'Penalty save'
                                   ,'Yellow card_x':'Yellow card'
                                   ,'Red card_x':'Red card'
                                   ,'Yellow 2nd/RC_x':'Yellow 2nd/RC'
                                   ,'Substitute in_x':'Substitute in'
                                   ,'Substitute out_x':'Substitute out' 
                                   }, inplace=True)                                                
   return dffornaomapeadoA, dfoconaomapeadoB
   




#a magia de comparacao está neste calculo
def calculaMapeamentoEstatistica(idffor,idfoco,icriteriojogfor,icriteriojogoco):
   mapFOROCO= pd.merge(idffor,idfoco,\
                      left_on=(icriteriojogfor,'Clube','Jogo'),right_on=(icriteriojogoco,'Clube','Jogo'), how='left')\
                           .reset_index(drop=True)

  
   mapFOROCO['Match'] = mapFOROCO.apply(lambda row: 'N' if row[icriteriojogoco] is np.NaN else 'Y', axis=1)

   return mapFOROCO

def formacaoocorrencia(iparams,idffor,idfoco):
   dfnewestatistica      = pd.DataFrame([])
   MapeamentoA           = calculaMapeamentoEstatistica(idffor,idfoco,'JogadorFOR','JogadorOCO')
   dfnomeinteiro         = MapeamentoA[(MapeamentoA['Match'] == 'Y')]   
   dfnewestatistica      = dfnewestatistica.append(dfnomeinteiro)


   dfforAE ,dfocoAE        = calculanaomapeado(MapeamentoA,idfoco,dfnewestatistica)
   dfexcJogador            =  Mapeamento.excepcoes(iparams,'A','FormacaoOcorrencia') 
   dfocoAF                  = pd.merge(dfocoAE,dfexcJogador  ,\
                            left_on=('JogadorOCOfinal'),right_on='Origem', how='left')\
                           .reset_index(drop=True)      
   MapeamentoAE          = calculaMapeamentoEstatistica(dfforAE,dfocoAF,'Jogador','Destino')
   MapeamentoAE          = MapeamentoAE.drop(['Origem','Destino'],axis=1) 
   dfexcepcoes           = MapeamentoAE[(MapeamentoAE['Match'] == 'Y')]  
   dfnewestatistica     = dfnewestatistica.append(dfexcepcoes)

   dfforA ,dfocoA        = calculanaomapeado(MapeamentoAE,dfocoAE,dfnewestatistica)
   MapeamentoB           = calculaMapeamentoEstatistica(dfforA,dfocoA,'SplitFORA','SplitOCOB')
   df1nome2nome          = MapeamentoB[(MapeamentoB['Match'] == 'Y')]
   dfnewestatistica      = dfnewestatistica.append(df1nome2nome)
   
   dfforB ,dfocoB        = calculanaomapeado(MapeamentoB,dfocoA,dfnewestatistica)
   MapeamentoC          = calculaMapeamentoEstatistica(dfforB,dfocoB,'SplitFORB','SplitOCOB')
   df2nome2nome          = MapeamentoC[(MapeamentoC['Match'] == 'Y')]
   dfnewestatistica      = dfnewestatistica.append(df2nome2nome)   
   
   dfforC ,dfocoC        = calculanaomapeado(MapeamentoC,dfocoB,dfnewestatistica)
   MapeamentoD          = calculaMapeamentoEstatistica(dfforC,dfocoC,'SplitFORA','SplitOCOA')
   df1nome1nome          = MapeamentoD[(MapeamentoD['Match'] == 'Y')]   
   dfnewestatistica      = dfnewestatistica.append(df1nome1nome)
   

   dfforD ,dfocoD        = calculanaomapeado(MapeamentoC,dfocoC,dfnewestatistica)
   MapeamentoE          = calculaMapeamentoEstatistica(dfforD,dfocoD,'SplitFORB','SplitOCOA')
   df2nome1nome          = MapeamentoE[(MapeamentoE['Match'] == 'Y')]   
   dfnewestatistica      = dfnewestatistica.append(df2nome1nome)
   
   #Vão estar muitos nomes errados 
   
   dfnewestatistica      = dfnewestatistica.append(dfocoD)

   #Param.testedf(dfforE,'Clube','Estoril')
   #Param.testedf(dfocoE,'Clube','Estoril')
   fichocoe = iparams['dirdata'] +'rnd1ocoe'
   #fichfore = iparams['dirdata'] +'rnd1fore'
   Param.writeTabularFile(dfocoD,fichocoe)
   #Param.writeTabularFile(dfforE,fichfore)
   #No fim acrescentar os foram convocados mas não tiveram ocorrencias  
   dfnewestatistica      = dfnewestatistica.append( dfforD)
   return dfnewestatistica 


def calcMinutos(isubsin,isubsout,itipo,iclube,ijogador,ijogo,isituacao,idfocorrencia):
   if isituacao !='NC':
      if isubsout ==0 and itipo == 'T':
         v_minuto = 90
      elif isubsout == 1 and itipo == 'T':
         ocorrencia =  'Substitute out'
         aux_minuto = idfocorrencia[(idfocorrencia['Clube']==iclube)\
                     & (idfocorrencia['JogadorOCOfinal']==ijogador)\
                     & (idfocorrencia['Jogo']==ijogo)\
                     & (idfocorrencia['Ocorrencia']== ocorrencia)]\
                        .reset_index(drop=True)                 
         v_minuto =int(aux_minuto ['Minuto'][0][0:2]) 
      elif isubsin == 1 and itipo == 'S':
         ocorrencia =  'Substitute in'
         aux_minuto =   idfocorrencia[(idfocorrencia['Clube']==iclube)\
                        & (idfocorrencia['JogadorOCOfinal']==ijogador)\
                        &(idfocorrencia['Jogo']==ijogo)\
                        &(idfocorrencia['Ocorrencia']== ocorrencia)]\
                        .reset_index(drop=True)
      
         minuto = int(aux_minuto ['Minuto'][0][0:2]) 
         if int(minuto)<90  :
            v_minuto = 90 - minuto 
         else:
            v_minuto =1 
      elif isubsin==0 and itipo == 'S':
         v_minuto = 0 
   else:
      v_minuto =0

   return v_minuto
def calculaestatisticasclube(iparams,ijornada,itipochamada):
   fichjogos  = iparams['dirdata'] + iparams['jogos']  + iparams['jornadas'] + str(ijornada)
   dfjogos   = Param.readFile(fichjogos)
   dfjogosA  = dfjogos [['Jogo','Clubecasa','Clubefora','Ronda']]
   fichestatisticasclube  = iparams['dirdata'] + iparams['estatisticas']  + iparams['jornadas'] + str(ijornada)
   dfestatisticasclube   = Param.readFile(fichestatisticasclube)
   dfestatisticasclubegoals = dfestatisticasclube[(dfestatisticasclube['Estatistica']=='goals')]
   dfestatisticasclubegoals['Valor']   = dfestatisticasclubegoals['Valor'].fillna(0) 
   dfgoalsA  = pd.merge(dfestatisticasclubegoals,dfjogosA,\
                        on=('Jogo'), how='left')\
                           .reset_index(drop=True)
   dfgoalsA['Clubeoponente'] = dfgoalsA.apply(lambda row: row['Clubefora'] if row['Clube']==row['Clubecasa'] else row['Clubecasa'], axis=1)

   dfgoalsB  = pd.merge(dfgoalsA,dfestatisticasclubegoals,\
                        left_on=('Jogo','Clubeoponente'),right_on=('Jogo','Clube'), how='left')\
                           .reset_index(drop=True) 
   
   if itipochamada =='placonv': 
      dfgoalsC   =dfgoalsB [['Jogo','Clube_x','Valor_x','Valor_y','Ronda']]
   elif itipochamada =='estat':
      dfgoalsC   =dfgoalsB [['Jogo','Clube_x','Valor_x','Valor_y']]
   dfgoalsC.rename(columns={'Clube_x': 'Clube','Valor_x': 'Golosmarcados','Valor_y': 'Golossofridos'}, inplace=True)   
   dfgoalsC['Resultado'] = dfgoalsC.apply(lambda row: 'D' if int(row['Golosmarcados'])< int(row['Golossofridos']) 
         else ('V' if int(row['Golosmarcados'])> int(row['Golossofridos']) else 'E'),axis=1)

   dfgoalsC['BonussemSofrer'] = dfgoalsC.apply(lambda row: 1 if int(row['Golossofridos'])==0 else 0,axis=1)   
   dfgoalsC['SubsemMarcar'] = dfgoalsC.apply(lambda row: -1 if int(row['Golosmarcados'])==0 else 0,axis=1)    
   dfgoalsC['BonusResultado'] = dfgoalsC.apply(lambda row: -1 if row['Resultado']=='D' else (1 if row['Resultado']=='V' else 0),axis=1)
   dfgoalsC['Dif2Golos'] = dfgoalsC.apply(lambda row: 1 if int(row['Golosmarcados']) -int(row['Golossofridos']) > 2 
         else (-1 if int(row['Golossofridos'])- int(row['Golosmarcados'])>2 else 0),axis=1)
                       
   return dfgoalsC





def newcalcSituacao(isubsin,isubsout,itipo):
   if isubsout==0 and itipo == 'T':
      v_situacao = 'T'
   elif isubsout==1 and itipo == 'T':
      v_situacao = 'TS'
   elif isubsin==1 and itipo == 'S':
      v_situacao = 'SU'
   elif isubsin==0  and itipo == 'S':
      v_situacao = 'SNU'
   else:
      v_situacao ='NC'
   return v_situacao

def readestatisticasjogo(iparams,ijornada): 
 
    #calcular a ronda -5 , com jornada >0 para ligar com a liga record
     #Ligar a Formacao/Ocorrencia a Ronda no ficheiro jogo
    #Ligar o Mapeamento a Formacao/Ocorrencia(EstatisticaJogador) 
    #Ligar o Mapeamento a plantelconvocados da Liga Record 
    #campos de ligacao : Jogador , Clube , Posicao , Ronda
      #JogadorMap - Jogador(EstatisticasJogador) , ClubeMap- Clube(EstatisticasJogador)
       #Ronda
   fichjogos  = iparams['dirdata'] + iparams['jogos']  + iparams['jornadas'] + str(ijornada)
   dfjogos   = Param.readFile(fichjogos)
   dfjogosA  = dfjogos[['Jogo','Ronda']]

   fichformacao =iparams['dirdata'] + iparams['formacao']  + iparams['jornadas'] + str(ijornada)
   dfformacao = Param.readFile(fichformacao)
   dfformacao['JogadorFOR']=dfformacao.apply (lambda row:Mapeamento.removerAcentosECaracteresEspeciais(row['Jogador']),axis=1)
   #Primeiro Nome
   dfformacao['SplitFORA']  =dfformacao.apply(lambda row: Mapeamento.splitRow(row['JogadorFOR'], 0), axis=1)
   #Segundo nome
   dfformacao['SplitFORB']  =dfformacao.apply(lambda row: Mapeamento.splitRow(row['JogadorFOR'], 1), axis=1)  

   dfformacaoronda = pd.merge(dfformacao,dfjogosA,\
                        on=('Jogo'), how='left')\
                           .reset_index(drop=True)
   

   fichocorrencias = iparams['dirdata'] + iparams['ocorrencias'] + iparams['jornadas'] + str(ijornada)
   dfocorrencias = Param.readFile(fichocorrencias)
   dfocorrencias.rename(columns={'Jogador': 'JogadorOCOfinal'}, inplace=True)
   dfocorrenciasA  = dfocorrencias [['JogadorOCOfinal','Minuto','Ocorrencia','Clube','Jogo']]
   dfocorrenciasA['JogadorOCO'] = dfocorrenciasA.apply (lambda row:Mapeamento.removerAcentosECaracteresEspeciais(row['JogadorOCOfinal']),axis=1)

   #Primeiro Nome
   dfocorrenciasA['SplitOCOA']  =dfocorrenciasA.apply(lambda row: Mapeamento.splitRow(row['JogadorOCO'], 0), axis=1)
   #Segundo nome
   dfocorrenciasA['SplitOCOB']  =dfocorrenciasA.apply(lambda row: Mapeamento.splitRow(row['JogadorOCO'], 1), axis=1)  

   dfocorrenciasA['Goal']           = dfocorrenciasA.apply(lambda row: 1 if row['Ocorrencia']=='Goal' else 0, axis=1)
   dfocorrenciasA['Penalty goal']   = dfocorrenciasA.apply(lambda row: 1 if row['Ocorrencia']=='Penalty goal' else 0, axis=1)
   dfocorrenciasA['Own goal']       = dfocorrenciasA.apply(lambda row: 1 if row['Ocorrencia']=='Own goal' else 0, axis=1)
   dfocorrenciasA['Penalty missed'] = dfocorrenciasA.apply(lambda row: 1 if row['Ocorrencia']=='Penalty missed' else 0, axis=1)
   dfocorrenciasA['Penalty save']   = dfocorrenciasA.apply(lambda row: 1 if row['Ocorrencia']=='Penalty save' else 0, axis=1)
   dfocorrenciasA['Yellow card']    = dfocorrenciasA.apply(lambda row: 1 if row['Ocorrencia']=='Yellow card' else 0, axis=1)
   dfocorrenciasA['Red card']       = dfocorrenciasA.apply(lambda row: 1 if row['Ocorrencia']=='Red card' else 0, axis=1)
   dfocorrenciasA['Yellow 2nd/RC']  = dfocorrenciasA.apply(lambda row: 1 if row['Ocorrencia']=='Yellow 2nd/RC' else 0, axis=1)
   dfocorrenciasA['Substitute in']  = dfocorrenciasA.apply(lambda row: 1 if row['Ocorrencia']=='Substitute in' else 0, axis=1)
   dfocorrenciasA['Substitute out'] = dfocorrenciasA.apply(lambda row: 1 if row['Ocorrencia']=='Substitute out' else 0, axis=1)    
   dfocorrenciasB  =dfocorrenciasA [['JogadorOCO','SplitOCOA','SplitOCOB','JogadorOCOfinal','Clube','Jogo','Goal','Penalty goal'\
                                        ,'Own goal','Penalty missed','Penalty save'\
                                        ,'Yellow card','Red card','Yellow 2nd/RC','Substitute in','Substitute out']]
   dfocorrenciasC  =dfocorrenciasB.groupby(['JogadorOCO','SplitOCOA','SplitOCOB','JogadorOCOfinal','Clube','Jogo'],as_index=False)\
                                .agg({"Goal": "sum"\
                                     ,"Penalty goal": "sum"\
                                     ,'Own goal': "sum"\
                                     ,'Penalty missed': "sum"\
                                     ,'Penalty save': "sum"\
                                     ,'Yellow card': "sum"\
                                     ,'Red card': "sum"\
                                     ,'Yellow 2nd/RC': "sum"\
                                     ,'Substitute in': "sum"\
                                    ,'Substitute out': "sum"\
                                     })
   
   
   #Sera necessário fazer uma correspondencia entre os nomes dos jogadores da occorencia 
   # e da formacao
   dfestatisticas   = formacaoocorrencia(iparams,dfformacaoronda,dfocorrenciasC)

   dfestatisticas['Goal']             = dfestatisticas['Goal'].fillna(0)
   dfestatisticas['Penalty goal']     = dfestatisticas['Penalty goal'].fillna(0)
   dfestatisticas['Own goal']         = dfestatisticas['Own goal'].fillna(0)
   dfestatisticas['Penalty missed']   = dfestatisticas['Penalty missed'].fillna(0)
   dfestatisticas['Penalty save']     = dfestatisticas['Penalty save'].fillna(0)
   dfestatisticas['Yellow card']      = dfestatisticas['Yellow card'].fillna(0)
   dfestatisticas['Red card']         = dfestatisticas['Red card'].fillna(0)
   dfestatisticas['Yellow 2nd/RC']    = dfestatisticas['Yellow 2nd/RC'].fillna(0)       
   dfestatisticas['Substitute in']    = dfestatisticas['Substitute in'].fillna(0)  
   dfestatisticas['Substitute out']   = dfestatisticas['Substitute out'].fillna(0)  
   dfestatisticas['Situacao']         = dfestatisticas.apply(lambda row:newcalcSituacao(row['Substitute in'],row['Substitute out'],row['Tipo']), axis=1)
   dfestatisticas.rename(columns={'Jogador_x': 'Jogador'}, inplace=True)
   #teste = dfocorrenciasA[(dfocorrenciasA['Clube']=='Paços Ferreira')\
   #               &(dfocorrenciasA['Jogo']==36)]\
   #              .reset_index(drop=True)
   dfestatisticas['MinutosJogados']  = dfestatisticas.apply(lambda row:calcMinutos(row['Substitute in'],row['Substitute out'],row['Tipo'],row['Clube'],row['JogadorOCOfinal'], row['Jogo'],row['Situacao'],dfocorrenciasA), axis=1)
   

   dfestatisticas                     = dfestatisticas.drop(['JogadorFOR','SplitFORA','SplitFORB','JogadorOCO'
                                                            ,'SplitOCOA','SplitOCOB','JogadorOCOfinal','Match'],axis=1)     
   
   dfestatisticas.rename(columns={'Tipo': 'TipoAAPO'}, inplace=True)   
   estatisticasclube = calculaestatisticasclube(iparams,ijornada,'estat')
   
   dfestatisticasA  = pd.merge(dfestatisticas,estatisticasclube,\
                        on=('Jogo','Clube'), how='left')\
                           .reset_index(drop=True)

   
   dfestatisticasA['BonusjogsemSofrer'] = dfestatisticasA.apply(lambda row: 2 if int(row['Golossofridos'])==0 and row['Posicao']=='G' 
                                                                   else ( 1 if int(row['Golossofridos'])==0 and row['Posicao']=='D' else 0 ),axis=1)

   dfestatisticasA['BonusHattrick'] = dfestatisticasA.apply(lambda row: 5 if int(row['Goal'])>=3 else 0,axis=1)   
   dfestatisticasA['SubRedCard'] = dfestatisticasA.apply(lambda row: -3 if int(row['Red card'])==1 else 0,axis=1)       
   dfestatisticasA['SubYellowRC'] = dfestatisticasA.apply(lambda row: -1 if int(row['Yellow 2nd/RC'])==1 else 0,axis=1)  
   dfestatisticasA['DifGRGoals'] = dfestatisticasA.apply(lambda row: -2*int(row['Golossofridos']) if int(row['Golossofridos'])>0 and row['Posicao']=='G' else 2,axis=1)                                                      
   dfestatisticasA['DifDFGoals'] = dfestatisticasA.apply(lambda row: -1*int(row['Golossofridos']) if int(row['Golossofridos'])>0 and row['Posicao']=='D' else 1,axis=1) 
   dfestatisticasA['SubOwnGoals'] = dfestatisticasA.apply(lambda row: -2*int(row['Own goal']) if int(row['Own goal'])>0  else 0,axis=1) 
   dfestatisticasA['SubAVGoals'] = dfestatisticasA.apply(lambda row: -1 if int(row['Goal'])==0 and row['Posicao']=='A' and int(row['MinutosJogados'])>75 else 0,axis=1) 
   dfestatisticasA['BonusGRGoals'] = dfestatisticasA.apply(lambda row: 20*int(row['Goal']) if int(row['Goal'])>0 and row['Posicao']=='G' else 0,axis=1)  
   dfestatisticasA['BonusDFGoals'] = dfestatisticasA.apply(lambda row: 4*int(row['Goal']) if int(row['Goal'])>0 and row['Posicao']=='D' else 0,axis=1)
   dfestatisticasA['BonusMDGoals'] = dfestatisticasA.apply(lambda row: 3*int(row['Goal']) if int(row['Goal'])>0 and row['Posicao']=='M' else 0,axis=1)
   dfestatisticasA['BonusAVGoals'] = dfestatisticasA.apply(lambda row: 2*int(row['Goal']) if int(row['Goal'])>0 and row['Posicao']=='A' else 0,axis=1)
   dfestatisticasA['BonusPenaltygoal'] = dfestatisticasA.apply(lambda row: 2*int(row['Penalty goal']) if int(row['Penalty goal'])>0  else 0,axis=1)
   dfestatisticasA['BonusPenaltysave'] = dfestatisticasA.apply(lambda row: 2*int(row['Penalty save']) if int(row['Penalty save'])>0 else 0,axis=1)
   dfestatisticasA['SubPenaltymissed'] = dfestatisticasA.apply(lambda row: -2*int(row['Penalty missed']) if int(row['Penalty missed'])>0  else 0,axis=1)
   dfestatisticasA['BonusJogVencedora'] = dfestatisticasA.apply(lambda row: 1 if row['Resultado']=='V' else 0,axis=1)
   dfestatisticasA                     = dfestatisticasA.drop([ 'Resultado' ,'BonussemSofrer', 'SubsemMarcar', 'BonusResultado','Dif2Golos'],axis=1)   


   return dfestatisticasA                                       


if __name__ == "__main__":
  try:     
   params        = Param.config(Param.configFile, 'ligarecord')  
   ronda         =  int(params['rondainicial'])
   jornadalrec   = ronda + int(params['paramdiflrec'])
   estatisticasjogo = readestatisticasjogo(params,jornadalrec)
   #jogo = Param.testedf(estatisticasjogo,'Jogo',36)
   #writeEstatisticas(params)

  except KeyboardInterrupt:
     print('\n')