import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import numpy as np
import snowflake.connector

# Function to establish connection to Snowflake
def snowflake_connection():
    conn = snowflake.connector.connect(
        user='********',
        password='**********',
        account='*****************', 
        warehouse='COMPUTE_WH',
        database='RAW',
        schema='RAW_BIOPS'
    )
    return conn

# Function to load data from Snowflake
def load_table_data_from_snowflake(table_name):
    conn = snowflake_connection()
    query = f"SELECT * FROM {table_name};"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Function to load data from a Snowflake view
def load_view_data_from_snowflake(view_name):
    conn = snowflake_connection()
    query = f"SELECT * FROM {view_name};"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Load the datasets from Snowflake tables
df_orders = load_view_data_from_snowflake('REFINED.REFINED_BIOPS.VW_ORDERS')
df_returns = load_table_data_from_snowflake('REFINED.REFINED_BIOPS.RETURNS')
df_people = load_table_data_from_snowflake('REFINED.REFINED_BIOPS.PEOPLE')

# Using df_orders for analysis
df = df_orders


def calculate_targets(df, profit_margin_target):
    # Calculate Total Cost based on Sales and Profit
    df['Total Cost'] = df['SALES'] - df['PROFIT']
    
    # Preparing DataFrame to store the targets
    targets = []

    # Iterate through each product in the dataset
    for product_id, group in df.groupby('PRODUCT_ID'):
        total_cost = group['Total Cost'].iloc[0]  
        quantity = group['QUANTITY'].iloc[0]  

        # Calculate Unit Price Target and Profit Target based on profit margin target
        unit_price_target = total_cost / quantity / (1 - profit_margin_target)
        profit_target = unit_price_target * profit_margin_target
        
        targets.append({
            'Product ID': product_id,
            'Unit Price Target': unit_price_target,
            'Profit Margin Target': profit_margin_target * 100,  
            'Total Cost': total_cost / quantity,  
            'Profit Target': profit_target
        })

    # Convert list of dictionaries to DataFrame
    targets_df = pd.DataFrame(targets)
    
    return targets_df



# Streamlit app
def main():
    st.title('Anomaly Detection in Sales Data')
    
    # Display Raw Data from Orders
    st.subheader('Raw Data - Orders')
    st.write(df_orders)

    # Orders - Grouped By Order ID
    df_grouped_orders = load_view_data_from_snowflake('REFINED.REFINED_BIOPS.VW_GROUPED_ORDERS')
    st.subheader('Orders - Grouped By Order ID')
    st.write(df_grouped_orders)

    # Orders - Grouped By Order ID (Filtered by People)
    df_grouped_joined_orders = load_view_data_from_snowflake('REFINED.REFINED_BIOPS.VW_GROUPED_JOINED_ORDERS')
    st.subheader('Orders - Grouped By Order ID (Filtered by People)')
    st.write(df_grouped_joined_orders)

    # Orders - Grouped By Order ID with Return Information
    df_orders_with_returns = load_view_data_from_snowflake('REFINED.REFINED_BIOPS.VW_ORDERS_WITH_RETURNS')
    st.subheader('Orders - Grouped By Order ID with Return Information')
    st.write(df_orders_with_returns)


    # Address Anomalies
    st.subheader('Address Anomalies')
    # Load address anomalies data from Snowflake view
    address_anomalies = load_view_data_from_snowflake('REFINED.REFINED_BIOPS.VW_ADDRESS_ANOMALIES')
    
    if address_anomalies.empty:
        st.write('No address anomalies detected.')
    else:
        st.write(address_anomalies)

    # Visualize relationship between Discount and Profit for Negative Profit Anomalies
    st.subheader('Visualizations')
    st.write('Relationship between Discount and Profit for Negative Profit Anomalies')
    fig, ax = plt.subplots()
    sns.scatterplot(x='DISCOUNT', y='PROFIT', data=df, ax=ax)
    st.pyplot(fig)
    
    # Display unit prices
    df_unit_prices = load_view_data_from_snowflake('REFINED.REFINED_BIOPS.VW_UNIT_PRICES')
    st.subheader('Unit Prices')
    st.write(df_unit_prices)

    # Negative Profit Anomalies
    st.subheader('Negative Profit Anomalies')
    df_negative_profit_analysis = load_view_data_from_snowflake('REFINED.REFINED_BIOPS.VW_NEGATIVE_PROFIT_ANOMALIES')
    
    if df_negative_profit_analysis.empty:
        st.write('No negative profit anomalies detected.')
    else:
        st.write(df_negative_profit_analysis)

    df_positive_profits = load_view_data_from_snowflake('REFINED.REFINED_BIOPS.VW_POSITIVE_PROFIT')  

    # Plotting the Distribution of Positive Profit Margins
    if not df_positive_profits.empty:
        fig, ax = plt.subplots()
        bin_edges = np.linspace(0, 2000, 41)  
        sns.histplot(df_positive_profits['PROFIT'], bins=bin_edges, kde=False, ax=ax, color='skyblue')
        ax.set_xlabel('Profit')
        ax.set_ylabel('Number of Transactions')
        ax.set_title('Distribution of Positive Profits')
        st.pyplot(fig)
    else:
        st.write("No transactions with positive profits to display.")
    
    # Data for Negative Profits
    df_negative_profits = load_view_data_from_snowflake('REFINED.REFINED_BIOPS.VW_NEGATIVE_PROFIT')  

    # Plotting the Distribution of Negative Profit Margins
    if not df_negative_profits.empty:
        fig, ax = plt.subplots()
        bin_edges = np.linspace(-2000, 0, 41) 
        sns.histplot(df_negative_profits['PROFIT'], bins=bin_edges, kde=False, ax=ax, color='red')
        ax.set_xlabel('Profit')
        ax.set_ylabel('Number of Transactions')
        ax.set_title('Distribution of Negative Profits')
        st.pyplot(fig)
    else:
        st.write("No transactions with negative profits to display.")

    # Product Performance Dashboard 
    st.subheader('Product Performance Dashboard')

    if df.empty:
        st.write('No data available for product performance analysis.')
    else:
        # Ensure Order Date is in datetime format
        df['ORDER_DATE'] = pd.to_datetime(df['ORDER_DATE'])
        
        # Extract year from Order Date for filtering
        df['ORDER_YEAR'] = df['ORDER_DATE'].dt.year
        
        # Generate a list of years present in the data plus an "All" option
        years = ['All'] + sorted(df['ORDER_YEAR'].unique().tolist())
        
        # Add interactive elements for filtering
        product_attributes = ['PRODUCT_ID', 'PRODUCT_NAME', 'CATEGORY', 'SUB_CATEGORY']
        selected_attribute = st.selectbox('Select Attribute:', product_attributes)
        
        # Modify to include an "All" option for Product ID
        if selected_attribute == 'PRODUCT_ID':
            unique_values = ['All'] + list(df[selected_attribute].unique())
        else:
            unique_values = df[selected_attribute].unique()
        
        selected_value = st.selectbox(f'Select {selected_attribute}:', unique_values)
        
        # New filter for selecting profit type
        profit_type = st.selectbox('Select Profit Type:', ['All', 'Positive Profit', 'Negative Profit'])

        # New filter for selecting order year
        selected_year = st.selectbox('Select Order Year:', years)
        
        # Apply filters based on user selection
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

        grouped_df = load_view_data_from_snowflake('REFINED.REFINED_BIOPS.VW_PRODUCT_PERFORMANCE')

        # Selecting specific columns to display after grouping
        columns_to_display_grouped = ['PRODUCT_ID', 'SALES', 'PROFIT', 'PRODUCT_NAME', 'CATEGORY', 'SUB_CATEGORY']
        grouped_df = grouped_df[columns_to_display_grouped]
            
        st.write(grouped_df)


    # Profit & Margin Targets with Dynamic Profit Margin Target
    st.subheader('Profit & Margin Targets')

    # Allow the user to set the Profit Margin Target dynamically
    profit_margin_target = st.slider('Set Profit Margin Target (%)', min_value=30, max_value=100, value=30, step=5) / 100.0

    # Profit & Margin Targets
    st.subheader('Profit & Margin Targets')
    if df.empty:
        st.write('No data available for analyzing profit & margin targets.')
   
    else:

        # Call the calculate_targets function with the dynamic profit margin target
        targets_df = calculate_targets(df, profit_margin_target)

        # Display the targets DataFrame
        st.write(targets_df)


    # Add new plot - Check Unit Price By Product ID
    st.subheader('Check Unit Price By Product ID')

    # User input for Product ID
    user_product_id = st.text_input('Enter Product ID:')

    # User input for Profit Margin
    user_profit_margin = st.slider('Enter Profit Margin:', min_value=30, max_value=100, value=30, step=5) / 100.0


    if user_product_id in df['PRODUCT_ID'].values:
        # Filter the DataFrame for the specified Product ID
        product_info = df[df['PRODUCT_ID'] == user_product_id]

        # Calculate Unit Price Target based on input Profit Margin
        product_info['Unit Price Target'] = product_info.apply(lambda row: row['TOTAL_COST'] / row['QUANTITY'] / (1 - user_profit_margin), axis=1)
            
        # Prepare the DataFrame to display
        display_df = pd.DataFrame({
            'Product ID': user_product_id,
            'Product Name': product_info['PRODUCT_NAME'].iloc[0],
            'Unit Price Target': product_info['Unit Price Target'].iloc[0],
            'Profit Margin': user_profit_margin * 100,  
            'Total Cost': product_info['TOTAL_COST'].iloc[0] / product_info['QUANTITY'].iloc[0],  
            'Profit': product_info['Unit Price Target'].iloc[0] - (product_info['TOTAL_COST'].iloc[0] / product_info['QUANTITY'].iloc[0]), 
        }, index=[0])

        # Display the table
        st.table(display_df)
    else:
        st.write('Please enter a valid Product ID.')


if __name__ == '__main__':
    main()