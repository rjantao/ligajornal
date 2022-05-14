

--remove a virtual environment 
rm -r ligarecord



--create virtual environment
mkdir ligarecord

--change directory
cd ligarecord

-- create a virtual environment
python3 -m venv ligarecord

#activate a virtual environment
source /home/rantao/projects/devs/ligarecord/bin/activate


#pip install sqlalchemy
#pip install psycopg2


#############Configuracao de base dados#####################3

#ligar como adminstrador
sudo -u postgres psql

#mostrar os utilizadores
\du

#criar a database postgres
create database ligadb


#criar utilizador
create user liga with password 'liga';

# conceder role superuser imoveis
ALTER USER liga SUPERUSER;

#configurar a base dados no dbeaver localhost 5432

#####################################################3


Para utilizar o debug é necessário 
Python : select interperter


Proximos Passos:
FormacaoConcorrencia
  Ligar a Formacao/Ocorrencia a Ronda no ficheiro jogo


PlantelConvocados  juntar FormacaoOcorrencia(EstatisticasJogador) 
   
   Ligar o Mapeamento a Formacao/Ocorrencia(EstatisticaJogador) 
   Ligar o Mapeamento a plantelconvocados da Liga Record 
   campos de ligacao : Jogador , Clube , Posicao , Ronda
       JogadorMap - Jogador(EstatisticasJogador) , ClubeMap- Clube(EstatisticasJogador)
       Ronda
Fazer a ligacao entre a jornada e a ronda        
   
Obter o Melhor equipa




 
