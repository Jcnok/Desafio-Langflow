"""Carrega(load) os dados para o banco de dados Skynet."""
import csv
import sqlite3


def load_data_from_csv(conn, table_name, csv_file):
    """Função para conectar ao banco de dados e carregar dados."""
    """Deve informar:
                     conn: var da conexão com o bd.
                     table_name: nome da tabela para atualizar.
                     csv_file: path do arquivo que contém os dados.csv para atualizar.
    """
    cursor = conn.cursor()
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        columns = ', '.join(reader.fieldnames)
        placeholders = ':' + ', :'.join(reader.fieldnames)
        sql = f'INSERT INTO {table_name} ({columns}) VALUES ({placeholders})'
        for row in reader:
            cursor.execute(sql, row)
    conn.commit()


# Conectar ao banco de dados
conn = sqlite3.connect('./db/Skynet.db')

# Carregar dados de cada arquivo CSV para as respectivas tabelas
load_data_from_csv(conn, 'Clientes', './data/clientes.csv')
load_data_from_csv(conn, 'Planos', './data/planos.csv')
load_data_from_csv(conn, 'Contratos', './data/contratos.csv')
load_data_from_csv(conn, 'Chamados', './data/chamados.csv')
load_data_from_csv(conn, 'Atendentes', './data/atendentes.csv')
load_data_from_csv(
    conn, 'Historico_Atendimento', './data/historico_atendimento.csv'
)
load_data_from_csv(conn, 'Faturas', './data/faturas.csv')
load_data_from_csv(conn, 'Pagamentos', './data/pagamentos.csv')

# Fechar a conexão
conn.close()

print('Dados carregados com sucesso para o banco de dados SQLite.')
