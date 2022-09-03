# BILIOTECAS/PACOTES

import os
import logging
import requests
import pandas as pd
import numpy as np
import re
import numpy
import sqlite3

from datetime import datetime
from bs4 import BeautifulSoup 
from sqlalchemy import create_engine

# COLETA DE DADOS
def coleta_de_dados(url, headers):

    # html vitrine
    principal_page = requests.get(url, headers=headers)

    # objeto beautiful soup da vitrine
    principal_soup = BeautifulSoup(principal_page.text, 'html.parser')

    #========================================== DADOS DOS PRODUTOS ==================================================
    products = principal_soup.find( 'ul', class_='products-listing small')

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

    data = pd.DataFrame([product_id, product_category, product_name, product_price]).T
    data.columns = ['product_id', 'product_category', 'product_name', 'product_price']
    
    return data


# COLETA DE DADOS POR PRODUTO
def coleta_de_dados_por_produto(data, headers):

    # dataframe vazio
    df_compositions = pd.DataFrame()

    aux = []

    # colunas para comportar dados extraídos
    df_pattern = pd.DataFrame(columns= ['Art. No.','Composition','Fit','Product safety','Size'])

    for i in range(len(data)):

    # ---------------------------------------------- obtenção html do produto -----------------------------------------------

        # URL da página do produto
        url_ = 'https://www2.hm.com/en_us/productpage.' + data.loc[i, 'product_id'] + '.html'
        logger.debug('Product: %s', url_)

        # html da pagina do produto
        page = requests.get(url_, headers=headers)

        # objeto Beautiful Soup do html da pagina do produto
        soup = BeautifulSoup(page.text, 'html.parser')

    # ---------------------------------------------------------- color name -------------------------------------------------

        product_list = soup.find_all('a', class_='filter-option miniature active') + soup.find_all('a', class_='filter-option miniature')

        # Aqui realizamos a extração dos dados.
        color_name = [p.get('data-color') for p in product_list]

        # Aqui estamos realizando a extração do identificador de cada cor do produto
        product_id = [p.get('data-articlecode') for p in product_list]

        df_color = pd.DataFrame([product_id, color_name]).T
        df_color.columns = ['product_id', 'color_name']

        for j in range(0,len(df_color)):

             # URL da página do produto
            url_ = 'https://www2.hm.com/en_us/productpage.' + df_color.loc[j, 'product_id'] + '.html'
            logger.debug('Color: %s', url_)

            # html da pagina do produto
            page = requests.get(url_, headers=headers)

            # objeto Beautiful Soup do html da pagina do produto
            soup = BeautifulSoup(page.text, 'html.parser')


            # ---------------------------------- Product Name --------------------------------

            product_name = soup.find_all('hm-product-name', id='js-product-name')[0].find_all('h1')[0].get_text()

            # ---------------------------------- Product Price -------------------------------
            product_price = soup.find_all('div', class_='primary-row product-item-price')[0].find_all('span')[0].get_text().split()[0]
            #--------------------------------------------------- composition ------------------------------------------------

            # variável auxiliar para extrair os dados necessários do html
            auxiliar = soup.find_all('hm-product-description', id='js-product-description')

            # Aqui nós extraímos parte do html que tem os dados necessários.
            product_composition_list = [list(filter(None, p.get_text().split('\n'))) for p in auxiliar[0].find_all('div')]

            # Transformar os dados extraídos em um DataFrame e obter a transposta para ter as colunas necessárias.
            df_composition = pd.DataFrame(product_composition_list).T

            # Nomeação das colunas
            df_composition.columns = df_composition.iloc[0]

            # Eliminar a primeira linha.
            df_composition = df_composition.iloc[1:].fillna(method='ffill')

            df_composition['Composition'] = df_composition['Composition'].str.replace('Pocket lining:', '', regex = True)
            df_composition['Composition'] = df_composition['Composition'].str.replace('Shell:', '', regex = True)
            df_composition['Composition'] = df_composition['Composition'].str.replace('Pocket:', '', regex = True)
            df_composition['Composition'] = df_composition['Composition'].str.replace('Lining:', '', regex = True)

            # garantia do mesmo números de colunas
            df_composition = pd.concat([df_pattern, df_composition], axis=0)

            # renomeando as colunas
            df_composition.columns = ['product_id', 'composition', 'fit', 'product_safety', 'size']
            df_composition['product_name'] = product_name
            df_composition['product_price'] = product_price

            aux = aux + df_composition.columns.tolist()

            df_composition = pd.merge(df_composition, df_color, how='left', on='product_id')

            # criar um data_base de detalhes dos produtos
            df_compositions = pd.concat([df_compositions, df_composition], axis=0) 

    df_compositions['style_id'] = df_compositions['product_id'].apply(lambda x: x[:-3])
    df_compositions['color_id'] = df_compositions['product_id'].apply(lambda x: x[-3:])

    # scrapy datetime
    df_compositions['scrapy_datetime'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    return df_compositions


# LIMPEZA DE DADOS
def limpeza_de_dados(data_compositions):

    data = data_compositions

    # product name
    # Vamos padronizar os textos da coluna product name de acordo com a coluna product category deixando todos os caracteres 
    # minúsculo
    data['product_name'] = data['product_name'].apply( lambda x: x.replace( ' ' , '_' ).lower() )

    # product price
    # Aqui nós vamos remover o cifrão e devolver novamente para a variável.
    data['product_price'] = data['product_price'].apply(lambda x: x.replace('$', ''))
    data['product_price'] = data['product_price'].astype(float)


    # color name
    # Aqui nós também vamos padronizar. Vamos colocar underline nos espaços e colocar todas as letras em minúsculos.
    data['color_name'] = data['color_name'].apply(lambda x: x.replace(' ','_').lower())

    # fit
    # Aqui nós também vamos padronizar. Vamos colocar underline nos espaços e colocar todas as letras em minúsculos.
    data['fit'] = data['fit'].apply(lambda x:x.replace(' ', '_').lower())

    # size
    # Com essa coluna vamos extrair dois dados que vão compor as colunas size number and size model
    data['size_number'] = data['size'].apply(lambda x: re.search('(\d{3})cm', x).group(1) if pd.notnull(x) else x )
    data['size_number'] = data['size_number'].astype(float)

    data['size_model'] = data['size'].str.extract('(\d+/\\d+)')

    # A coluna Product safety não pe de nosso interesse nesse momento. Desta forma, removemos ela.
    data = data.drop(columns=['size', 'product_safety'], axis=1)

    # ===============================  composition ==========================

    # Nesse momento vamos organizar a Compositon. Para que isso ocorra, nós vamos quebrá-la com
    # as composições básicas da calças jeans. Antes disso, vamos verificar todos os
    # componentes das calças. 
    df1 = data['composition'].str.split(',', expand=True).reset_index(drop=True)

    # Uma vez visto do que as calças são compostas, vamos montar as nossas colunas.
    # cotton | spandex | Polyester 
    df_ref = pd.DataFrame(index = np.arange(len(data)), columns=['cotton', 'spandex', 'polyester'] )

    # ----------------------------composition--------------------------------

    # cotton

    df_cotton_0 = df1.loc[df1[0].str.contains('Cotton', na=True),0]
    df_cotton_0.name = 'cotton'

    df_cotton_1 = df1.loc[df1[1].str.contains('Cotton', na=True),1]
    df_cotton_1.name = 'cotton'

    df_cotton = df_cotton_0.combine_first(df_cotton_1)

    # logo após, fizemos a junção do df_ref com o df_cotton
    df_ref = pd.concat([df_ref, df_cotton], axis=1)
    # aqui, nós eliminamos a primeira coluna.
    df_ref = df_ref.loc[:, ~df_ref.columns.duplicated(keep='last') ]


    #------------------------------polyester-----------------------------------

    df_polyester_0 = df1.loc[df1[0].str.contains('Polyester', na=True),0]
    df_polyester_0.name = 'polyester'

    df_polyester_1 = df1.loc[df1[1].str.contains('Polyester', na=True),1]
    df_polyester_1.name = 'polyester'

    # combine
    df_polyester = df_polyester_0.combine_first(df_polyester_1)

    # concat
    df_ref = pd.concat([df_ref, df_polyester], axis=1)
    # aqui, nós eliminamos a primeira coluna.
    df_ref = df_ref.loc[:, ~df_ref.columns.duplicated(keep='last') ]
    df_ref['polyester'] = df_ref['polyester'].fillna('Polyester 0%')


    # -----------------------------spandex------------------------------

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


    # junção das combinações com o product_id
    df_aux = pd.concat([data['product_id'].reset_index(drop=True), df_ref], axis=1)

    # aqui nós vamos extrair somente o número das colunas cotton, polyeste e spandex.
    # Para isso, vamos usar a regex.
    df_aux['cotton']    = df_aux['cotton'].apply(lambda x:int(re.search('\d+', x).group(0))/100 if pd.notnull(x) else x ) 
    df_aux['polyester'] = df_aux['polyester'].apply(lambda x:int(re.search('\d+', x).group(0))/100 if pd.notnull(x) else x)
    df_aux['spandex']   = df_aux['spandex'].apply(lambda x:int(re.search('\d+', x).group(0))/100 if pd.notnull(x) else x)

    df_aux = df_aux.groupby('product_id').max().reset_index()

    # junção 
    data = pd.merge(data, df_aux, on='product_id', how='left')

    data = data.drop(columns=['composition'], axis=1)

    data = data.drop_duplicates().reset_index(drop=True)

    return data


# INSERÇÃO DOS DADOS NO BANCO DE DADOS
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

    # Conexão na tabela criada
    conn = create_engine('sqlite:///database_hm.sqlite', echo=False)

    data_insert.to_sql('vitrine', con=conn, if_exists='append', index=False)



if __name__ == '__main__':
    
    if not os.path.exists('logs'):
        os.makedirs('logs') 
        
    logging.basicConfig(filename = 'logs\webscraping_hm.txt',
                        level = logging.DEBUG, 
                        format = '%(asctime)s-%(levelname)s-%(name)s-%(message)s', 
                        datefmt='%Y-%m-%d %H:%M:%S')
    logger = logging.getLogger('webscraping_hm')
    
    
    # PARÂMETROS E CONSTANTES
    
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36 Edg/103.0.1264.37'}

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
        
        
        
        
        
        
        
        
        
        
        