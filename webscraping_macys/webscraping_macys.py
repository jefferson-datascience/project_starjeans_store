# ============================================= BIBLIOTECAS E PACOTES ====================================================================


import logging
import os
import pandas as pd
import requests
import re
import selenium
import sqlite3


from bs4                            import BeautifulSoup
from datetime                       import datetime
from selenium                       import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by   import By
from selenium.webdriver.support.ui  import Select
from sqlalchemy                     import create_engine
from time                           import sleep


# ============================================= COLETA DE DADOS ==========================================================================


def collect_data(url, headers):
    
    # Extração do html da página principal
    main_page = requests.get(url, headers=headers)

    # Intansciado a Extração do html da página principal como BeautifulSoup
    main_page_soup = BeautifulSoup(main_page.text, 'html.parser')

    # Extração dos links de cada produto e acomodação em uma lista com a url pronta.
    lista_html_produtos = main_page_soup.find_all('div', class_='productThumbnail redesignEnabled')
    lista_url_produtos = ['https://www.macys.com' + pagina_html.find('a')['href'] for pagina_html in lista_html_produtos]

    return lista_url_produtos


# ============================================== COLETA DE DADOS POR PRODUTO =============================================================


def collect_data_by_product(lista_url_produtos):

    # DataFrame que vai receber os dados
    df_pattern = pd.DataFrame(columns = ['product_id', 'product_name', 'price', 'color', 'size', 'details', 'scrapy_datetime'])

    # Bloco que vai realizar a coleta dos dados.
    for url in lista_url_produtos:

        # LIsta Vazia para Armazenar os dados
        product_details_list = list()

        # EDgeDriver do Selenium para navegar pela página.
        driver = webdriver.Edge()
        driver.get(url)
        sleep(2)
        num = len(driver.find_elements(By.CLASS_NAME, 'swatch-webp'))

        if num > 0:

            for i in range(num):

                elem = driver.find_elements(By.CLASS_NAME, 'swatch-webp')
                elem[i].click()

                # Extração do html atual
                page = driver.page_source
                product_page = BeautifulSoup(page, 'html.parser')

                # Extração dos tamanhos
                size_list_html = product_page.find('div', class_='collapsable cell').find_all('li', class_='swatch-itm cell selection-tile static')
                size_list = [size_html.find('span').get_text().split()[0] for size_html in size_list_html]

                for size in size_list:

                    product_details = list()

                    # Extração do Product_id
                    product_id = product_page.find('p', class_='c-small-font web-id c-margin-top-3v').get_text()
                    product_details.append(product_id)

                    # Extração do Product_name
                    product_name = product_page.find('div', class_='h3').get_text().split('\n')[1]
                    product_details.append(product_name)

                    # Extração do product price
                    price_html = product_page.find_all('div', class_='lowest-sale-price')[0]
                    price = price_html.find('span').get_text().split()[1]
                    product_details.append(price)

                    # Extração do color and color_id
                    color_html = product_page.find('div', class_='color-label-container c-uppercase')
                    color = color_html.find('span').get_text()
                    product_details.append(color)

                    # Extração do size
                    product_details.append(size)

                    # Extração do product_details
                    details = product_page.find('span', class_='processed-details').get_text().split('\n')
                    product_details.append(details)

                    # Extração do scrapy datetime
                    scrapy_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    product_details.append(scrapy_datetime)

                    # Apeend da lista de detalhes do produto
                    product_details_list.append(product_details[:])


            df_product = pd.DataFrame(product_details_list)
            df_product.columns = ['product_id', 'product_name', 'price', 'color', 'size', 'details', 'scrapy_datetime']
            df_pattern = pd.concat([df_pattern, df_product])
            logger.debug('Product URL: %s', url)

        else:

            # Extração do html atual
            page = driver.page_source
            product_page = BeautifulSoup(page, 'html.parser')

            # Extração dos tamanhos
            if product_page.find('div', class_='collapsable cell') is not None:

                size_list_html = product_page.find('div', class_='collapsable cell').find_all('li', class_='swatch-itm cell selection-tile static')
                size_list = [size_html.find('span').get_text().split()[0] for size_html in size_list_html]

                for size in size_list:

                    product_details = list()

                    #product_id
                    product_id = product_page.find('p', class_='c-small-font web-id c-margin-top-3v').get_text()
                    product_details.append(product_id)

                    # product_name
                    product_name = product_page.find('div', class_='h3').get_text().split('\n')[1]
                    product_details.append(product_name)

                    # price
                    price_html = product_page.find_all('div', class_='lowest-sale-price')[0]
                    price = price_html.find('span').get_text().split()[1]
                    product_details.append(price)

                    # color and color_id
                    color_html = product_page.find('div', class_='color-label-container c-uppercase')
                    if color_html is None:
                        color = None
                        product_details.append(color)
                    else:
                        color = color_html.find('span').get_text()
                        product_details.append(color)

                    # size
                    product_details.append(size)

                    # details
                    details = product_page.find('span', class_='processed-details').get_text().split('\n')
                    product_details.append(details)

                    # scrapy datetime
                    scrapy_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    product_details.append(scrapy_datetime)

                    # construction of product details list
                    product_details_list.append(product_details[:])

                df_product = pd.DataFrame(product_details_list)
                df_product.columns = ['product_id', 'product_name', 'price', 'color', 'size', 'details', 'scrapy_datetime']
                df_pattern = pd.concat([df_pattern, df_product])
                logger.debug('Product URL: %s', url)
        driver.close()

    df_pattern =  df_pattern.reset_index(drop=True)
    return df_pattern
    

# ================================================= LIMPEZA DE DADOS =====================================================================


def data_clean(df_pattern):

    # Removendo espaços vazios das células da coluna 'details' que são compostas por lista.
    for i in range(len(df_pattern['details'])):
        auxiliar_list=[]
        for element in df_pattern['details'].iloc[i]:
            if element.strip():
                auxiliar_list.append(element)
        df_pattern['details'].iloc[i] = auxiliar_list 

    # Criação da coluna fit e separação do fit da calça jeans do details.    
    df_pattern['fit'] = ''

    for j in range(len(df_pattern['details'])):
        for element in df_pattern['details'].iloc[j]:
            if len(element) < 59 and 'fit' in element:
                df_pattern['fit'].iloc[j] = element

    # Criação da coluna composition e separação das composições do details            
    df_pattern['composition'] = ''

    for j in range(len(df_pattern['details'])):
        for element in df_pattern['details'].iloc[j]:
            if 'cotton' in element or 'Cotton' in element:
                df_pattern['composition'].iloc[j] = element.lower()     

    # composição cotton
    df_pattern['cotton'] = ''
    df_pattern['cotton'] = df_pattern['composition'].apply(lambda x: 'yes' if 'cotton' in x else 'no')

    # composição polyester
    df_pattern['polyester'] = ''
    df_pattern['polyester'] = df_pattern['composition'].apply(lambda x: 'yes' if 'polyester' in x else 'no')

    # composição spandex
    df_pattern['spandex'] = ''
    df_pattern['spandex'] = df_pattern['composition'].apply(lambda x: 'yes' if 'spandex' in x else 'no')

    # composição elastane
    df_pattern['elastane'] = ''
    df_pattern['elastane'] = df_pattern['composition'].apply(lambda x: 'yes' if 'elastane' in x else 'no')

    # composição lyocell
    df_pattern['lyocell'] = ''
    df_pattern['lyocell'] = df_pattern['composition'].apply(lambda x: 'yes' if 'lyocell' in x else 'no')

    # composição viscose
    df_pattern['viscose'] = ''
    df_pattern['viscose'] = df_pattern['composition'].apply(lambda x: 'yes' if 'viscose' in x else 'no')
    
    # remoção dos na's
    df_pattern = df_pattern.dropna().reset_index(drop=True)

    # limpeza da coluna product_id
    df_pattern['product_id'] = df_pattern['product_id'].apply(lambda x: re.search('\d+', x).group())
    
    # limpeza da coluna product_name
    df_pattern['product_name'] = df_pattern['product_name'].apply(lambda x: x.lower())
    df_pattern['product_name'] = df_pattern['product_name'].apply(lambda x: x.strip())
    
    # limpeza da coluna color
    df_pattern['color'] = df_pattern['color'].apply(lambda x: x.lower())
    df_pattern['color'] = df_pattern['color'].apply(lambda x: x.strip())
    df_pattern['color'] = df_pattern['color'].apply(lambda x: x.replace(' ', '_'))
    
    # limpeza da coluna fit
    df_pattern['fit'] = df_pattern['fit'].apply(lambda x: x.lower())
    df_pattern['fit'] = df_pattern['fit'].apply(lambda x: 'regular_fit' if bool(re.search('regular', x)) else x)
    df_pattern['fit'] = df_pattern['fit'].apply(lambda x: 'slim_fit' if bool(re.search('slim', x)) else x)
    df_pattern['fit'] = df_pattern['fit'].apply(lambda x: 'relaxed_fit' if bool(re.search('relaxed', x)) else x)
    df_pattern['fit'] = df_pattern['fit'].apply(lambda x: 'skinny_fit' if bool(re.search('skinny', x)) else x)
    
    # Mudança de Variável para float
    df_pattern['price'] = df_pattern['price'].astype(float)

    
    # remoção de colunas 
    df_pattern.drop(columns =['details', 'composition'])

    # reorganização das colunas
    df_final = df_pattern[['product_id', 
                         'product_name', 
                         'price', 'color', 
                         'fit', 
                         'size', 
                         'cotton', 
                         'polyester', 
                         'spandex', 
                         'elastane', 
                         'lyocell', 
                         'viscose',
                         'scrapy_datetime']].copy()
    
    # Retorno do DataFrame
    return df_final


# ============================================== INSERÇÃO DOS DADOS NO BANCO DE DADOS=====================================================


def upload_database(df_clean):

    # Conexão com os Dados
    conexao = create_engine('sqlite:///database_macys.sqlite', echo=False)

    # upload dos dados
    df_clean.to_sql('vitrine', con = conexao, if_exists = 'append', index=False)

    
#-----------------------------------------------------------------------------------------------------------------------------------------


# Inicializador
if __name__ == '__main__':
    
    # ARQUIVO DE LOGGS
    
    if not os.path.exists('logs'):
        os.makedirs('logs') 

    logging.basicConfig(filename = 'logs\webscraping_macys.txt',
                            level = logging.DEBUG, 
                            format = '%(asctime)s-%(levelname)s-%(name)s-%(message)s', 
                            datefmt='%Y-%m-%d %H:%M:%S')
    logger = logging.getLogger('webscraping_macys')
    
    
    # PARÂMETROS E CONSTANTES
    
        # Parâmetro para realizar uma requisão na API
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36 Edg/103.0.1264.37'}

    # url da página principal
    url = 'https://www.macys.com/shop/mens-clothing/mens-jeans?id=11221&cm_sp=intl_hdr-_-men-_-11221_jeans_COL1%7D'
    
    # COLETA DE DADOS
    lista_urls = collect_data(url, headers)
    logger.info('Coleta de Dados Concluida')
    
    # COLETA DE DADOS POR PRODUTO
    dataframe_product = collect_data_by_product(lista_urls)
    logger.info('Coleta de Dados por Produto Concluida')
    
    # LIMPEZA DE DADOS
    dataframe_clean = data_clean(dataframe_product)
    logger.info('Limpeza de dados concluída')
    
    # INSERÇÃO DOS DADOS NO BANCO DE DADOS
    upload_database(dataframe_clean)
    logger.info('Inserção de Dados Concluída')
    
    