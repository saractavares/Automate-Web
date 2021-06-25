#!/usr/bin/env python
# coding: utf-8

# # Automação Web e Busca de Informações com Python
# 
# #### Desafio: 
# 
# Trabalhamos em uma importadora e o preço dos nossos produtos é vinculado a cotação de:
# - Dólar
# - Euro
# - Ouro
# 
# Precisamos pegar na internet, de forma automática, a cotação desses 3 itens e saber quanto devemos cobrar pelos nossos produtos, considerando uma margem de contribuição que temos na nossa base de dados.
# 
# Base de Dados: https://drive.google.com/drive/folders/1o2lpxoi9heyQV1hIlsHXWSfDkBPtze-V?usp=sharing
# 
# Para isso, vamos criar uma automação web:
# 
# - Usaremos o selenium
# - Importante: baixar o webdriver

# In[68]:


from selenium import webdriver
from selenium.webdriver.common.keys import Keys


#abrir navegador
nav = webdriver.Chrome(executable_path='C:/Users/Samsung/chromedriver.exe')
nav.get('https://www.google.com/')

nav.find_element_by_xpath('/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys('cotação dólar agora')
nav.find_element_by_xpath('/html/body/div[1]/div[3]/form/div[1]/div[1]/div[3]/center/input[1]').send_keys(Keys.ENTER)

dolar = nav.find_element_by_xpath('//*[@id="knowledge-currency__updatable-data-column"]/div[1]/div[2]/span[1]').get_attribute('data-value')
print(dolar)

nav.get('https://www.google.com/')

nav.find_element_by_xpath('/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys('cotação euro agora')
nav.find_element_by_xpath('/html/body/div[1]/div[3]/form/div[1]/div[1]/div[3]/center/input[1]').send_keys(Keys.ENTER)

euro = nav.find_element_by_xpath('//*[@id="knowledge-currency__updatable-data-column"]/div[1]/div[2]/span[1]').get_attribute('data-value')
print(euro)

nav.get('https://www.melhorcambio.com/ouro-hoje#:~:text=O%20valor%20do%20grama%20do,em%20R%24%20280%2C60.')

ouro = nav.find_element_by_xpath('//*[@id="comercial"]').get_attribute('value')
ouro = ouro.replace(',','.')
print(ouro)
nav.quit()


# ### Agora vamos atualiza a nossa base de preços com as novas cotações

# - Importando a base de dados

# In[69]:


import pandas as pd

tb = pd.read_excel(r'C:\Users\Samsung\Downloads\Produtos.xlsx')
display(tb)


# - Atualizando os preços e o cálculo do Preço Final

# In[70]:


tb.loc[tb["Moeda"] == "Dólar", "Cotação"] = float(dolar)
tb.loc[tb["Moeda"] == "Euro", "Cotação"] = float(euro)
tb.loc[tb["Moeda"] == "Ouro", "Cotação"] = float(ouro)

tb["Preço Base Reais"] = tb["Preço Base Original"] * tb["Cotação"]

tb["Preço Final"] = tb["Preço Base Reais"] * tb["Margem"]

display(tb)


# ### Agora vamos exportar a nova base de preços atualizada

# In[71]:


tb.to_excel("Produtos Novo1.xlsx", index=False)

