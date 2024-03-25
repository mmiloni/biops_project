import pandas as pd
import snowflake.connector

# Url pública do arquivo Excel de sample
excel_url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vR25kb-kFz17SwOFCGVxBSOS6UEQK2ls-lj8EI1vuF926tKa5gDXCmfJEYZZz5eRAxTrGslRwdJaVNV/pub?output=xlsx'

# Lendo cada aba do arquivo Excel e transformando em DataFrames
df_orders = pd.read_excel(excel_url, sheet_name='Orders')
df_returns = pd.read_excel(excel_url, sheet_name='Returns')
df_people = pd.read_excel(excel_url, sheet_name='People')

# Transformando os DFs em arquivos Parquet
df_orders.to_parquet('orders.parquet', index=False)
df_returns.to_parquet('returns.parquet', index=False)
df_people.to_parquet('people.parquet', index=False)

# Conectando ao Snowflake
conn = snowflake.connector.connect(
    user='*********',
    password='**********',
    account='********************',
    warehouse='COMPUTE_WH',
    database='RAW',
    schema='RAW_BIOPS'
)

# Função para fazer upload de arquivos para o Snowflake
def upload_file_to_snowflake(file_name, stage_name='RAW_STG_BIOPS'):
    cs = conn.cursor()

    put_command = f"PUT file://{file_name} @{stage_name} AUTO_COMPRESS=TRUE PARALLEL=8;"
    cs.execute(put_command)

# Execução da função para fazer upload dos arquivos para o Snowflake
upload_file_to_snowflake('orders.parquet')
upload_file_to_snowflake('returns.parquet')
upload_file_to_snowflake('people.parquet')

conn.close()
