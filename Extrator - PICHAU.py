from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
import csv

service = Service(executable_path=r'C:\Users\Gabriel - PC\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\LocalCache\local-packages\Python311\site-packages\seleniumbase\drivers\chromedriver.exe')
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)
url = 'https://www.pichau.com.br/computadores/pichau-gamer'
driver.get(url)

wait = WebDriverWait(driver, 15)
page_source = driver.page_source
# Agora você pode criar um objeto BeautifulSoup com o conteúdo da página
soup = BeautifulSoup(page_source, 'html.parser')

# Lista para armazenar os dados
dados = []

# Encontre todos os elementos com a classe "MuiCardContent-root"
produtos = soup.find_all('div', class_='MuiCardContent-root')

# Itere sobre os elementos e extraia a descrição, valor original, valor à vista e valor parcelado
for produto in produtos:
    descricao_element = produto.find('h2', class_='MuiTypography-h6')
    preco_original_element = produto.find('s')
    preco_a_vista_element = produto.find('div', class_='jss81')

    if descricao_element and preco_original_element and preco_a_vista_element:
        descricao = descricao_element.get_text(strip=True)
        preco_original = preco_original_element.get_text(strip=True)
        preco_a_vista = preco_a_vista_element.get_text(strip=True)

        # Encontre o elemento que contém o valor parcelado
        preco_parcelado_element = None
        for sibling in preco_a_vista_element.next_siblings:
            if "no PIX" in sibling.get_text(strip=True):
                preco_parcelado_element = sibling
                break

        if preco_parcelado_element:
            preco_parcelado = preco_parcelado_element.get_text(strip=True)
        else:
            preco_parcelado = ""

        dados.append([descricao, preco_original, preco_a_vista, preco_parcelado])

#paginas = list(range(2, int(Ultima_Pagina[4]) + 1))
#print(paginas)

paginas = [2, 3, 4]

for pg in paginas:
    service = Service(executable_path=r'C:\Users\Gabriel - PC\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\LocalCache\local-packages\Python311\site-packages\seleniumbase\drivers\chromedriver.exe')
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)
    url = f'https://www.pichau.com.br/computadores/pichau-gamer?page={pg}'
    driver.get(url)
    wait = WebDriverWait(driver, 40)
    pg_dados = driver.page_source

    # Agora você pode criar um objeto BeautifulSoup com o conteúdo da página
    soup = BeautifulSoup(pg_dados, 'html.parser')

    # Lista para armazenar os dados da página atual
    dados_paginação = []

    produtos = soup.find_all('div', class_='MuiCardContent-root')
    for produto in produtos:
        descricao_element = produto.find('h2', class_='MuiTypography-h6')
        preco_original_element = produto.find('s')
        preco_a_vista_element = produto.find('div', class_='jss81')

        if descricao_element and preco_original_element and preco_a_vista_element:
            descricao = descricao_element.get_text(strip=True)
            preco_original = preco_original_element.get_text(strip=True)
            preco_a_vista = preco_a_vista_element.get_text(strip=True)
            
            dados_paginação.append([descricao, preco_original, preco_a_vista])

    driver.quit()

    with open(f'produtos - {pg}.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter='|')
        writer.writerow(['Descrição', 'Valor Original', 'Valor à Vista'])
        writer.writerows(dados_paginação)

# Escreva os dados da primeira página em um arquivo CSV separado
with open('produtos.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file, delimiter='|')
    writer.writerow(['Descrição', 'Valor Original', 'Valor à Vista'])
    writer.writerows(dados)

print("Dados foram salvos em produtos.csv")
