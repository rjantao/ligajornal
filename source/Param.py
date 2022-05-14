
import Configurations as cfg
from   time import sleep
import pandas as pd
import os
from configparser import ConfigParser
import html2text


aapoLnkPlantel='https://www.academiadasapostas.com/stats/competition/portugal-stats/63'
paginaPrincipal  = 'http://liga.record.pt/gerir-equipas/default.aspx'
enc           = 'UTF-8'
dataliga1920 = '/Users/rjantao/Experiment/Liga/DataLiga/Liga1920/'
newSeason        = '/dataliga/20202021/'

configFile = '/home/rantao/projects/devs/ligarecord/source/ligarecord.ini'


def config(filename,section):
   # create a parser
   parser = ConfigParser()
   # read config file
   parser.read(filename)
   # get section, default to postgresql
   configparams = {}
   if parser.has_section(section):
      params = parser.items(section)
      for param in params:
         configparams[param[0]] = param[1]
   else:
      raise Exception('Section {0} not found in the {1} file'.format(section, filename))
   return configparams

def paramstoasts(isection): 
   cfparams = config(configFile, isection) 
   return cfparams



def driverselenium(segundos,link):
   driver = cfg.initDriver()
   driver.get(link)
   sleep(segundos)
   return driver

def driver():
   driver = cfg.initDriver()
   return driver

def writeTabularFile(i_dataframe, iFicheiro):
   i_dataframe.to_csv(iFicheiro + '.csv', index=False, encoding='utf-8')


def writeHTMLFile(itext):
   file = open("/home/rantao/projects/devs/ligarecord/source/erros.html","wb")
   file.write(itext)
   file.close()

def readFile(iFicheiro,isep=','):
   iData = pd.read_csv(iFicheiro+'.csv',encoding='utf-8', sep=isep)
   return iData



def runDriverProxy(incrementproxy):
   proxies = cfg.getProxy()
   ipDriver = proxies['Ip'][incrementproxy]
   ipPort   = proxies['Port'][incrementproxy]
   driver   = cfg.initDriver(ipDriver,ipPort)
   return driver



def runDriver(iproxies,incrementproxy):
   ipDriver = iproxies['Ip'][incrementproxy]
   ipPort = iproxies['Port'][incrementproxy]
   driver = cfg.initDriver(ipDriver,ipPort)
   return driver


def testedf(idf,icolumn,icriterio):
  dfteste = idf[(idf[icolumn] == icriterio)]
  print(dfteste)
  return dfteste



def writeTestFile(iparams,i_dataframe, iFicheiro,isep=','):
   testedir =iparams['dirteste'] 
   for file in os.scandir(testedir):
      os.remove(file.path)
   testeficheiro = testedir + iFicheiro
   i_dataframe.to_csv(testeficheiro + '.csv', index=False, encoding='utf-8', sep=isep)