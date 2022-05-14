import pandas as pd
import Param
import EquipaConvocados
import Equipa
import EstatisticasAAPO
import Mapeamento
import numpy as np



def tipoConvocacao(isituacao,iposicao):
   if isituacao is np.NAN:
      if iposicao =='TRE':
         vtipoconvocacao ='TRE'
      else:
         vtipoconvocacao ='NC'
   else:
      vtipoconvocacao = isituacao   

   return vtipoconvocacao

def readPontuacaoRondaLREC(iparams,ijornalrec,iron,iequipa,ireturn):
   plantelConvocados        = EquipaConvocados.readRondaPlantelConvocados(iparams,iron)
   
   estatististicasjogadores = EstatisticasAAPO.readestatisticasjogo(iparams,ijornalrec)
   #print(estatististicasjogadores.info())
   mapeamento               = Mapeamento.MapeamentoLRECAAPO(params,'F',ijornalrec,iron)    
   if ireturn ==1: 
      plantelconvocadosmap = pd.merge(plantelConvocados,mapeamento,\
                       on=('Jogador','Clube'), how='left')\
                        .reset_index(drop=True)  

      estatjogmap     = pd.merge(plantelconvocadosmap,estatististicasjogadores,\
                              left_on=('JogadorMAP','ClubeMAP'),right_on=('Jogador','Clube'), how='left')\
                                   .reset_index(drop=True) 
   
   elif ireturn ==2:
      plantelConvocadosequipa = plantelConvocados[plantelConvocados['IdEquipa']==iequipa]  
      plantelconvocadosmap = pd.merge(plantelConvocadosequipa,mapeamento,\
                       on=('Jogador','Clube'), how='left')\
                        .reset_index(drop=True)  

      estatjogmap     = pd.merge(plantelconvocadosmap,estatististicasjogadores,\
                              left_on=('JogadorMAP','ClubeMAP'),right_on=('Jogador','Clube'), how='left')\
                                   .reset_index(drop=True)                               
   
   pontuacaoRondaLREC =  estatjogmap[['Jogador_x','Clube_x'
   ,'Posicao_x','PontosRonda','Equipa','IdEquipa'
   ,'ValorInicial','ValorAtual','Ronda_x'
   ,'TipoLREC','Condicao','Nacionalidade','TipoAAPO'
   ,'Goal','Penalty goal','Own goal'
   ,'Penalty missed','Penalty save'
   ,'Yellow card','Red card','Yellow 2nd/RC'
   ,'Substitute in','Substitute out'
   ,'Situacao','MinutosJogados'
   ,'BonusjogsemSofrer','BonusHattrick','SubRedCard'
   ,'SubYellowRC','DifGRGoals','DifDFGoals'
   ,'SubOwnGoals','SubAVGoals','BonusGRGoals'
   ,'BonusDFGoals','BonusMDGoals','BonusAVGoals'
   ,'BonusPenaltygoal','BonusPenaltysave'
   ,'SubPenaltymissed','BonusJogVencedora'
   ]]


   #acrescentar a condicao de nao convocado já que o mapeamento é feito com apenas os convocados que são aqueles que estao na formacao
   pontuacaoRondaLREC['Convocado']  = pontuacaoRondaLREC.apply(lambda row: 'N' if row['TipoAAPO'] is np.NaN else 'Y', axis=1)
   pontuacaoRondaLREC.rename(columns={'Jogador_x': 'Jogador','Clube_x': 'Clube','Posicao_x': 'Posicao','Ronda_x':'Ronda'}, inplace=True) 
   pontuacaoRondaLREC['Goal']              = pontuacaoRondaLREC['Goal'].fillna(0)
   pontuacaoRondaLREC['Penalty goal']      = pontuacaoRondaLREC['Penalty goal'].fillna(0)
   pontuacaoRondaLREC['Own goal']          = pontuacaoRondaLREC['Own goal'].fillna(0)
   pontuacaoRondaLREC['Penalty missed']    = pontuacaoRondaLREC['Penalty missed'].fillna(0)
   pontuacaoRondaLREC['Penalty save']      = pontuacaoRondaLREC['Penalty save'].fillna(0)
   pontuacaoRondaLREC['Yellow card']       = pontuacaoRondaLREC['Yellow card'].fillna(0)
   pontuacaoRondaLREC['Red card']          = pontuacaoRondaLREC['Red card'].fillna(0)
   pontuacaoRondaLREC['Yellow 2nd/RC']     = pontuacaoRondaLREC['Yellow 2nd/RC'].fillna(0)       
   pontuacaoRondaLREC['Substitute in']     = pontuacaoRondaLREC['Substitute in'].fillna(0)  
   pontuacaoRondaLREC['Substitute out']    = pontuacaoRondaLREC['Substitute out'].fillna(0)  
   pontuacaoRondaLREC['BonusjogsemSofrer'] = pontuacaoRondaLREC['BonusjogsemSofrer'].fillna(0)       
   pontuacaoRondaLREC['BonusHattrick']     = pontuacaoRondaLREC['BonusHattrick'].fillna(0)  
   pontuacaoRondaLREC['SubRedCard']        = pontuacaoRondaLREC['SubRedCard'].fillna(0)  
   pontuacaoRondaLREC['SubYellowRC']       = pontuacaoRondaLREC['SubYellowRC'].fillna(0)  
   pontuacaoRondaLREC['DifGRGoals']        = pontuacaoRondaLREC['DifGRGoals'].fillna(0)  
   pontuacaoRondaLREC['DifDFGoals']        = pontuacaoRondaLREC['DifDFGoals'].fillna(0)  
   pontuacaoRondaLREC['SubOwnGoals']       = pontuacaoRondaLREC['SubOwnGoals'].fillna(0)  
   pontuacaoRondaLREC['SubAVGoals']        = pontuacaoRondaLREC['SubAVGoals'].fillna(0)  
   pontuacaoRondaLREC['BonusGRGoals']      = pontuacaoRondaLREC['BonusGRGoals'].fillna(0)  
   pontuacaoRondaLREC['BonusDFGoals']      = pontuacaoRondaLREC['BonusDFGoals'].fillna(0) 
   pontuacaoRondaLREC['BonusMDGoals']      = pontuacaoRondaLREC['BonusMDGoals'].fillna(0)  
   pontuacaoRondaLREC['BonusAVGoals']      = pontuacaoRondaLREC['BonusAVGoals'].fillna(0)   
   pontuacaoRondaLREC['BonusPenaltygoal']  = pontuacaoRondaLREC['BonusPenaltygoal'].fillna(0)  
   pontuacaoRondaLREC['BonusPenaltysave']  = pontuacaoRondaLREC['BonusPenaltysave'].fillna(0)  
   pontuacaoRondaLREC['SubPenaltymissed']  = pontuacaoRondaLREC['SubPenaltymissed'].fillna(0)  
   pontuacaoRondaLREC['BonusJogVencedora'] = pontuacaoRondaLREC['BonusJogVencedora'].fillna(0)  
   pontuacaoRondaLREC['TipoConvocacao']    = pontuacaoRondaLREC.apply(lambda row: tipoConvocacao(row['Situacao'],row['Posicao']), axis=1) 

   estatisticasclube = EstatisticasAAPO.calculaestatisticasclube(iparams,ijornalrec,'placonv')
   
   pontuacaoRondaLRECA  = pd.merge(pontuacaoRondaLREC,estatisticasclube,\
                        on=('Clube','Ronda'), how='left')\
                           .reset_index(drop=True)

   
   if ireturn ==3:
      return pontuacaoRondaLRECA, plantelConvocados , mapeamento
   elif ireturn ==1 or ireturn ==2:
      return pontuacaoRondaLRECA


def NewCalculoMelhorEquipa(ipontuacaoequipasjog,inomeequipa,idf,imd,iav):
   
   bestteam = pd.DataFrame([])
   plaronC1GRA = ipontuacaoequipasjog[ipontuacaoequipasjog['Posicao'] == 'GR']  
   plaronC1GRB = plaronC1GRA.nlargest(1, ['PontosRonda'])
   bestteam   = bestteam.append(plaronC1GRB, ignore_index=True)
   plaronC1DFA = ipontuacaoequipasjog[ipontuacaoequipasjog['Posicao'] == 'DF']
   plaronC1DFB = plaronC1DFA.nlargest(idf, ['PontosRonda'])
   bestteam = bestteam.append(plaronC1DFB, ignore_index=True)
   plaronC1MDA = ipontuacaoequipasjog[ipontuacaoequipasjog['Posicao'] == 'MD']
   plaronC1MDB = plaronC1MDA.nlargest(imd, ['PontosRonda'])
   bestteam = bestteam.append(plaronC1MDB, ignore_index=True)
   plaronC1AVA = ipontuacaoequipasjog[ipontuacaoequipasjog['Posicao'] == 'AV']
   plaronC1AVB = plaronC1AVA.nlargest(iav, ['PontosRonda'])   
   bestteam = bestteam.append(plaronC1AVB, ignore_index=True)
   plaronC1CAPA = ipontuacaoequipasjog[ipontuacaoequipasjog['Posicao'] != 'TRE']
   plaronC1CAPB = plaronC1CAPA.nlargest(1, ['PontosRonda'])
   plaronC1CAPB.iat[0,2]= 'CAP'
   bestteam = bestteam.append(plaronC1CAPB, ignore_index=True)
   plaronC1TREA = ipontuacaoequipasjog[ipontuacaoequipasjog['Posicao'] == 'TRE']
   plaronC1TREB = plaronC1TREA.nlargest(1, ['PontosRonda'])
   
   bestteam = bestteam.append(plaronC1TREB, ignore_index=True)
   bestteam['Equipa'] = inomeequipa
   bestteam['Tatica'] = str(idf) + 'x' + str(imd) + 'x' + str(iav)
   #bestteamB = bestteam.groupby('NomeEquipa', as_index=False).agg({"PontosRonda": "sum"})
   bestteamB = bestteam.groupby(['Equipa','Tatica'], as_index=False).agg({"PontosRonda": "sum"})
   return bestteamB ,bestteam






def calculaequipaescolhida(ipontuacaoequipa):
   equipaescolhida = pd.DataFrame([])
   transfpontuacaoequipaA = ipontuacaoequipa[ (ipontuacaoequipa['Condicao'] == 'TIT')
       & (ipontuacaoequipa['Convocado']=='Y')
       & (ipontuacaoequipa['Posicao'].isin(['GR', 'DF','MD','AV']))
       ]
   transfpontuacaoequipaB = ipontuacaoequipa[ (ipontuacaoequipa['Posicao'].isin(['TRE']))
       ]    
            
   #acrescentar o valor dos capitaes 
   transfpontuacaoequipaCAP= ipontuacaoequipa[ (ipontuacaoequipa['Posicao'] == 'CAP')
      & (ipontuacaoequipa['Convocado']=='Y')  
        ] 
   
   transfpontuacaoequipaC = ipontuacaoequipa[ (ipontuacaoequipa['Condicao'] == 'TIT')
      & (ipontuacaoequipa['Convocado']=='N')
       & (ipontuacaoequipa['Posicao'].isin(['GR', 'DF','MD','AV']))
       ]    
   
   transfpontuacaoequipaD= pd.DataFrame([])
   if transfpontuacaoequipaC.empty == False:
      suplentes = ipontuacaoequipa[ (ipontuacaoequipa['Condicao'] == 'SUP')
      & (ipontuacaoequipa['Convocado']=='Y')
       & (ipontuacaoequipa['Posicao'].isin(['GR', 'DF','MD','AV']))
       ] 

      capitao = ipontuacaoequipa[ (ipontuacaoequipa['Posicao'] == 'CAP')
          & (ipontuacaoequipa['Convocado']=='N')
       ]   

      
      for index, row in transfpontuacaoequipaC.iterrows():    
         suplentesPossiveis = pd.DataFrame([]) 
         suplentesPossiveis =  suplentes[ (suplentes['Posicao'] == row['Posicao'])]
         if suplentesPossiveis.empty==False:
            suplentesPossiveisA = suplentesPossiveis.nlargest(1, ['PontosRonda'])
            indexsuplente = suplentesPossiveisA.index.values.astype(int)[0]
            transfpontuacaoequipaD = transfpontuacaoequipaD.append(suplentesPossiveisA,ignore_index=True)
            if capitao.empty==False:
               #verificar se o jogador a substituir é o capitao
               validacapitao  = capitao[ (capitao['Jogador'] == row['Jogador'])
                & (capitao['Clube']==row['Clube'])
                & (capitao['Posicao']=='CAP')
               ]
               if validacapitao.empty==False:
                  transfpontuacaoequipaD = transfpontuacaoequipaD.append(suplentesPossiveisA,ignore_index=True)
            suplentes = suplentes.drop([indexsuplente])
         else:  
            #nºao encontrou nenhum suplente que possa entrar para aquela posicao 
            titnaoconvocado =pd.DataFrame({'Equipa':row['Equipa']
                          ,'IdEquipa': row['IdEquipa']
                          ,'Jogador':row['Jogador']
                          ,'Clube':row['Clube']
                          ,'Posicao':row['Posicao']
                          ,'PontosRonda':row['PontosRonda']
                          ,'Ronda':row['Ronda']
                          ,'TipoLREC':row['TipoLREC']
                          ,'Condicao':row['Condicao'] 
                          ,'Situacao':row['Situacao']
                          ,'Convocado':row['Convocado']})
            transfpontuacaoequipaD = transfpontuacaoequipaD.append(titnaoconvocado,ignore_index=True)              

   equipaescolhida = equipaescolhida.append(transfpontuacaoequipaA, ignore_index=True)
   equipaescolhida = equipaescolhida.append(transfpontuacaoequipaB, ignore_index=True)
   if  transfpontuacaoequipaD.empty==False: 
      equipaescolhida = equipaescolhida.append(transfpontuacaoequipaD, ignore_index=True)
   if transfpontuacaoequipaCAP.empty==False:
      equipaescolhida = equipaescolhida.append(transfpontuacaoequipaCAP, ignore_index=True)

   #print(equipaescolhida)
   return equipaescolhida



def NewMelhorEquipaRonda(iparams,iron):
   jornadalrec   = iron + int(params['paramdiflrec'])
   NomeEquipas = Equipa.readEquipas(iparams)
   dfTotalRondaEquipasJogadores = pd.DataFrame([])
   dfTotalRondaEquipas          = pd.DataFrame([])
   pontuacaoLREC         = pd.DataFrame([])
   estatisticaplantel    = pd.DataFrame([])
   mapeamento            =pd.DataFrame([])
   NumEquipas = len(NomeEquipas)
   #NumEquipas = 1
   ficheiroRank = iparams['dirdata'] +'rnd' + str(iron) + 'rank' 
   dfRnd = Param.readFile(ficheiroRank)
   dfRndEquipa = pd.merge(dfRnd,NomeEquipas,\
                     left_on=('IdEquipa'),right_on=('idequipa'), how='left')\
                                   .reset_index(drop=True)  
                  
   for eqp in range(0,NumEquipas):
      vIdEquipa = NomeEquipas.loc[eqp, 'idequipa']
      vNomeEquipa = NomeEquipas.loc[eqp, 'nomeEquipa']
      pontuacaorankings= dfRndEquipa[ (dfRndEquipa['IdEquipa'] == vIdEquipa) & (dfRndEquipa['Ronda'] == iron)]
      pontuacaorankingsA = pontuacaorankings[['nomeEquipa','PontosRonda']]
      #pontuacaorankingsA.assign(Tatica='Ranking')
      pontuacaorankingsA['Tatica']='Ranking'
      pontuacaorankingsA.rename(columns={'nomeEquipa': 'Equipa'}, inplace=True)  
      pontuacaoequipasjogA     = readPontuacaoRondaLREC(iparams,jornadalrec,iron,vIdEquipa,2)
      #calcula a equipa escolhida tem em conta os suplentes e as respectivas substituicoes
      pontuacaoequipasjogB     = calculaequipaescolhida(pontuacaoequipasjogA)
      pontuacaoequipasjogB['Tatica'] ='Escolhida'
      pontuacaoequipasescolhida = pontuacaoequipasjogB.groupby(['Equipa','Tatica'], as_index=False).agg({"PontosRonda": "sum"})

      pontuacaoquipas433 ,pontuacaoquipas433jog= NewCalculoMelhorEquipa(pontuacaoequipasjogA,vNomeEquipa,4,3,3)
      pontuacaoquipas352 ,pontuacaoquipas352jog= NewCalculoMelhorEquipa(pontuacaoequipasjogA,vNomeEquipa,3,5,2)
      pontuacaoquipas343 ,pontuacaoquipas343jog= NewCalculoMelhorEquipa(pontuacaoequipasjogA,vNomeEquipa,3,4,3)
      
      pontuacaoquipas451 ,pontuacaoquipas451jog= NewCalculoMelhorEquipa(pontuacaoequipasjogA,vNomeEquipa,4,5,1)
      pontuacaoquipas442 ,pontuacaoquipas442jog= NewCalculoMelhorEquipa(pontuacaoequipasjogA,vNomeEquipa,4,4,2)
      pontuacaoquipas541 ,pontuacaoquipas541jog= NewCalculoMelhorEquipa(pontuacaoequipasjogA,vNomeEquipa,5,4,1)
      pontuacaoquipas532 ,pontuacaoquipas532jog= NewCalculoMelhorEquipa(pontuacaoequipasjogA,vNomeEquipa,5,3,2)
      
      
      dfTotalRondaEquipas = dfTotalRondaEquipas.append(pontuacaoequipasescolhida, ignore_index=True)     
      dfTotalRondaEquipas = dfTotalRondaEquipas.append(pontuacaorankingsA, ignore_index=True)
      dfTotalRondaEquipas = dfTotalRondaEquipas.append(pontuacaoquipas433, ignore_index=True)
      dfTotalRondaEquipas = dfTotalRondaEquipas.append(pontuacaoquipas343, ignore_index=True)
      dfTotalRondaEquipas = dfTotalRondaEquipas.append(pontuacaoquipas352, ignore_index=True)
      dfTotalRondaEquipas = dfTotalRondaEquipas.append(pontuacaoquipas451, ignore_index=True)
      dfTotalRondaEquipas = dfTotalRondaEquipas.append(pontuacaoquipas442, ignore_index=True)
      dfTotalRondaEquipas = dfTotalRondaEquipas.append(pontuacaoquipas541, ignore_index=True)
      dfTotalRondaEquipas = dfTotalRondaEquipas.append(pontuacaoquipas532, ignore_index=True)

         
      dfTotalRondaEquipasJogadores = dfTotalRondaEquipasJogadores.append(pontuacaoequipasjogB, ignore_index=True)
      dfTotalRondaEquipasJogadores = dfTotalRondaEquipasJogadores.append(pontuacaoquipas433jog, ignore_index=True)
      dfTotalRondaEquipasJogadores = dfTotalRondaEquipasJogadores.append(pontuacaoquipas343jog, ignore_index=True)
      dfTotalRondaEquipasJogadores = dfTotalRondaEquipasJogadores.append(pontuacaoquipas352jog, ignore_index=True)
      dfTotalRondaEquipasJogadores = dfTotalRondaEquipasJogadores.append(pontuacaoquipas451jog, ignore_index=True)
      dfTotalRondaEquipasJogadores = dfTotalRondaEquipasJogadores.append(pontuacaoquipas442jog, ignore_index=True)
      dfTotalRondaEquipasJogadores = dfTotalRondaEquipasJogadores.append(pontuacaoquipas541jog, ignore_index=True)
      dfTotalRondaEquipasJogadores = dfTotalRondaEquipasJogadores.append(pontuacaoquipas532jog, ignore_index=True)


   #Param.writeTestFile(params,dfTotalRondaEquipasJogadores , 'testeronda1',';') 
   return dfTotalRondaEquipas,dfTotalRondaEquipasJogadores
   

def writeTotMelhorEquipa(iparams):
   ini = 1
   #ini = int(iparams['rondainicial']) 
   #fim = int(iparams['rondafinal']) 
   fim  = 2
   for ronda in range(ini, fim):
      
      dfmelhorEquiparonda,dfmelhorEquiparondajog = NewMelhorEquipaRonda(iparams,ronda) 
      fichmelhorequipa = iparams['dirdata'] +'rnd' +str(ronda) +'melhorequipa'
      fichmelhorequipajog = iparams['dirdata'] +'rnd' +str(ronda) +'melhorequipajog'
      Param.writeTabularFile(dfmelhorEquiparonda,fichmelhorequipa)
      Param.writeTabularFile(dfmelhorEquiparondajog,fichmelhorequipajog)
      #dfmelhorEquipatotal = dfmelhorEquipatotal.append(melhorEquiparonda, ignore_index=True)


   



if __name__ == "__main__":
  try:
   params = Param.config(Param.configFile, 'ligarecord') 
   ronda  =  int(params['rondainicial']) 
   jornadalrec = ronda + int(params['paramdiflrec'])
   #numequipa = 26593

   #NewMelhorEquipaRonda(params,1)
   writeTotMelhorEquipa(params)
 
   #pontuacaoequipasjogA     = readPontuacaoRondaLREC(params,jornadalrec,ronda,numequipa,2)  
   #pontuacaoequipasjogB     = calculaequipaescolhida(pontuacaoequipasjogA)
   #Param.writeTestFile(params,pontuacaoequipasjogA, 'teste26593') 
  except KeyboardInterrupt:
     print('\n')