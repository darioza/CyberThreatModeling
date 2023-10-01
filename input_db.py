import pandas as pd
from sqlalchemy import create_engine

# Conectar ao banco de dados SQLAlchemy
engine = create_engine('sqlite:///instance/projeto.db')

# Função para inserir dados
def insert_data(sheet_data, table_name):
    sheet_data.to_sql(table_name, engine, if_exists='replace', index=False)

# Carregar dados do Excel
xls1 = pd.ExcelFile('Normalized_Database (1).xlsx')
xls2 = pd.ExcelFile('Normalized_Database_Assessment (1).xlsx')

# Inserir dados nas tabelas
insert_data(pd.read_excel(xls1, 'Domains'), 'Domains')
insert_data(pd.read_excel(xls1, 'Requirements'), 'Requirements')
insert_data(pd.read_excel(xls1, 'Risks'), 'Risks')
insert_data(pd.read_excel(xls1, 'PreventiveControls'), 'PreventiveControls')
insert_data(pd.read_excel(xls1, 'CorrectiveControls'), 'CorrectiveControls')
insert_data(pd.read_excel(xls1, 'DetectiveControls'), 'DetectiveControls')
insert_data(pd.read_excel(xls2, 'Requirements_assessment'), 'Requirements_assessment')
insert_data(pd.read_excel(xls2, 'Risks_assessment'), 'Risks_assessment')
insert_data(pd.read_excel(xls2, 'PreventiveControls_assessment'), 'PreventiveControls_assessment')
insert_data(pd.read_excel(xls2, 'CorrectiveControls_assessment'), 'CorrectiveControls_assessment')
insert_data(pd.read_excel(xls2, 'DetectiveControls_assessment'), 'DetectiveControls_assessment')

# Não é necessário fechar a conexão com SQLAlchemy
