# biops_project
Teste - Analytics Engineering (Pré Vendas) - Business Intelligence &amp; Data Modelling (Short Track)

# Primeiro Entregável: Análise de Dados e Detecção de Anomalias - Business Intelligence & Data Modeling

Este projeto apresenta uma solução de análise de dados e detecção de anomalias implementada com Python, Snowflake e Streamlit. A solução transforma datasets simples em possíveis produtos de dados acionáveis, permitindo insights estratégicos e operacionais para equipes de negócios.

## Contexto

O desafio consiste em integrar dados de uma grande indústria norte-americana, abrangendo dados de pedidos, clientes e devoluções, para identificar anomalias e oportunidades de otimização nos processos de vendas.

## Solução Proposta

A aplicação desenvolvida busca garantir a integridade e fácil manipulação dos dados, com uma abordagem que visa estruturar uma lakehouse no Snowflake, proporcionando uma camada de consumo adequada para análises avançadas e insights de negócios.

### Estrutura do Projeto no Snowflake

![snowflake1](https://github.com/mmiloni/biops_project/assets/25778957/d2899374-d884-4f18-b095-24108c38e3d2)

O projeto faz uso de duas principais bases de dados no Snowflake:

- `RAW`: Onde os dados são carregados em seu formato original.
- `REFINED`: Onde os dados são transformados e preparados para análise, entre criação de tabelas e views.

### Análise de Anomalias

A aplicação Streamlit é integrada ao Snowflake, uma aplicação para visualizar dados, identificar anomalias e construir produtos de dados a partir dos datasets. As visualizações incluem:

- Anomalias de endereço, sugerindo hipóteses de inconsistência nos dados.
- Relação entre descontos e lucros, indicando uma tendência de aumento do prejuízo com o crescimento dos descontos concedidos.
- Performance dos produtos ao longo do tempo, possibilitando um monitoramento estratégico e operacional.

### Visualizações Implementadas

As imagens a seguir demonstram as visualizações e análises realizadas através do Streamlit:

- **Dados Brutos dos Pedidos**

![sis1](https://github.com/mmiloni/biops_project/assets/25778957/47f0f62e-6345-4d09-93c3-3fc482fc2376)

- **Anomalias de Endereço**
  
![sis2](https://github.com/mmiloni/biops_project/assets/25778957/5f3c6f8b-fe39-4767-a820-ed2e6f5ea9c6)

- **Relação entre Desconto e Lucro**
  
![sis3](https://github.com/mmiloni/biops_project/assets/25778957/cbc29b4f-6185-40de-b267-72ffc5ceb9ba)

- **Anomalias de Lucro Negativo**
  
![sis4](https://github.com/mmiloni/biops_project/assets/25778957/f440775e-b72f-40aa-8751-8f0b5aa6b7c5)

- **Distribuição de Lucros Positivos e Negativos**
  
![sis5](https://github.com/mmiloni/biops_project/assets/25778957/81e9a068-db77-496e-9bb0-878ffb35e19f)

- **Dashboard de Performance dos Produtos**
  
![sis6](https://github.com/mmiloni/biops_project/assets/25778957/6aec4c21-3fc5-4fe5-bd97-15349e26bd01)

- **Definição de Metas de Lucro e Margem**
  
![sis7](https://github.com/mmiloni/biops_project/assets/25778957/1ec8ffe2-35ad-4d05-9340-db6ae74a8e2d)

## Futuras Implementações e Melhorias

- **Governança de Dados:** Estruturação de uma framework robusta de governança para gestão e qualidade, linhagem de dados. Gestão de acesso, permissionamento e mascaramento de informações.
- **Definição de Arquitetura alinhado ao planejamento estratégico de Governança:** Implementação da arquitetura para atender e atingir da melhor forma a democratização dos dados.
- **Automatização:** Desenvolvimento de funcionalidades para automação de recomendações de precificação de produtos. Com foco em produtização de dados, e como essas funcionalidades podem voltar para a aplicação como forma de assegurar a eficácia de novas regras de negócio.

# Segundo Entregável: 

Foi feito upload do código Python: json_file.py

Como resultado da execução deste programa, temos 3 arquivos CSV para demonstrar os datasets finais:
- expanded_items.csv
- general_info.csv
- items_details.csv

## Terceiro Entregável: Arquiteturas Recomendadas

Sugestão de arquitetura de Big Data em AWS, focando em serviços que atendam às necessidades de:

- **Extração e Ingestão de Dados:** Tecnologias como AWS Glue.
- **Transformação e Processamento:** Utilização de Glue ou AWS EMR.
- **Armazenamento e Análise:** Utilização de Athena e AWS Redshift.
- **Gestão de Dados:** Catálogo de dados, Gestão de acesso e permissões.

![aws_big_data_architecture](https://github.com/mmiloni/biops_project/assets/25778957/14263558-c2cb-463d-ba1a-beec9a1d21d8)

A integração desses serviços proporcionará uma solução escalável e com governança incorporada, pronta para ambientes de produção de alta demanda.

## Conclusão

Avaliação final:
Quanto ao primeiro entregável, diversas hipóteses foram validadas que, em cenário de vida real, poderiam ser discutidas com especialistas do negócio e os donos dos dados. Todas as renderizações no Streamlit tem como propósito levantar uma possível discussão ou evidenciar um tratamento necessário do dado que requer uma validação.

Quanto ao segundo entregável, ele é bem direto ao ponto e com o entregável que pode ser visualizado, por isso a demnonstração do código e os datasets que ele gera.

O terceiro entregável é o mais subjetivo, parti do princípio de que se tratava de um projeto de Big Data e, mesmo assim, ainda trouxe mais de um caminho possível na arquitetura. destacando as Etapas:
- Ingestão de dados
- Tratamento, transformação e movimentação de dados
- Processamento de dados
- Camadas de disponibilidade e consumo de dados.

Se tivesse mais tempo, o que você faria para melhorar a sua solução?

Como mencionei, em um cenário da vida real temos diversas ações que acontecem entre ser apresenbtado com um cenário e a solução, exemplos:
- Entregável 1: esta não me parece a modelagem original, eu esperaria uma separação enbtre as informações de transação, cliente, endereço, produtos, precificação, etc. Tudo estava quase que totalmente consolidado em uma planilha, obviamente eu gostaria de entender qual a origem desses dados, e sugerir uma arquitetura em cima das origens reais. Além disso, há diversas discussões sobre o porquê o dataset estar assim, é possível imaginar que o dataset está incompleto (acredito que parte do teste tem essa intenção), não temos dados do preço de cada produto e o custo de produção dele, muitas coisas temos que deduzir para aplicar uma solução ao teste, enquanto que na vida real eu daria diversos passos para trás a fim de clarificar todas essas questões antes.
- No terceiro entregável, muitas dessas questões também se aplicam. O único dataset a ser carregado será das notas fiscais? Obviamente em um projeto isso dificilmente aconteceria, estaríamos falando de todo um sistema de origem. sistema do qual não temos informações sobre volumetria, quantidade de integrações a serem feitas (pipelines), quantidade de consumidores, finalidade do proejto. Enfim, diversas questões que em um cenário real teríamos espeço para questionar e poder precisar o desenho da solução. É comum quando estamos na posição de quem faz o desenho da solução sermos questionados de qual a melhor solução possível, muitas vezes a melhor resposta é "depende", pois temos várias questões em aberto aqui, por isso preferi trazer um desenho mais abrangente e trazer minha recomendações para um cenário que se trata de Big Data e deve ser uma adoção massiva dentro da empresa.
