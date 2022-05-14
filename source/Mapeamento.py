
import Param
import pandas as pd
import numpy as np
import unicodedata
import re


#compara campos entre dataframes
def fieldprint(idf1,idf2,ifield1,ifield2):
    sortdfidf1      =idf1.sort_values(ifield1)
    dffields1       =sortdfidf1[ifield1].unique()    
    sortdfidf2 =  idf2.sort_values(ifield2) 
    dffields2      = sortdfidf2[ifield2].unique()


def diffjogadores(iparams,idfJogadoresAAPO, idfJogadoresAAPO2, which = None):
    """
    Find rows which are different between two DataFrames.
    """
    comparison_df = idfJogadoresAAPO.merge(
      idfJogadoresAAPO2,
      indicator = True,
      how = 'outer'
      )
    if which is None:
      diff_df = comparison_df[comparison_df['_merge'] != 'both']
    else :
      diff_df = comparison_df[comparison_df['_merge'] == which]
    diffjogadoresfich =  iparams['dirdata'] + 'diffjogadores'
    #Param.writeTabularFile(diff_df, diffjogadoresfich ) 
    
    return diff_df


def excepcoes(iparams,itipo,iparamA,iparamB = None,iparamC=None):
  excJogDisp         = iparams['dirdata'] + iparams['excepcoesfile']
  dfexcJogDisp       = Param.readFile(excJogDisp,';')
  if itipo=='A':
     dfexcJogDispTipoA   = dfexcJogDisp[(dfexcJogDisp['ParametroA'] == iparamA)]
     dfexcJogDispTipoB   = dfexcJogDispTipoA[['Origem','Destino']]
  elif itipo=='B':
     dfexcJogDispTipoA   = dfexcJogDisp[(dfexcJogDisp['ParametroA'] == iparamA)&(dfexcJogDisp['ParametroB'] == iparamB)] 
     dfexcJogDispTipoB   = dfexcJogDispTipoA[['Origem','Destino']] 
  elif itipo=='C':
     dfexcJogDispTipoA   = dfexcJogDisp[(dfexcJogDisp['ParametroA'] == iparamA)&(dfexcJogDisp['ParametroB'] == iparamB)  &(dfexcJogDisp['ParametroC'] == iparamC) ]    
     dfexcJogDispTipoB   = dfexcJogDispTipoA[['Origem','Destino']]  
  return dfexcJogDispTipoB





def jogadoresDispensados(idflrecdisp):
  NewMapJogadorLrecAdisp = idflrecdisp[(idflrecdisp['Match'] == 'Y')]
  NewMapJogadorLrecAdisp = NewMapJogadorLrecAdisp.drop(['Match','Origem','Destino','Posicao'],axis=1)
  NewMapJogadorLrecAdisp['ClubeMAP'] = 'N'
  NewMapJogadorLrecAdisp['JogadorMAP'] = 'N'
  NewMapJogadorLrecAdisp['Motivos'] = 'JogadoresDispensados'
  NewMapJogadorLrecAdisp['Site'] = 'LREC'
  return NewMapJogadorLrecAdisp





def removerAcentosECaracteresEspeciais(palavra):
    # Unicode normalize transforma um caracter em seu equivalente em latin.
   nfkd = unicodedata.normalize('NFKD', palavra)
   palavraSemAcento = u"".join([c for c in nfkd if not unicodedata.combining(c)])

    # Usa expressão regular para retornar a palavra apenas com números, letras e espaço
   return re.sub('[^a-zA-Z0-9 \\\]', '', palavraSemAcento)

def splitRow(ifield,word):
   spl_lrec     = ifield.upper().split()
   if word == 1:
      if len(spl_lrec) < word+1:
        v_split = spl_lrec[0]
      else:
        v_split = spl_lrec[1]
   else:
      if len(spl_lrec) ==0:
         v_split = ifield.upper()
      else:
         v_split = spl_lrec[0] 
   return v_split


def calculajogadoresAAPO(iparams,itipo,ijor):
  if itipo =='O':
    fichaapo=  iparams['dirdata'] + iparams['ocorrencias'] + iparams['jornadas']+str(ijor)
  elif itipo =='F':
    fichaapo =  iparams['dirdata'] + iparams['formacao'] + iparams['jornadas'] + str(ijor)

  #temos de tirar os que vem com acento e sem acento  

  JogadorAAPO = Param.readFile(fichaapo)
  #apaga os duplicados dos jogadores , já que estes são titulares em vários e vao se repetir
  #ficando assim śo os jogadores que participaram nos jogos
  if itipo=='F':
    JogadorAAPOA = JogadorAAPO[['Jogador','Clube','Posicao']]
    JogadorAAPOA = JogadorAAPOA[['Jogador','Clube','Posicao']].drop_duplicates().reset_index(drop=True)
    JogadorAAPOA['JogadorLRECAAPO']       =JogadorAAPOA.apply (lambda row:removerAcentosECaracteresEspeciais(row['Jogador']),axis=1)
    JogadorAAPOB = JogadorAAPOA[['Jogador','JogadorLRECAAPO','Clube','Posicao']]
    JogadorAAPOB['Posicao']           = JogadorAAPOB['Posicao'].replace('G','GR')
    JogadorAAPOB['Posicao']           = JogadorAAPOB['Posicao'].replace('D','DF')
    JogadorAAPOB['Posicao']           = JogadorAAPOB['Posicao'].replace('M','MD')
    JogadorAAPOB['Posicao']           = JogadorAAPOB['Posicao'].replace('A','AV')
    JogadorAAPOB.rename(columns={'Posicao': 'PosicaoMAP'}, inplace=True) 
  
  elif itipo=='O':
    JogadorAAPOA = JogadorAAPO[['Jogador','Clube']]
    #remover os acentos e ficar só com um dos jogadores que tem acento
    JogadorAAPOA['JogadorLRECAAPO']       =JogadorAAPOA.apply (lambda row:removerAcentosECaracteresEspeciais(row['Jogador']),axis=1) 
    JogadorAAPOB = JogadorAAPOA[['JogadorLRECAAPO','Clube']].drop_duplicates().reset_index(drop=True)

  JogadorAAPOB.rename(columns={'Jogador': 'JogadorMAP','Clube':'ClubeMAP'}, inplace=True)  
  #Modificar o clube              
  
  #Primeiro Nome
  JogadorAAPOB['SplitAAPOA']  =JogadorAAPOA.apply(lambda row: splitRow(row['JogadorLRECAAPO'], 0), axis=1)
  #Segundo nome
  JogadorAAPOB['SplitAAPOB']  =JogadorAAPOA.apply(lambda row: splitRow(row['JogadorLRECAAPO'], 1), axis=1)         

  dfexcClubes =  excepcoes(iparams,'A','AAPOClubeFormacao') 
  JogadorAAPOC  = pd.merge(JogadorAAPOB,dfexcClubes ,\
                            left_on=('ClubeMAP'),right_on='Origem', how='left')\
                           .reset_index(drop=True) 
  JogadorAAPOC['ClubeLRECAAPO']= JogadorAAPOC.apply(lambda row: row['ClubeMAP'] if row['Destino'] is np.NaN else row['Destino'], axis=1) 
  JogadorAAPOC = JogadorAAPOC.drop(['Origem','Destino'],axis=1)
    
  return JogadorAAPOC


def calculajogadoresLREC(iparams):
  listajoglrec     = iparams['dirdata'] + iparams['listajoglrec']
  jogadorLREC  = Param.readFile(listajoglrec)
  dfjogadoresLREC = jogadorLREC[['Jogador', 'Clube', 'Posicao']]
  #Esta lista varia durante o ano, esta lista é feita com base na lista dos jogadores do plantel
  #Os jogadores da site liga record é que vao ser mapeados com os outros sites, neste caso com academia de apostas
  #Observacoes :Jogadores com o minuto 0 ou excluidos    
  dfexcJogDisp       = excepcoes(iparams,'A','JOGDISP')   
  dfjogadoresLRECA  = pd.merge(dfjogadoresLREC,dfexcJogDisp  ,\
                            left_on=('Jogador'),right_on='Destino', how='left')\
                           .reset_index(drop=True)
  dfjogadoresLRECA['Match'] = dfjogadoresLRECA.apply(lambda row: 'N' if row['Destino'] is np.NaN else row['Origem'], axis=1) 
  dfjogadoresLRECA           = dfjogadoresLRECA.replace(to_replace =["Guarda Redes"], value ="GR")
  dfjogadoresLRECA           = dfjogadoresLRECA.replace(to_replace =["Avançado"], value ="AV")
  dfjogadoresLRECA           = dfjogadoresLRECA.replace(to_replace =["Defesa"], value ="DF")
  dfjogadoresLRECA           = dfjogadoresLRECA.replace(to_replace =["Médio"], value ="MD")
  dfjogadoresLRECB           = dfjogadoresLRECA[(dfjogadoresLRECA['Match'] == 'N')]
  dfjogadoresLRECB           = dfjogadoresLRECB.drop(['Match','Origem','Destino'],axis=1)
  #Remove carateres especiais dos nomes dos jogadores da liga record, será o 1 criterio de comparacao
  dfjogadoresLRECB['JogadorLREC'] = dfjogadoresLRECB.apply(lambda row:removerAcentosECaracteresEspeciais(row['Jogador']),axis=1)
  #Separa o nome em 2 nomes colocando a letra grande, será 2 e 3 criterio de comparacao
  dfjogadoresLRECB['SplitLRECA'] = dfjogadoresLRECB.apply(lambda row: splitRow(row['JogadorLREC'], 0), axis=1)
  dfjogadoresLRECB['SplitLRECB'] = dfjogadoresLRECB.apply(lambda row:splitRow(row['JogadorLREC'],1),axis=1) 
  return dfjogadoresLRECB




#a magia de comparacao está neste calculo
def calculoRelLrecAAPO(idfLrec,idfAAPO,icriteriojogLrec,icriterioclubeLrec,icriterioposA,icriteriojogA,icriterioclubeA,icriterioposB,iflagpos='Y'):

  if iflagpos =='Y':
    relLrecAAPO= pd.merge(idfLrec,idfAAPO,\
                            left_on=(icriteriojogLrec,icriterioclubeLrec,icriterioposA),right_on=(icriteriojogA,icriterioclubeA,icriterioposB), how='left')\
                           .reset_index(drop=True)
  elif  iflagpos =='N':
    relLrecAAPO= pd.merge(idfLrec,idfAAPO,\
                            left_on=(icriteriojogLrec,icriterioclubeLrec),right_on=(icriteriojogA,icriterioclubeA), how='left')\
                           .reset_index(drop=True)

  
  relLrecAAPO['Match'] = relLrecAAPO.apply(lambda row: 'N' if row[icriteriojogA] is np.NaN else 'Y', axis=1)

  return relLrecAAPO

#carregamento para a tabela de mapeamento
def jogadoresmapeados(imapeamentoLrec,ivalidacao,icontrole,icolumns,iMatch):
  dfjogadoresmapeados     = imapeamentoLrec[(imapeamentoLrec['Match'] == iMatch)]
  dfjogadoresmapeados     = dfjogadoresmapeados.drop(icolumns,axis=1)
  dfjogadoresmapeados ['TipoValidacao'] = ivalidacao
  dfjogadoresmapeados ['TipoControle'] = icontrole
  return dfjogadoresmapeados 




def calculaMapeamento(icalcLREC,icalcAAPO,icriterioA,icriterioB,ivalidacao,iflagpos,icontrole):
  Mapeamento    =  calculoRelLrecAAPO(icalcLREC ,icalcAAPO ,icriterioA,'Clube','Posicao',icriterioB,'ClubeLRECAAPO','PosicaoMAP',iflagpos)
  columnsdrop    = ['Match','JogadorLREC','JogadorLRECAAPO','SplitLRECA','SplitLRECB','SplitAAPOA','SplitAAPOB','ClubeLRECAAPO']
  dfcriterio     = jogadoresmapeados(Mapeamento,ivalidacao,icontrole,columnsdrop,'Y')
  return dfcriterio , Mapeamento
    
def calculaLRECAAPO(idflrec,idfaapo,imapeamentos,itipo):
  lrecA                      = idflrec[(idflrec['Match'] == 'N')]  
  lrecaMapear                = lrecA[['Jogador', 'Clube', 'Posicao','JogadorLREC','SplitLRECA','SplitLRECB']]  

  if itipo=='F':
    AAPOJogadores              = pd.merge(idfaapo,imapeamentos,\
                            on=('JogadorMAP','ClubeMAP','PosicaoMAP'), how='left')\
                           .reset_index(drop=True)
  elif itipo=='O':
    AAPOJogadores              = pd.merge(idfaapo,imapeamentos,\
                            on=('JogadorMAP','ClubeMAP'), how='left')\
                           .reset_index(drop=True)
  
  AAPOJogadores['Match']     = AAPOJogadores.apply(lambda row: 'N' if row['Jogador'] is np.NaN else 'Y', axis=1)  
  AAPOJogadoresA             = AAPOJogadores[(AAPOJogadores['Match'] == 'N')]                       
  if itipo=='F':
    AAPOJogadoresaMapear     = AAPOJogadoresA[['JogadorMAP','ClubeMAP','PosicaoMAP','SplitAAPOA','SplitAAPOB','ClubeLRECAAPO','JogadorLRECAAPO']] 
  elif itipo=='O':
    AAPOJogadoresaMapear     = AAPOJogadoresA[['JogadorMAP','ClubeMAP','SplitAAPOA','SplitAAPOB','ClubeLRECAAPO','JogadorLRECAAPO']] 
  return lrecaMapear, AAPOJogadoresaMapear



def MapeamentoLRECAAPO(iparams,itipo,ijor,iron):
  dfmapeamentos           = pd.DataFrame([])  
  #jogadores da liga record 
  LRECJog          = calculajogadoresLREC(iparams)
  #AAPOFormacaoJog  = jogadoresAAPOFormacao(iparams)
  AAPOJog  = calculajogadoresAAPO(iparams,itipo,ijor)
   #os jogadores da liga record vao ter de um mapeamento com o dataset formacoes de jogadores da academia de apostas
   #os jogadores da liga record vao ter de um mapeamento com o dataset ocorrencias de jogadores da academia de apostas
  if itipo=='F':
    v_controle = 'AAPOFormacao'
  elif itipo=='O': 
    v_controle = 'AAPOOcorrencia'

  flagposicoes = ['Y','N'] 
  for flagposicao in flagposicoes:
    if flagposicao=='Y':
      #1 criterio nome completo
      dfnomecompleto,JogadoresLRECaMapear   = calculaMapeamento(LRECJog,AAPOJog,'JogadorLREC','JogadorLRECAAPO','nomecompleto',flagposicao,v_controle)
      dfmapeamentos    = dfmapeamentos.append(dfnomecompleto, ignore_index=True)
      #Param.testedf(LRECJog,'Jogador','Kenji Gorré') 
      
      
      #2 criterio 1nome1nome
      #continua o calculo com o universo completo menos os jogadores mapeados, e assim sucessivamente até ao fim.
      LRECJogA , AAPOJogA = calculaLRECAAPO(JogadoresLRECaMapear,AAPOJog,dfmapeamentos,itipo)  
      df1nome1nome,JogadoresLRECaMapearA   = calculaMapeamento(LRECJogA,AAPOJogA ,'SplitLRECA','SplitAAPOA','1nome1nome',flagposicao,v_controle)
      dfmapeamentos                       = dfmapeamentos.append(df1nome1nome, ignore_index=True)
      #3 criterio 1nome2nome
      LRECJogB , AAPOJogB = calculaLRECAAPO(JogadoresLRECaMapearA,AAPOJogA,dfmapeamentos,itipo)  
      df1nome2nome,JogadoresLRECaMapearB   = calculaMapeamento(LRECJogB,AAPOJogB ,'SplitLRECA','SplitAAPOB','1nome2nome',flagposicao,v_controle)
      dfmapeamentos                       = dfmapeamentos.append(df1nome2nome, ignore_index=True)
    elif flagposicao=='N':
      #4 criterio nome completo sem a posicao
      LRECJogC , AAPOJogC = calculaLRECAAPO(JogadoresLRECaMapearB,AAPOJogB,dfmapeamentos,itipo)   
      dfnomecompletosp,JogadoresLRECaMapearC   = calculaMapeamento(LRECJogC,AAPOJogC ,'JogadorLREC','JogadorLRECAAPO','nomecompletosp','N','AAPOFormacao')
      dfmapeamentos                       = dfmapeamentos.append(dfnomecompletosp, ignore_index=True)
      

      #5 criterio 1nome1nome sem posicao
      LRECJogD , AAPOJogD = calculaLRECAAPO(JogadoresLRECaMapearC,AAPOJogC,dfmapeamentos,itipo)  
      df1nome1nomesp,JogadoresLRECaMapearD   = calculaMapeamento(LRECJogD,AAPOJogD ,'SplitLRECA','SplitAAPOA','1nome1nomesp',flagposicao,v_controle)
      dfmapeamentos                       = dfmapeamentos.append(df1nome1nomesp, ignore_index=True)

      #6 criterio 1nome2nome sem posicao
      LRECJogE , AAPOJogE = calculaLRECAAPO(JogadoresLRECaMapearD,AAPOJogD,dfmapeamentos,itipo)  
      df1nome2nomesp,JogadoresLRECaMapearE   = calculaMapeamento(LRECJogE,AAPOJogE,'SplitLRECA','SplitAAPOB','1nome2nomesp',flagposicao,v_controle)
      dfmapeamentos                          = dfmapeamentos.append(df1nome2nomesp, ignore_index=True)
    
  LRECJogF , AAPOJogF = calculaLRECAAPO(JogadoresLRECaMapearE,AAPOJogE,dfmapeamentos,itipo) 
  dfexcJogador =  excepcoes(iparams,'A','AAPOJogador') 
  AAPOJogG   = pd.merge(AAPOJogF,dfexcJogador  ,\
                            left_on=('JogadorMAP'),right_on='Origem', how='left')\
                           .reset_index(drop=True)   
  dfexcepcoesnome,JogadoresLRECaMapearF   = calculaMapeamento(LRECJogF,AAPOJogG ,'Jogador','Destino','excepcoesnome','N','AAPOFormacao')
  dfmapeamentos                       = dfmapeamentos.append(dfexcepcoesnome, ignore_index=True)



  
  dfmapeamentos['Ronda'] = iron 
  dfmapeamentos = dfmapeamentos.drop(['Origem','Destino'],axis=1)
  #Param.testedf(JogadoresLRECaMapearE,'Clube','Boavista') 
  #Param.testedf(dfmapeamentos,'Clube','Boavista') 
  #Param.testedf(AAPOJogG,'ClubeMAP','Boavista') 
  #Param.testedf(LRECJogD,'Clube','Sporting')
  #os jogadores da liga record vao ter de um mapeamento com o dataset planteis de jogadores da academia de apostas
  
  return dfmapeamentos




if __name__ == "__main__":
  try:
   params            = Param.config(Param.configFile, 'ligarecord')   
   #mapLREC , mapAAPO = MapeamentoLRECAAPO(params)
   #MapeamentoLRECAAPOFormacao(params)
   ronda         = int(params['rondainicial'])
   jornadalrec   =  ronda + int(params['paramdiflrec'])
   MapeamentoLRECAAPO(params,'F',jornadalrec,ronda )
  #MapeamentoLRECAAPO(params,'O')
   #mapAAPOclube = mapAAPO[(mapAAPO['ClubeMAP'] == 'Porto')]
  except KeyboardInterrupt:
     print('\n')