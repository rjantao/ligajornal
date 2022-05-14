import sys
import random
sys.path.append('/home/rantao/projects/devs/custom')
import projectparams
import Param
import Equipa
import JogadoresLREC
import EquipaConvocados
import EquipaRonda

from sqlalchemy.types import Integer,  String, DateTime,Numeric

def insereEquipa():
   paramsdb = projectparams.config(Param.configFile,'postgresql') 
   params = projectparams.config(Param.configFile, 'ligarecord')
   engine = projectparams.connect(paramsdb) 
   dfequipas = Equipa.readEquipas(params)
   print(dfequipas)                                
   dfequipas.to_sql('equipas'
       ,engine
       ,schema='public'
       ,if_exists ='replace'
       ,index=False
       ,dtype={"idequipa": Integer
              ,"nomeEquipa": String(100)     
              })  
def insereJogadores():
   paramsdb = projectparams.config(Param.configFile,'postgresql') 
   params = projectparams.config(Param.configFile, 'ligarecord')
   engine = projectparams.connect(paramsdb) 
   dfjogadores = JogadoresLREC.readJogadoresLREC(params)
   print(dfjogadores)
   dfjogadores.to_sql('jogadores'
       ,engine
       ,schema='public'
       ,if_exists ='replace'
       ,index=False
       ,dtype={"jogador": String(100)
              ,"clube": String(100)    
              ,"posicao": String(50)
              ,"valoratual": Numeric(15)  
              ,"valorinicial": Numeric(15)  
              }) 

def insereEquipaConvocados():
   paramsdb     = projectparams.config(Param.configFile,'postgresql') 
   params       = projectparams.config(Param.configFile, 'ligarecord')
   engine       = projectparams.connect(paramsdb)
   plantel,  convocados   = EquipaConvocados.readTotConvocados(params)
   print(plantel)
   plantel.to_sql('plantel'
       ,engine
       ,schema='public'
       ,if_exists ='replace'
       ,index=False
       ,dtype={"jogador": String(100)
               ,"posicao": String(20)    
              ,"clube": String(50)
              ,"pontosronda": Integer  
              ,"pontostotal":  Integer 
              ,"valorinicial": String(50)
              ,"valoratual": String(50) 
              ,"idequipa":  Integer
              ,"ronda": Integer 
              ,"flexField": String(50)
              ,"plaid": Integer  
              ,"shirt": Integer 
              }) 
   print(convocados)
   convocados.to_sql('convocados'
       ,engine
       ,schema='public'
       ,if_exists ='replace'
       ,index=False
       ,dtype={"tipo": String(20)   
              ,"idequipa": String(50)  
              ,"plaid": String(50)     
              ,"ronda": Integer  
              })

def insereRondas():
   paramsdb     = projectparams.config(Param.configFile,'postgresql') 
   params       = projectparams.config(Param.configFile, 'ligarecord')
   engine       = projectparams.connect(paramsdb)
   EquipaRondas = EquipaRonda.readTotRondas(params)   
   print(EquipaRondas.info())  
   print(EquipaRondas)         

   EquipaRondas.to_sql('equiparondas'
       ,engine
       ,schema='public'
       ,if_exists ='replace'
       ,index=False
       ,dtype={"idequipa": Integer 
              ,"ranking": String(20) 
              ,"tactica": String(20) 
              ,"variacao": String(20)   
              ,"pontosronda": String(50)     
              ,"pontostotal": String(50)   
             ,"saldodisponivel": String(50)  
             ,"val11titular": String(50)
               ,"valorplantel": String(50)
              ,"ronda": Integer  
              })                                


     


         
    


if __name__ == "__main__":
  try:

   #insereRondas()
   #insereEquipaConvocados()
   #insereEquipa()
   insereJogadores()
  except KeyboardInterrupt:
     print('\n')

