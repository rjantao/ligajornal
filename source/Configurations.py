
from   selenium import webdriver
import bs4
import os
import pandas as pd
from datetime import timedelta
import requests


fire_atual=r'/home/rantao/projects/devs/geckodriver/geckodriver'
dirPath  = r'/home/rantao/projects/devs/liga/'
dirPathData  = r'/Users/rjantao/Experiment/Liga/DataLiga/Liga1920/'
browser = 'F'
enc = 'UTF-8'
# o site onde se vai buscar os proxies antes de correr o bot ,
# para ultrapassar possíveis blocker que impedem o download dos 
# dados
def getProxy():
   proxies = []
   lip = []
   lport = []
   ltypeproxy=[]
   proxies_req = requests.get('https://www.sslproxies.org/')
   proxies_source = proxies_req.text
   soup = bs4.BeautifulSoup(proxies_source.encode(enc), 'html.parser')
   proxies_table= soup.find("table", {"class": "table table-striped table-bordered"})
   #proxies_table = soup.find(id='proxylisttable')
   for row in proxies_table.tbody.find_all('tr'):
        lip.append(row.find_all('td')[0].string)
        lport.append(row.find_all('td')[1].string)
        ltypeproxy.append(row.find_all('td')[4].string)
   df_proxies =pd.DataFrame({'Ip':lip
                    , 'Port':lport
                    , 'Type': ltypeproxy})                
   filter1 = df_proxies["Type"]=='elite proxy'
   df_elite_proxies = df_proxies[filter1]
   df_elite_proxies = df_elite_proxies.reset_index(drop=True)
   #return proxies
   return df_elite_proxies

def initDriver(ipprofile,portprofile):
   os.chdir(dirPath)
   if browser == 'F':
       profile = webdriver.FirefoxProfile() 
       profile.set_preference("network.proxy.type", 1)
       #Ir buscar mais ip e portas
       profile.set_preference("network.proxy.http", ipprofile)
       profile.set_preference("network.proxy.http_port", portprofile)
       profile.update_preferences() 
       driver = webdriver.Firefox(executable_path=fire_atual,firefox_profile=profile)
   elif browser == 'C':
       proxy = ipprofile + portprofile
       chrome_options = webdriver.ChromeOptions()
       chrome_options.add_argument('--proxy-server=%s' % proxy)
       driver = webdriver.Chrome(executable_path=chrome_atual,chrome_options=chrome_options)
   return driver



