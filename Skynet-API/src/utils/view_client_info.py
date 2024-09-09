'''Criar a view ClienteInfo com as informações básicas dos clientes.'''
import sqlite3

# Passo 1: Conectar ao banco de dados
conn = sqlite3.connect('./db/Skynet.db')  # Conecta ao banco de dados SQLite existente ou cria um novo
cursor = conn.cursor()

# Passo 2: Criar a view 'ClienteInfo'
create_view_sql = """
CREATE VIEW IF NOT EXISTS ClienteInfo AS
SELECT 
    c.cpf,
    c.nome AS Cliente,
    ctr.tipo_servico AS Serviço,
    ch.status AS Chamados,
    ch.categoria AS Setor,
    ch.descricao AS Problema
FROM 
    Clientes c
LEFT JOIN contratos ctr ON c.cliente_id = ctr.cliente_id
LEFT JOIN Chamados ch ON c.cliente_id = ch.cliente_id;
"""

cursor.executescript(create_view_sql)
conn.commit()

# Passo 3: Verificar se a view foi criada corretamente
cursor.execute("SELECT name FROM sqlite_master WHERE type='view';")
views = cursor.fetchall()

print("Views criadas:")
for view in views:
    print(view[0])

# Fechar a conexão
conn.close()
