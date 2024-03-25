# biops_project
Teste - Analytics Engineering (Pré Vendas) - Business Intelligence &amp; Data Modelling (Short Track)

# Primeiro Entregável: Análise de Dados e Detecção de Anomalias - Business Intelligence & Data Modeling

Este projeto apresenta uma solução de análise de dados e detecção de anomalias implementada com Python, Snowflake e Streamlit. A solução transforma datasets simples em possíveis produtos de dados acionáveis, permitindo insights estratégicos e operacionais para equipes de negócios.

## Contexto

O desafio consiste em integrar dados de uma grande indústria norte-americana, abrangendo dados de pedidos, clientes e devoluções, para identificar anomalias e oportunidades de otimização nos processos de vendas.

## Solução Proposta

A aplicação desenvolvida busca garantir a integridade e a escalabilidade dos dados, com uma abordagem que visa estruturar uma lakehouse no Snowflake, proporcionando uma camada de consumo adequada para análises avançadas e insights de negócios.

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

# Segundo Entregável: ...



## Terceiro Entregável: Arquiteturas Recomendadas

São sugeridas arquiteturas de dados em nuvem, tanto para Azure quanto para AWS, focando em serviços que atendam às necessidades de:

- **Extração e Ingestão de Dados:** Tecnologias como Azure Data Factory ou AWS Glue.
- **Transformação e Processamento:** Utilização de Azure Databricks ou AWS EMR.
- **Armazenamento e Análise:** Aplicação de Azure Synapse ou AWS Redshift.

A integração desses serviços proporcionará uma solução escalável e com governança incorporada, pronta para ambientes de produção de alta demanda.

## Conclusão

Este projeto reflete um exercício prático e estratégico em engenharia de analytics. Ele demonstra habilidades de data wrangling, validação e governança de dados, além de mostrar
