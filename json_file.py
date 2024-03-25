import pandas as pd

# Caminho para o arquivo JSON, foi salvo na máquina local
file_path = "C:\\Users\\marce\\Downloads\\data.json"

# Lendo e salvando no dataframe
with open(file_path, 'r') as f:
    df_json = pd.read_json(f)

# Função para expandir "ItemList" em colunas separadas no mesmo dataframe
def expand_item_list(df):
    # Explode 'ItemList' para trabalhar com cada item individualmente
    df = df.explode('ItemList')
    # Normaliza os itens individuais e concatena com o df original sem 'ItemList'
    df_items_expanded = pd.json_normalize(df['ItemList'])
    df_expanded = df.drop('ItemList', axis=1).reset_index(drop=True)
    df_final = pd.concat([df_expanded, df_items_expanded], axis=1)
    return df_final

# Função para normalizar e separar itens da "ItemList" em 2 dataframes
def normalize_items(df):
    df_general = df.drop('ItemList', axis=1)
    df_items = pd.json_normalize(df.to_dict(orient='records'), 'ItemList', ['NFeID'])
    return df_general, df_items

# Expandir os itens
df_expanded = expand_item_list(df_json)
# Normalizar os itens
df_general, df_items = normalize_items(df_json)

# Salvar os dataframes em arquivos CSV
df_expanded.to_csv("expanded_items.csv", index=False)
df_general.to_csv("general_info.csv", index=False)
df_items.to_csv("items_details.csv", index=False)

print("Dataframes salvos como CSV.")

print(df_expanded.head())
print(df_general.head())
print(df_items.head())
