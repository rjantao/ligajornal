import Param
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from   time import sleep
pagEquipas = 'http://liga.record.pt/gerir-equipas/default.aspx'
pagLogin= 'https://aminhaconta.xl.pt/Login?returnUrl=http%3A%2F%2Fliga.record.pt%2F'




#https://liga.record.pt/gerir-equipas/jogar.aspx?id_team=62823&id_round=1

def loginLigaRecord(driver,iparams):
   usernameval  = iparams['username']
   passwordval  = iparams['password']
   paginalogin  = iparams['paginalogin']
   driver.get(paginalogin)
   driver.find_element_by_id('email').clear()
   username =  driver.find_element_by_id('email')
   username.send_keys(usernameval)
   driver.find_element_by_id('password').click()
   password =  driver.find_element_by_id('password')
   password.send_keys(passwordval)
   driver.find_element_by_id('loginBtn').click()
   sleep(5)
   gerirequipas = iparams['gerirequipas']
   driver.get(gerirequipas)
   sleep(5)


if __name__ == "__main__":
  try:
   params  = Param.config(Param.configFile, 'ligarecord')
   browse  = Param.runDriverProxy(0)
   loginLigaRecord(browse,params)
  except KeyboardInterrupt:
     print('\n')








