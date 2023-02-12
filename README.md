# Consultoria de Ciência de Dados para StarJeans! Store


O objetivo do projeto é realizar uma consultoria de para a empresa StarJeans! Store com o objetivo de ajudar na tomada de decisão sobre qual preço estipular, sobre qual modelo de calça fabricar e quais matéria-primas utilizar, baseado nas informações extraídas da concorrência por meio de scripts Python.

## PROBLEMA DE NEGÓCIO

Eduardo e Marcelo são dois brasileiros, amigos e sócios de empreendimento. Depois de vários negócios bem sucedidos, eles estão planejando se lançar no mercado de moda dos USA como um modelo de negócio do tipo E-commerce. A idéia inicial é entrar no mercado com apenas um produto e para um público específico, no caso, o produto seria calças Jeans para o público masculino. O objetivo é manter o custo de operação baixo e escalar a medida que forem conseguindo clientes. 

Porém, mesmo com o produto de entrada e a audiência definidos, os dois sócios não tem experiência nesse mercado de moda e, portanto, não sabem definir coisas básicas como preço, o tipo de calça e o material para a fabricação de cada peça. Assim, os dois sócios contrataram uma consultoria de um Cientista de Dados(no caso, eu) para ajudar nessa empreitada.

## QUESTÃO DE NEGÓCIO

Nessa consultoria, os CEOs esperam que eu responda as seguintes questões de negócio:

**1.** Qual o melhor preço de venda para as calças?

**2.** Quantos tipos de calças e suas cores para o produto inicial?

**3.** Quais as matérias-prima necessárias para confeccionar as calças?

Além dessas questões, foi nos informado que as principais concorrentes da empresa Start Jeans! serão as americanas H&M e Macys.

### Planejamento de Solução

**Qual a solução desse problema?** Com a informação de que as principais concorrentes da StarJeans! Store serão a H&M e a Macys, a soluçao para esse esse problema foi o desenvolvimento de dois scripts em python para a extração de dados das webpages da H&M e Macys com o objetivo de extrair informações relevantes sobre modelo de calças, materiais que compõem as calças, preços e outras informações relevantes.

**Como vai ser a entrega do produto final?** A entrega será da seguinte forma:

i. Será entregue dois arquivo csv com todas as informações sobre os modelos de calças, tamanho, preço, matérias-primas que compõem essas calças, sendo que um arquivo é da H&M e o outro da Macys.

ii. Para agilizar o processo de tomada de decisão e permitir que o CEO acesse essas informações de qualquer lugar, será entregue um dashboard com um resumo de todas essas informações onde estará as informações extraídas desses concorrentes, a análise de preço de mercado das calças Jeans e as questões de negócio respondidas.

## PREMISSAS DE NEGÓCIO

- Considerei as matérias-primas de composição das calças Jeans que são mais frequentes em relação a cada concorrente.

- Os dados foram extraídos durante 4 dias na última de semana de Agosto do ano de 2022.

Em relação aos produtos da H&M:

- Desconsideramos as matérias-primas dos bolsos e dos forros dos bolsos das calças Jeans.

- Sobre as matérias-primas das calças, será extraído a composição e informado a porcentagem de cada material na constituição de cada produto.

Em relação aos produtos da Macys:

- Será extraído a composição e informado se o produto possui determinada matéria-prima.

## ESTRATÉGIA DE RESOLUÇÃO

**Etapa 01 - Estudo Prévio:** Estudo do HTML das Webpages da H&M e da Macys e escolha das ferramentas de Webscraping.

**Etapa 02 - Script H&M:** Desenvolvimento do script de Webscraping para a webpage da H&M que realiza a extração de dados, limpeza e estruturação dos dados e deposita todas essas informações no banco de dados SQLITE.

**Etapa 03 - Script Macys :** Desenvolvimento do script de Webscraping para a webpage da Macys que realiza a extração de dados, limpeza e estruturação dos dados e deposita todas essas informações no banco de dados SQLITE.

**Etapa 04 - Automação de Coleta:** Automatização da coleta de dados das Webpages da Macys e da H&M utilizando o agendador de tarefas, coleta de dados realizada por 4 dias.

**Etapa 05 - Carregamento dos Dados:** Carregamento dos Dados Extraídos e estudo prévio dessas informações.

**Etapa 06 - Análise Exploratória dos Dados:** Análise dos preços máximo, mínimo e médio das calças da H&M e da Macys e Distribuição dos preços das calças.

**Etapa 07 - Dashboard:** Desenvolvimento do Dashboard para a empresa StarJeans! Store.

## RESULTADOS DE NEGÓCIO

Como resultado de negócio, foi obtido informações relevantes sobre os preço das concorrentes o que permite que os CEO's tomem a melhor decisão sobre qual preço estipular para as calças que serão produzidas a partir de modelo, cor e tamanho. Segue abaixo os gráficos:

### Análise de preço de mercado das calças da H&M

Aqui temos informações sobre os preços de cada modelo de calça da H&M

**PREÇO MÁXIMO**

<img src="https://github.com/jefferson-datascience/project_starjeans_store/blob/main/images/preco_maximo_calcas_hm.png" alt="logo" style="zoom: 100%"/>

**PREÇO MÍNIMO**

<img src="https://github.com/jefferson-datascience/project_starjeans_store/blob/main/images/preco_minimo_calcas_hm.png" alt="logo" style="zoom: 100%"/>

**PREÇO MÉDIO**

<img src="https://github.com/jefferson-datascience/project_starjeans_store/blob/main/images/preco_medio_calcas_hm.png" alt="logo" style="zoom: 100%"/>

**DISTRIBUIÇÃO DE PREÇOS DAS CALÇAS**

<img src="https://github.com/jefferson-datascience/project_starjeans_store/blob/main/images/distribuicao_precos_calcas_hm.png" alt="logo" style="zoom: 100%"/>

### Análise de preço de mercado das calças da Macys

Aqui temos informações sobre os preços de cada modelo de calça da Macys

**PREÇO MÁXIMO**

<img src="https://github.com/jefferson-datascience/project_starjeans_store/blob/main/images/preco_maximo_calcas_macys.png" alt="logo" style="zoom: 100%"/>

**PREÇO MÍNIMO**

<img src="https://github.com/jefferson-datascience/project_starjeans_store/blob/main/images/preco_minimo_calcas_macys.png" alt="logo" style="zoom: 100%"/>

**PREÇO MÉDIO**

<img src="https://github.com/jefferson-datascience/project_starjeans_store/blob/main/images/preco_medio_calcas_macys.png" alt="logo" style="zoom: 100%"/>

**DISTRIBUIÇÃO DE PREÇOS DAS CALÇAS**

<img src="https://github.com/jefferson-datascience/project_starjeans_store/blob/main/images/distribuicao_precos_calcas_macys.png" alt="logo" style="zoom: 100%"/>


## Projetos Futuros

Um ótimo projeto futuro seria sobre das questões das entregas desses produtos aos clientes. As ferramentas de extração de dados Beautiful Soup + Selenium seriam muito bem aplicadas para se investigar sobre prazos de entregas, preços de fretes e logística para variadas regiões do estado americano, dessa forma, ajudando na tomada de decisões de negócios dos CEO´s da StarJeans! e com isso gerando insights relevantes para a empresa.



### Para acessar o produto final do projeto acesse o link abaixo
https://dashboard-starjeans.onrender.com/
