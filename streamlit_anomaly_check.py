from snowflake.snowpark.context import get_active_session
import pandas as pd
import altair as alt
import streamlit as st

# Acessando com as credenciais atuais
session = get_active_session()

# Função para executar as queries e salvar em dataframe do pandas
def run_query(sql):
    results = session.sql(sql).collect()
    df = pd.DataFrame(results)
    return df

# Carregar os datasets das tabelas e views do Snowflake
df_orders = run_query('SELECT * FROM REFINED.REFINED_BIOPS.VW_ORDERS')
df_returns = run_query('SELECT * FROM REFINED.REFINED_BIOPS.RETURNS')
df_people = run_query('SELECT * FROM REFINED.REFINED_BIOPS.PEOPLE')

# Definindo o df_orders como dataframe principal
df = df_orders

# Função para cálculo de margem e lucro alvos
def calculate_targets(df, profit_margin_target):
    # Calculate Total Cost based on Sales and Profit
    df['Total Cost'] = df['SALES'] - df['PROFIT']
    
    targets = []

    # Itera por cada produto no dataset
    for product_id, group in df.groupby('PRODUCT_ID'):
        total_cost = group['Total Cost'].iloc[0]  
        quantity = group['QUANTITY'].iloc[0]  

        # Calcula Unit Price Target e Profit Target baseados na margem de lucro alvo
        unit_price_target = total_cost / quantity / (1 - profit_margin_target)
        profit_target = unit_price_target * profit_margin_target
        
        targets.append({
            'Product ID': product_id,
            'Unit Price Target': unit_price_target,
            'Profit Margin Target': profit_margin_target * 100,  # Convert to percentage
            'Total Cost': total_cost / quantity,  # Assuming cost is consistent across quantities
            'Profit Target': profit_target
        })

    # Converte a lista de dicionários para o dataframe
    targets_df = pd.DataFrame(targets)
    
    return targets_df

# Streamlit app
def main():
    st.title('Anomaly Detection in Sales Data')
    
    # Plota o dataset cru de Orders
    st.subheader('Raw Data - Orders')
    st.write('Tabela de Orders, mantendo a mesma estrutura da origem.\nDataset não contém preço unitário do produto e fatores que contribuem para o lucro, como custo total de fabricação e operação.')
    st.write(df_orders)

    # Orders - Grouped By Order ID
    df_grouped_orders = run_query('SELECT * FROM REFINED.REFINED_BIOPS.VW_GROUPED_ORDERS')
    st.subheader('Orders - Grouped By Order ID')
    st.write('Tabela de Orders agurpada por Order ID, com agregação dos valores como Sales e Profit.\nTestando hipóteses da venda de diversos itens não ter sido negativa em conjunto, mas sim apenas olhando para um item isolado.')
    st.write(df_grouped_orders)

    # Orders - Grouped By Order ID (Filtrado pelas pessoas contidas no dataset People)
    df_grouped_joined_orders = run_query('SELECT * FROM REFINED.REFINED_BIOPS.VW_GROUPED_JOINED_ORDERS')
    st.subheader('Orders - Grouped By Order ID (Filtered by People)')
    st.write('Premissa similar com a renderização acima, porém, fazendo join com pessoas para buscar possível anomalia específica com este grupo.')
    st.write(df_grouped_joined_orders)

    # Orders - Grouped By Order ID com informações de Returns
    df_orders_with_returns = run_query('SELECT * FROM REFINED.REFINED_BIOPS.VW_ORDERS_WITH_RETURNS')
    st.subheader('Orders - Grouped By Order ID with Return Information')
    st.write('Novamente uma premissa muito parecida, agora fazendo join também com tabela das compras retornadas.')
    st.write(df_orders_with_returns)


    # Anomalias de endereços - basicamente procura registros de 1 cliente para n endereços
    st.subheader('Address Anomalies')
    st.write('Partindo da premissa que a anomalia pode ser apenas inconsistência de dados, como N endereços atribuídos a mesma pessoa, mas parece ser um caso constante neste dataset. O mesmo princípio poderia ser usado para cchecar se o mesmo produto por vezes está em categoria diferente, sub-categorias em categorias diferentes, data de envio menor que data da transação e inconsistências na relação Sales/Quantity.')
    address_anomalies = run_query('SELECT * FROM REFINED.REFINED_BIOPS.VW_ADDRESS_ANOMALIES')
    if address_anomalies.empty:
        st.write('No address anomalies detected.')
    else:
        st.write(address_anomalies)

    
    # Visualizar possível relação entre Discount e Profit para lucros negativos
    st.subheader('Visualizations')
    st.write('Buscando visualizar uma possível tendência de aumento de lucro negativo conforme aumento de desconto.')
    scatter_data = df[['DISCOUNT', 'PROFIT']]
    scatter_chart = alt.Chart(scatter_data).mark_circle(size=60).encode(
        x='DISCOUNT',
        y='PROFIT',
        tooltip=['DISCOUNT', 'PROFIT']
    ).interactive()
    
    # Renderiza o gráfico
    st.altair_chart(scatter_chart, use_container_width=True)
    
    # Plota a tabela de Unit Prices
    df_unit_prices = run_query('SELECT * FROM REFINED.REFINED_BIOPS.VW_UNIT_PRICES')
    st.subheader('Unit Prices')
    st.write('Partindo do ponto que a tabela Orders não fornece o preço unitário, parecia importante termos essa visão, inclusive para calcular novas métricas como custo total para operacionalizar a venda do produto e margem de lucro.')
    st.write(df_unit_prices)

    # Anomalias de lucros negativos
    st.subheader('Negative Profit Anomalies')
    st.write('Esta seção renderiza uma view que filtra os registros com lucro negativo. Temos 6 campos calculados que evidenciam que, caso não houvessem concedido descontos, quase não teríamos lucro negativo, porém, abre espaço também para questionar a eficácia da precificação, visto que muito produtos, mesmo sem desconto, ficam com lucro 0 ou muito próximo disso e alguns poucos ainda com lucro negativo.')
    df_negative_profit_analysis = run_query('SELECT * FROM REFINED.REFINED_BIOPS.VW_NEGATIVE_PROFIT_ANOMALIES')
    
    if df_negative_profit_analysis.empty:
        st.write('No negative profit anomalies detected.')
    else:
        st.write(df_negative_profit_analysis)

    # Carrega dados com lucros positivos
    df_positive_profits = run_query('SELECT * FROM REFINED.REFINED_BIOPS.VW_POSITIVE_PROFIT')  

    # Plota a distribuição de margem de lucro positiva
    if not df_positive_profits.empty:
        positive_profits_chart = alt.Chart(df_positive_profits).mark_bar(color='skyblue').encode(
            alt.X('PROFIT:Q', bin=alt.Bin(maxbins=80), title='Profit'),
            alt.Y('count()', title='Number of Transactions')
        ).properties(
            title='Distribution of Positive Profits'
        )
        
        st.subheader('Positive Profit Distribution')
        st.write('Evidencia uma possível tendência a zero dos lucros, mas também pode ser explicado pelo valor baixo tanto do produto unitário como ticket médio.')
        st.altair_chart(positive_profits_chart, use_container_width=True)
    else:
        st.write("No transactions with positive profits to display.")
    
    # Carrega dados de lucros negativos
    df_negative_profits = run_query('SELECT * FROM REFINED.REFINED_BIOPS.VW_NEGATIVE_PROFIT')  

    # Plota a distribuição de margem de lucro negativa
    if not df_negative_profits.empty:
        negative_profits_chart = alt.Chart(df_negative_profits).mark_bar(color='red').encode(
            alt.X('PROFIT:Q', bin=alt.Bin(maxbins=60), title='Profit'),
            alt.Y('count()', title='Number of Transactions')
        ).properties(
            title='Distribution of Negative Profits'
        )
        
        st.subheader('Negative Profit Distribution')
        st.write('Distribuição parecida com os lucros, mas invertidas, e com número de transações menor, porém evidencia uma distribuição e range negativos muito preocupantes.')
        st.altair_chart(negative_profits_chart, use_container_width=True)
    else:
        st.write("No transactions with negative profits to display.")

    #  Dash para avaliar perfomance dos produtos
    st.subheader('Product Performance Dashboard')
    st.write('Análise de performance dos produtos. Interessante para analisar se houve períodos determinados que tal produto performou negativamente ou se é uma constante.')
    
    if df.empty:
        st.write('No data available for product performance analysis.')
    else:
        df['ORDER_DATE'] = pd.to_datetime(df['ORDER_DATE'])
        df['ORDER_YEAR'] = df['ORDER_DATE'].dt.year
        years = ['All'] + sorted(df['ORDER_YEAR'].unique().tolist())
        product_attributes = ['PRODUCT_ID', 'PRODUCT_NAME', 'CATEGORY', 'SUB_CATEGORY']
        selected_attribute = st.selectbox('Select Attribute:', product_attributes)
        
        # Incluindo opção "All" para Product ID
        if selected_attribute == 'PRODUCT_ID':
            unique_values = ['All'] + list(df[selected_attribute].unique())
        else:
            unique_values = df[selected_attribute].unique()
        
        selected_value = st.selectbox(f'Select {selected_attribute}:', unique_values)
        
        profit_type = st.selectbox('Select Profit Type:', ['All', 'Positive Profit', 'Negative Profit'])
        selected_year = st.selectbox('Select Order Year:', years)
        
        if selected_value != 'All':
            filtered_df = df[df[selected_attribute] == selected_value]
        else:
            filtered_df = df.copy()
        
        if profit_type == 'Positive Profit':
            filtered_df = filtered_df[filtered_df['PROFIT'] >= 0]
        elif profit_type == 'Negative Profit':
            filtered_df = filtered_df[filtered_df['PROFIT'] < 0]
        
        if selected_year != 'All':
            filtered_df = filtered_df[filtered_df['ORDER_YEAR'] == selected_year]

        grouped_df = run_query('SELECT * FROM REFINED.REFINED_BIOPS.VW_PRODUCT_PERFORMANCE')

        # Selecionando as colunas específicas para plotar
        columns_to_display_grouped = ['PRODUCT_ID', 'SALES', 'PROFIT', 'PRODUCT_NAME', 'CATEGORY', 'SUB_CATEGORY']
        grouped_df = grouped_df[columns_to_display_grouped]
            
        st.write(grouped_df)


    # Setando lucros e margens alvos de forma dinâmica
    st.subheader('Profit & Margin Targets')
    st.write('Possibilita o usuário flutuar o alvo da margem de lucro que deseja.')

    profit_margin_target = st.slider('Set Profit Margin Target (%)', min_value=30, max_value=100, value=30, step=5) / 100.0
    st.subheader('Profit & Margin Targets')
    st.write('Reflete nos preços dos produtos a margem de lucro escolhida, proém para todos os produtos.')
    if df.empty:
        st.write('No data available for analyzing profit & margin targets.')
   
    else:
        targets_df = calculate_targets(df, profit_margin_target)
        st.write(targets_df)

    # Checando valores entre mínimos e máximos para Unit Prices
    st.subheader('Check Unit Price By Product ID')
    st.write('Possibilita o usuário a consultar valores possíveis para um único produto, dentro do range de margens de lucro aceitáveis para o negócio.')
    
    user_product_id = st.text_input('Enter Product ID:')
    user_profit_margin = st.slider('Enter Profit Margin:', min_value=30, max_value=100, value=30, step=5) / 100.0

    if user_product_id in df['PRODUCT_ID'].values:
        # Filtra o dataframe para o Product ID específico
        product_info = df[df['PRODUCT_ID'] == user_product_id]
        product_info['Unit Price Target'] = product_info.apply(lambda row: row['TOTAL_COST'] / row['QUANTITY'] / (1 - user_profit_margin), axis=1)
            
        display_df = pd.DataFrame({
            'Product ID': user_product_id,
            'Product Name': product_info['PRODUCT_NAME'].iloc[0],
            'Unit Price Target': product_info['Unit Price Target'].iloc[0],
            'Profit Margin': user_profit_margin * 100,  # Convert to percentage
            'Total Cost': product_info['TOTAL_COST'].iloc[0] / product_info['QUANTITY'].iloc[0],  # Average total cost
            'Profit': product_info['Unit Price Target'].iloc[0] - (product_info['TOTAL_COST'].iloc[0] / product_info['QUANTITY'].iloc[0]),  # Average profit per unit
        }, index=[0])
        st.table(display_df)
        
    else:
        st.write('Please enter a valid Product ID.')

if __name__ == '__main__':
    main()