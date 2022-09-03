import streamlit as st
import pandas as pd
import numpy as np


dataframe_macys = pd.read_csv('vitrine_macys.csv')
dataframe_hm = pd.read_csv('vitrine_hm.csv')


def dataframe_metrics_hm(dataframe_hm):
    # METRICAS HM

    # MAX
    maximo_hm = dataframe_hm[['fit', 'product_price']].groupby('fit').max().reset_index()

    columns_name_max = maximo_hm['fit'].tolist()

    # reorganização para obter o dataframe max
    maximo_hm.columns = ['fit', 'max']
    maximo_hm = maximo_hm.T
    maximo_hm.columns = columns_name_max

    # drop da linha desnecessária
    maximo_hm = maximo_hm.iloc[1:].fillna(method='ffill')

    # MIN
    minimo_hm = dataframe_hm[['fit', 'product_price']].groupby('fit').min().reset_index()

    columns_name_min = minimo_hm['fit'].tolist()

    # reorganização para obter o dataframe min
    minimo_hm.columns = ['fit', 'min']
    minimo_hm = minimo_hm.T
    minimo_hm.columns = columns_name_min

    # drop na linha desnecessária
    minimo_hm = minimo_hm.iloc[1:].fillna('ffill')

    # MEDIA
    media_hm = dataframe_hm[['fit', 'product_price']].groupby('fit').mean().reset_index()

    columns_name_media = media_hm['fit'].tolist()

    # reorganização para obter o dataframe media
    media_hm.columns = ['fit', 'mean']
    media_hm = media_hm.T
    media_hm.columns = columns_name_media

    # drop das linhas desnecessárias
    media_hm = media_hm.iloc[1:].fillna(method='ffill')

    # MEDIANA
    mediana_hm = dataframe_hm[['fit', 'product_price']].groupby('fit').median().reset_index()

    columns_name_mediana = mediana_hm['fit'].tolist()

    # reorganização para obter o dataframe mediana
    mediana_hm.columns = ['fit', 'median']
    mediana_hm = mediana_hm.T
    mediana_hm.columns = columns_name_mediana

    # drop nas linhas desnecessárias
    mediana_hm = mediana_hm.iloc[1:].fillna(method='ffill')

    # SKEWNESS
    # Construção da tabela skewness
    skewness_hm = dataframe_hm[['fit', 'product_price']].groupby('fit').skew().reset_index()

    columns_name_skewness = skewness_hm['fit'].tolist()

    # reorganização para obter o dataframe skewness
    skewness_hm.columns = ['fit', 'skewness']
    skewness_hm = skewness_hm.T
    skewness_hm.columns = columns_name_skewness

    # drop de linha desnecessária
    skewness_hm = skewness_hm.iloc[1:].fillna(method='ffill')

    # Métricas
    metricas_hm = pd.concat([maximo_hm, minimo_hm, media_hm, mediana_hm, skewness_hm], axis=0).T

    return metricas_hm


def metrics_dataframe_macys(dataframe_macys):
    # METRICAS MACYS

    # MAX
    maximo_macys = dataframe_macys[['fit', 'price']].groupby('fit').max().reset_index()

    columns_name_max = maximo_macys['fit'].tolist()

    # reorganização para obter o dataframe max
    maximo_macys.columns = ['fit', 'max']
    maximo_macys = maximo_macys.T
    maximo_macys.columns = columns_name_max

    # drop da linha desnecessária
    maximo_macys = maximo_macys.iloc[1:].fillna(method='ffill')

    # MIN
    minimo_macys = dataframe_macys[['fit', 'price']].groupby('fit').min().reset_index()

    columns_name_min = minimo_macys['fit'].tolist()

    # reorganização para obter o dataframe min
    minimo_macys.columns = ['fit', 'min']
    minimo_macys = minimo_macys.T
    minimo_macys.columns = columns_name_min

    # drop na linha desnecessária
    minimo_macys = minimo_macys.iloc[1:].fillna('ffill')

    # MEDIA
    media_macys = dataframe_macys[['fit', 'price']].groupby('fit').mean().reset_index()

    columns_name_media = media_macys['fit'].tolist()

    # reorganização para obter o dataframe media
    media_macys.columns = ['fit', 'mean']
    media_macys = media_macys.T
    media_macys.columns = columns_name_media

    # drop das linhas desnecessárias
    media_macys = media_macys.iloc[1:].fillna(method='ffill')

    # MEDIANA
    mediana_macys = dataframe_macys[['fit', 'price']].groupby('fit').median().reset_index()

    columns_name_mediana = mediana_macys['fit'].tolist()

    # reorganização para obter o dataframe mediana
    mediana_macys.columns = ['fit', 'median']
    mediana_macys = mediana_macys.T
    mediana_macys.columns = columns_name_mediana

    # drop nas linhas desnecessárias
    mediana_macys = mediana_macys.iloc[1:].fillna(method='ffill')

    # SKEWNESS
    # Construção da tabela skewness
    skewness_macys = dataframe_macys[['fit', 'price']].groupby('fit').skew().reset_index()

    columns_name_skewness = skewness_macys['fit'].tolist()

    # reorganização para obter o dataframe skewness
    skewness_macys.columns = ['fit', 'skewness']
    skewness_macys = skewness_macys.T
    skewness_macys.columns = columns_name_skewness

    # drop de linha desnecessária
    skewness_macys = skewness_macys.iloc[1:].fillna(method='ffill')

    # Métricas
    metricas_macys = pd.concat([maximo_macys, minimo_macys, media_macys, mediana_macys, skewness_macys], axis=0).T
    return metricas_macys


# side bar

with st.sidebar:
    st.image('logo_apresentacao.png')
    page = st.selectbox("Navegue pelo Projeto", ["Apresentação",
                                                 "Vitrine H&M",
                                                 "Vitrine Macys",
                                                 "Respondendo as Perguntas do CEO"])

if page == 'Apresentação':

    st.image('imagem_fundo_apresentacao.png')

    #  Apresentação
    st.title('StarJeans! Store')

    st.subheader('Questão de Negócio')
    st.write('Eduardo e Marcelo são dois brasileiros, amigos e sócios de empreendimento. Depois de vários '
             'negócios bem sucedidos, eles estão planejando se lançar no mercado de moda dos USA como um '
             'modelo de negócio do tipo E-commerce. A idéia inicial é entrar no mercado com apenas um produto e para '
             'um público específico, no caso, o produto seria calças Jeans para o público masculino. O objetivo é '
             'manter o custo de operação baixo e escalar a medida que forem conseguindo clientes. Porém, mesmo com o '
             'produto de entrada e a audiência definidos, os dois sócios não tem experiência nesse mercado de moda e, '
             'portanto, não sabem definir coisas básicas como preço, o tipo de calça e o material para a fabricação de '
             'cada peça. Assim, os dois sócios contrataram uma consultoria de um Cientista de Dados para responder as '
             'seguintes perguntas: ')
    st.write('1. Qual o melhor preço de venda para as calças?\n')
    st.write('2. Quantos tipos de calças e suas cores para o produto inicial?\n')
    st.write('3. Quais as matérias-prima necessárias para confeccionar as calças?')

    st.write('As principais concorrentes da empresa Start Jeans! são as americanas H&M e Macys.')

    st.subheader('Premissas de Negócio')
    st.write('- Assumimos as matérias-primas de composição das calças Jeans que são mais frequentes em relação a cada '
             'concorrente.')

    st.markdown('Em relação aos produtos da concorrente H&M: ')
    st.write('- Desconsideramos as matérias-primas dos bolsos e dos forros dos bolsos '
             'das calças Jeans.\n'
             '- Sobre as matérias-primas das calças, será extraído a composição e informado a porcentagem de cada '
             'material na constituição de cada produto, sendo que será considerado a maior porcentagem da matéria-prima'
             ' na composição do produto.')
    st.markdown('Em relação aos produtos da Macys: ')
    st.write('- Será extraído a composição e informado se o produto possui determinada matéria-prima.')

    st.subheader('Estratégia de Resolução')

    st.write('1. Reconhecimento da estrutura das informações dos produtos do WebSite de calças Jeans masculina da '
             'Macys e da H&M')

    with st.expander('Link dos Websites', expanded=False):
        st.write('- Site da H&M: https://www2.hm.com/en_us/men/products/jeans.html')
        st.write('- Site da Macys: https://www.macys.com/shop/mens-clothing/mens-jeans?id=11221&edge=hybrid')

    st.write('2. Entendimento do negócio.')
    st.write('3. Coleta dos dados de cada produto do site da H&M.')
    st.write('4. Coleta dos dados de cada produto do site da MACYS.')
    st.write('5. Limpeza e tratamento dos dados coletados.')
    st.write('6. Análise Exploratória dos Dados.')
    st.write("7. Respondendo as perguntas dos CEO's.")

    st.subheader('Ferramentas Utilizadas')

    with st.expander('Análise exploratória/Manipulação dos Dados/Construção dos Códigos', expanded=True):
        st.write('- Jupyter Notebook')
        st.write('- Python 3.9.0')
        st.write('- PyCharm')

    with st.expander('Extração de dados dos sites', expanded=True):
        st.write('- Selenium')
        st.write('- Beautiful Soup')

    with st.expander('Visualização de Dados', expanded=True):
        st.write('Streamlit')

    with st.expander('Hospedagem de App/Armazenamento de Código', expanded=True):
        st.write('Heroku')
        st.write('GitHub')

    st.subheader('Conclusão')
    st.write('O projeto foi concluído com sucesso e todos os objetivos foram atingidos. Uma vez entregado o projeto, '
             'um ótimo projeto futuro seria sobre das questões das entregas desses produtos aos clientes. '
             'As ferramentas de '
             'extração de dados Beautiful Soup + Selenium seriam muito bem aplicadas para se investigar sobre prazos '
             'de entregas, preços de fretes e logística para variadas regiões do estado americano, dessa forma, '
             'ajudando na tomada de decisões de negócios dos CEO´s da StarJeans! e com isso gerando insights '
             'relevantes para a empresa.')

elif page == 'Vitrine H&M':

    st.image('logo_hm.png')

    # Dados extraídos H&M
    metrics_hm = dataframe_metrics_hm(dataframe_hm)

    st.title('Vitrine de Produtos H&M')

    st.write('Logo abaixo, temos a vitrine dos produtos do site da H&M com seus detalhes armazenado em um DataFrame. '
             'Nesse DataFrame possuímos informações como nome das calças, modelo, tamanhos disponíveis, preço, cores e '
             'composição.')

    filter_columns_hm = st.multiselect('Selecione as colunas a serem visualizadas: ', dataframe_hm.columns.tolist())
    filter_jeans_hm = st.multiselect('Selecione os modelos de jeans: ', dataframe_hm['fit'].unique().tolist())

    if filter_jeans_hm:
        df_hm = dataframe_hm[dataframe_hm['fit'].isin(filter_jeans_hm)]
        if filter_columns_hm:
            st.dataframe(df_hm[filter_columns_hm])
        else:
            st.dataframe(df_hm)
    else:
        if filter_columns_hm:
            st.dataframe(dataframe_hm[filter_columns_hm])
        else:
            st.dataframe(dataframe_hm)

    st.write('Além disso, temos algumas métricas relevantes em relação aos modelos das calças jeans e seus preços.')

    filter_metrics_hm = st.multiselect('Selecione as métricas a serem visuzalizadas: ', metrics_hm.columns)

    if filter_metrics_hm:
        st.dataframe(metrics_hm[filter_metrics_hm])
    else:
        st.dataframe(metrics_hm)

    st.write('Logo abaixo temos os gráficos representando as métricas:')

    col3, col4 = st.columns(2)

    with col3:
        st.image('image_max_hm.png')
    with col4:
        st.image('image_min_hm.png')

    col5, col6 = st.columns(2)

    with col5:
        st.image('image_mean_hm.png')
    with col6:
        st.image('image_median_hm.png')


elif page == 'Vitrine Macys':

    st.image('logo_macys.png')
    # Dados extraídos Macys
    metrics_macys = metrics_dataframe_macys(dataframe_macys)

    st.title('Vitrine de Produtos Macys')

    st.write('Logo abaixo, temos a vitrine dos produtos do site da H&M com seus detalhes armazenado em um DataFrame. '
             'Nesse DataFrame possuímos informações como nome das calças, modelo, tamanhos disponíveis, preço, cores e '
             'composição.')

    filter_columns_macys = st.multiselect('Selecione as colunas a serem visualizadas: ',
                                          dataframe_macys.columns.tolist())
    filter_jeans_macys = st.multiselect('Selecione os modelos de jeans: ', dataframe_macys['fit'].unique().tolist())

    if filter_jeans_macys:
        df_macys = dataframe_macys[dataframe_macys['fit'].isin(filter_jeans_macys)]
        if filter_columns_macys:
            st.dataframe(df_macys[filter_columns_macys])
        else:
            st.dataframe(df_macys)
    else:
        if filter_columns_macys:
            st.dataframe(dataframe_macys[filter_columns_macys])
        else:
            st.dataframe(dataframe_macys)

    st.write('Além disso, temos algumas métricas relevantes em relação aos modelos das calças jeans e seus preços.')

    filter_metrics_macys = st.multiselect('Selecione as métricas a serem visuzalizadas: ', metrics_macys.columns)

    if filter_metrics_macys:
        st.dataframe(metrics_macys[filter_metrics_macys])
    else:
        st.dataframe(metrics_macys)

    st.write('Segue abaixo os gráficos representando as métricas.')

    col7, col8 = st.columns(2)

    with col7:
        st.image('image_max_macys.png')
    with col8:
        st.image('image_min_macys.png')

    col9, col10 = st.columns(2)

    with col9:
        st.image('image_mean_macys.png')
    with col10:
        st.image('image_median_macys.png')


elif page == "Respondendo as Perguntas do CEO":

    st.image('imagem_fundo_apresentacao.png')

    st.title('Respondendo as Perguntas do CEO')

    st.subheader('1. Qual o melhor preço de venda para as calças?')
    st.write('Vamos fornecer para os CEO´s da empresa o preço máximo, mínimo, média e mediana dos preços das calças '
             'jeans sobre cada modelo de cada concorrente.')

    metrics_macys = metrics_dataframe_macys(dataframe_macys)
    metrics_hm = dataframe_metrics_hm(dataframe_hm)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader('Preços H&M')
        st.dataframe(metrics_hm[['max', 'min', 'median', 'mean']])

    with col2:
        st.subheader('Preços Macys')
        st.dataframe(metrics_macys[['max', 'min', 'median', 'mean']])

    st.subheader('2. Quantos tipos de calças e suas cores para o produto inicial?')

    col3, col4 = st.columns(2)

    with col3:
        vitrine_cores_hm = dataframe_hm[['product_name', 'color_name']]
        st.subheader('Catalogo H&M')
        st.write('Na tabela abaixo podemos ver as calças e cores.')
        st.dataframe(vitrine_cores_hm)

    with col4:
        vitrine_cores_macys = dataframe_macys[['product_name', 'color', 'size']].copy()
        st.subheader('Catálogo Macys')
        st.write('Logo abaixo, podemos ver as calças, as cores e tamanhos.')

        st.dataframe(vitrine_cores_macys)

    st.subheader('3. Quais as matérias prima necessárias para confeccionar as calças?')

    st.subheader('Vitrine de Composição H&M')
    st.write('As principais matérias-primas das calças jeans da H&M são algodão, polyester e spandex. Logo abaixo,'
             'podemos ver as calças jeans e suas composições e a porcentagem usadas nas calças.')
    vitrine_composicoes_hm = dataframe_hm.drop_duplicates(subset=['product_name']).reset_index(drop=True)
    st.dataframe(vitrine_composicoes_hm[['product_name', 'fit', 'cotton', 'polyester', 'spandex']])

    st.subheader('Vitrine de Composições Macys')
    st.write('As principais materias-primas usadas nas calças jeans da Macys são algodão, polyester, spandex, '
             'elastano, lyocell e viscose. Na tabela abaixo, podemos ver as calças e de quais matérias-primas elas '
             'são constituídas.')
    vitrine_composicoes_macys = dataframe_macys.drop_duplicates(subset=['product_name']).reset_index(drop=True)
    st.dataframe(vitrine_composicoes_macys[['product_name',
                                            'fit',
                                            'cotton',
                                            'polyester',
                                            'spandex',
                                            'elastane',
                                            'lyocell',
                                            'viscose']])
