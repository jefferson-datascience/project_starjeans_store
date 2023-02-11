# ================================================= BILIOTECAS E PACOTES =================================================================

import logging
import numpy  as np
import os
import pandas as pd
import re
import requests
import sqlite3

from bs4        import BeautifulSoup 
from datetime   import datetime
from sqlalchemy import create_engine


# ================================================ COLETA DE DADOS ======================================================================


def coleta_de_dados(url, headers):

    # Extração do HTML da vitrine
    principal_page = requests.get(url, headers=headers)

    # Instanciar o HTML da vitrine como Objeto Beautiful Soup
    principal_soup = BeautifulSoup(principal_page.text, 'html.parser')

    
    # ---------------------------------------------------- DADOS DOS PRODUTOS -----------------------------------------------------------
    
    # Acesso aos produtos
    products = principal_soup.find( 'ul', class_='products-listing small')

    # Listamos os produtos
    product_list = products.find_all( 'article', class_='hm-product-item' )

    # Extração dos id's do produto
    product_id = [ p.get( 'data-articlecode' ) for p in product_list ]

    # Extração da categoria do produto
    product_category = [p.get( 'data-category' ) for p in product_list]

    # Extração do nome do produto
    product_list = products.find_all('a', class_='link')
    product_name = [p.get_text() for p in product_list]

    # Extração dos preços
    product_list = products.find_all('span', class_='price regular')
    product_price=[p.get_text() for p in product_list]

    # Armazenamento das informações..
    data = pd.DataFrame([product_id, product_category, product_name, product_price]).T
    
    # Renomeando as colunas
    data.columns = ['product_id', 'product_category', 'product_name', 'product_price']
    
    # Retornando o DataFrame com a coleta dos dados
    return data


# ============================================== COLETA DAS CARACTERÍSTICAS DE CADA PRODUTO ==============================================


def coleta_de_dados_por_produto(data, headers):

    # Dataframe vazio
    df_compositions = pd.DataFrame()
    
    # Lista vazia auxiliar
    aux = []

    # colunas para comportar dados extraídos
    df_pattern = pd.DataFrame(columns= ['Art. No.','Composition','Fit','Product safety','Size'])

    for i in range(len(data)):

    # ---------------------------------------------- Obtenção do HTML do produto  --------------------------------------------------------

        # URL da página do produto
        url_ = 'https://www2.hm.com/en_us/productpage.' + data.loc[i, 'product_id'] + '.html'
        # Debbuger
        logger.debug('Product: %s', url_)

        # Extração do HTML da Página do Produto
        page = requests.get(url_, headers=headers)

        # Instaciar o HTML da Página do Produto como umobjeto Beautiful Soup
        soup = BeautifulSoup(page.text, 'html.parser')

    # ---------------------------------------------------------- Extração das Cores do Produto -------------------------------------------

        # Acesso as Cores do Produto
        product_list = soup.find_all('a', class_='filter-option miniature active') + soup.find_all('a', class_='filter-option miniature')

        # Extração das Cores
        color_name = [p.get('data-color') for p in product_list]

        # Extração do identificador de cada cor do produto
        product_id = [p.get('data-articlecode') for p in product_list]

        # Armazenamento das cores
        df_color = pd.DataFrame([product_id, color_name]).T
        
        # Renomear as colunas
        df_color.columns = ['product_id', 'color_name']

        for j in range(0,len(df_color)):

             # URL da página do produto de terminada cor
            url_ = 'https://www2.hm.com/en_us/productpage.' + df_color.loc[j, 'product_id'] + '.html'
            logger.debug('Color: %s', url_)

            # Extração da página do html do produto
            page = requests.get(url_, headers=headers)

            # INstanciar o html do produto com um Objeto Beautiful Soup
            soup = BeautifulSoup(page.text, 'html.parser')

            # Extração do nome
            product_name = soup.find_all('hm-product-name', id='js-product-name')[0].find_all('h1')[0].get_text()

            # Extração do Preço
            product_price = soup.find_all('div', class_='primary-row product-item-price')[0].find_all('span')[0].get_text().split()[0]
            
            
            # ------------------------- Extração da Composição das Matérias-Primas das Calçascomposition ---------------------------------

            
            # Extração do html que possui os dados necessários
            auxiliar = soup.find_all('hm-product-description', id='js-product-description')
            product_composition_list = [list(filter(None, p.get_text().split('\n'))) for p in auxiliar[0].find_all('div')]

            # Armazenamento dos Dados
            df_composition = pd.DataFrame(product_composition_list).T

            # Nomeação das Colunas
            df_composition.columns = df_composition.iloc[0]

            # Eliminar a primeira linha.
            df_composition = df_composition.iloc[1:].fillna(method='ffill')

            # Remoção de strings desnecessárias
            df_composition['Composition'] = df_composition['Composition'].str.replace('Pocket lining:', '', regex = True)
            df_composition['Composition'] = df_composition['Composition'].str.replace('Shell:', '', regex = True)
            df_composition['Composition'] = df_composition['Composition'].str.replace('Pocket:', '', regex = True)
            df_composition['Composition'] = df_composition['Composition'].str.replace('Lining:', '', regex = True)

            # Garantia do mesmo números de colunas
            df_composition = pd.concat([df_pattern, df_composition], axis=0)

            # renomeando as colunas
            df_composition.columns = ['product_id', 'composition', 'fit', 'product_safety', 'size']
            
            # Criando as colunas do product name e product price
            df_composition['product_name'] = product_name
            df_composition['product_price'] = product_price

            aux = aux + df_composition.columns.tolist()
            
            # Junção dos Dados com todas as características e informações de id.
            df_composition = pd.merge(df_composition, df_color, how='left', on='product_id')

            # criar um data_base de detalhes dos produtos
            df_compositions = pd.concat([df_compositions, df_composition], axis=0) 

    df_compositions['style_id'] = df_compositions['product_id'].apply(lambda x: x[:-3])
    df_compositions['color_id'] = df_compositions['product_id'].apply(lambda x: x[-3:])

    # Criação da coluna para informar a hora da extração dos dados 
    df_compositions['scrapy_datetime'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    return df_compositions


# ==================================================== LIMPEZA DE DADOS ==================================================================


def limpeza_de_dados(data_compositions):

    data = data_compositions

    # Padronização dos textos da coluna product name
    data['product_name'] = data['product_name'].apply( lambda x: x.replace( ' ' , '_' ).lower() )

    # Remoção do caracter '$' da coluna product price e mudança da natureza da variável.
    data['product_price'] = data['product_price'].apply(lambda x: x.replace('$', ''))
    data['product_price'] = data['product_price'].astype(float)

    # Padronização dos textos da coluna color name
    data['color_name'] = data['color_name'].apply(lambda x: x.replace(' ','_').lower())

    # Padronização dos textos da coluna fit
    data['fit'] = data['fit'].apply(lambda x:x.replace(' ', '_').lower())

    # Criação da coluna size_number a partir da extração das informações da coluna size e mudança da variável
    data['size_number'] = data['size'].apply(lambda x: re.search('(\d{3})cm', x).group(1) if pd.notnull(x) else x )
    data['size_number'] = data['size_number'].astype(float)

    # Criaçaõ da coluna size_model a partir da extração das informações dad coluna size
    data['size_model'] = data['size'].str.extract('(\d+/\\d+)')

    # Dropagem da coluna Product safety e Size
    data = data.drop(columns=['size', 'product_safety'], axis=1)

    
    # ===============================  Organização e Limpeza das Matérias-Primas =========================================================

    
    # Splitar os dados
    df1 = data['composition'].str.split(',', expand=True).reset_index(drop=True)

    # Montagem do DataFrame com as principais matéria-primas que compõem as calças.
    df_ref = pd.DataFrame(index = np.arange(len(data)), columns=['cotton', 'spandex', 'polyester'] )

    
    # ----------------------------------------- Matéria-Prima: Cotton -------------------------------------------------------------------
    
    
    df_cotton_0 = df1.loc[df1[0].str.contains('Cotton', na=True),0]
    df_cotton_0.name = 'cotton'

    df_cotton_1 = df1.loc[df1[1].str.contains('Cotton', na=True),1]
    df_cotton_1.name = 'cotton'

    df_cotton = df_cotton_0.combine_first(df_cotton_1)

    df_ref = pd.concat([df_ref, df_cotton], axis=1)
    
    df_ref = df_ref.loc[:, ~df_ref.columns.duplicated(keep='last') ]


    #--------------------------------------------- Matéria-Prima: Polyester --------------------------------------------------------------

    
    df_polyester_0 = df1.loc[df1[0].str.contains('Polyester', na=True),0]
    df_polyester_0.name = 'polyester'

    df_polyester_1 = df1.loc[df1[1].str.contains('Polyester', na=True),1]
    df_polyester_1.name = 'polyester'

    df_polyester = df_polyester_0.combine_first(df_polyester_1)

    df_ref = pd.concat([df_ref, df_polyester], axis=1)
    
    
    df_ref = df_ref.loc[:, ~df_ref.columns.duplicated(keep='last') ]
    df_ref['polyester'] = df_ref['polyester'].fillna('Polyester 0%')


    # ------------------------------------------------- Matéria-Prima: spandex -----------------------------------------------------------
    

    df_spandex_1 = df1.loc[df1[1].str.contains('Spandex', na=True),1]
    df_spandex_1.name = 'spandex'

    df_spandex_2 = df1.loc[df1[2].str.contains('Spandex', na=True),2]
    df_spandex_2.name = 'spandex'

    df_spandex = df_spandex_1.combine_first(df_spandex_2)

    # logo após, fizemos a junção do df_ref com o df_cotton
    df_ref = pd.concat([df_ref, df_spandex], axis=1)
    # aqui, nós eliminamos a primeira coluna.
    df_ref = df_ref.loc[:, ~df_ref.columns.duplicated(keep='last') ]
    df_ref['spandex'] = df_ref['spandex'].fillna('Spandex 0%')

    
    # ----------------------------------------------------------------------------------------------------------------------------------

    
    # junção das combinações com o product_id
    df_aux = pd.concat([data['product_id'].reset_index(drop=True), df_ref], axis=1)
    
    # Extração das POrcentagens de matéria prima sobre cada material.
    df_aux['cotton']    = df_aux['cotton'].apply(lambda x:int(re.search('\d+', x).group(0))/100 if pd.notnull(x) else x ) 
    df_aux['polyester'] = df_aux['polyester'].apply(lambda x:int(re.search('\d+', x).group(0))/100 if pd.notnull(x) else x)
    df_aux['spandex']   = df_aux['spandex'].apply(lambda x:int(re.search('\d+', x).group(0))/100 if pd.notnull(x) else x)

    # Agrupamento dos dados
    df_aux = df_aux.groupby('product_id').max().reset_index()

    # Merge do DataFrame Principal com o Dataframe das matérias primas.
    data = pd.merge(data, df_aux, on='product_id', how='left')

    # Dropagem da coluna
    data = data.drop(columns=['composition'], axis=1)

    # Dropagem das Colunas
    data = data.drop_duplicates().reset_index(drop=True)

    # Retorno do DataFrame
    return data


# ========================================= INSERÇÃO DOS DADOS NO BANCO DE DADOS =========================================================


def insercao_dos_dados(data):

    data_insert = data[['product_id', 
                        'style_id', 
                        'color_id', 
                        'product_name', 
                        'color_name', 
                        'fit', 
                        'product_price', 
                        'size_number', 
                        'size_model', 
                        'cotton', 
                        'polyester', 
                        'spandex', 
                        'scrapy_datetime']].copy()

    # Conexão criada com o banco de dados sqlite.
    conn = create_engine('sqlite:///database_hm.sqlite', echo=False)

    # Inserção dos dados
    data_insert.to_sql('vitrine', con=conn, if_exists='append', index=False)

    
# ----------------------------------------------------------------------------------------------------------------------------------------


# Inicializador
if __name__ == '__main__':
    
    # Arquivo de Log para monitoramento das extrações.
    if not os.path.exists('logs'):
        os.makedirs('logs') 
        
    logging.basicConfig(filename = 'logs\webscraping_hm.txt',
                        level = logging.DEBUG, 
                        format = '%(asctime)s-%(levelname)s-%(name)s-%(message)s', 
                        datefmt='%Y-%m-%d %H:%M:%S')
    logger = logging.getLogger('webscraping_hm')
    
    
    # PARÂMETROS E CONSTANTES
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36 Edg/103.0.1264.37'}

    # Url da Página da hm
    url = 'https://www2.hm.com/en_us/men/products/jeans.html'
    
    # COLETA DE DADOS
    data = coleta_de_dados(url, headers)
    logger.info('coleta de dados feita')
        
    # COLETA DE DADOS POR PRODUTO
    data_product = coleta_de_dados_por_produto(data, headers)
    logger.info('coleta de dados por produto feita')
    
    # LIMPEZA DE DADOS
    data_cleaning = limpeza_de_dados(data_product)
    logger.info('limpeza de dados feita')
    
    # INSERÇÃO DOS DADOS NO BANCO DE DADOS
    insercao_dos_dados(data_cleaning)
    logger.info('insercao de dados feita')
        
        
        
        
        
        
        
        
        
        
        