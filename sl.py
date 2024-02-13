from  selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

options = Options()
options.headless = False

MeuNavegador = webdriver.Chrome(options=options)

link = "https://ford-iap-kpmg.ws360.com.br/"

MeuNavegador.get(url=link)

esperar = time.sleep(4)

# Logando na tela de login

#inputar usuario
LoginUsuario = MeuNavegador.find_element(By.XPATH, '//*[@id="inputLogin"]')
LoginUsuario.send_keys('aferr136')

#inputar senha
LoginSenha = MeuNavegador.find_element(By.XPATH, '//*[@id="inputPassword"]')
LoginSenha.send_keys('ford123')

BotaoLogin = MeuNavegador.find_element(By.XPATH,'/html/body/div/div/form/input[1]')
BotaoLogin.click()

time.sleep(5)

# Ações na tela primeira de acesso

primeiro_botao = MeuNavegador.find_element(By.XPATH, '//*[@id="side-menu"]/li[3]/a/span[1]')
primeiro_botao.click()

time.sleep(2)

segundo_botao = MeuNavegador.find_element(By.XPATH, '//*[@id="side-menu"]/li[3]/ul/li/a')
segundo_botao.click()

time.sleep(3600)