"""script para criar o banco de dados."""
import sqlite3

# Passo 1: Criar conexão com o banco de dados
conn = sqlite3.connect(
    './db/Skynet.db'
)  # Nome do arquivo do banco de dados SQLite
cursor = conn.cursor()

# Passo 2: Ler o script SQL do arquivo
script_sql = """
-- Tabela `Clientes`
DROP TABLE IF EXISTS Clientes;

CREATE TABLE IF NOT EXISTS Clientes (
  cliente_id INTEGER PRIMARY KEY ,
  cpf TEXT NOT NULL UNIQUE,
  nome TEXT NOT NULL,
  email TEXT NOT NULL,
  telefone TEXT NOT NULL,
  endereco TEXT NOT NULL,
  data_cadastro DATE NOT NULL
);

-- Tabela `Planos`
DROP TABLE IF EXISTS Planos;

CREATE TABLE IF NOT EXISTS Planos (
  plano_id INTEGER PRIMARY KEY ,
  nome TEXT NOT NULL,
  descricao TEXT,
  velocidade TEXT NOT NULL,
  preco DECIMAL(10, 2) NOT NULL,
  tipo TEXT NOT NULL
);

-- Tabela `Contratos`
DROP TABLE IF EXISTS Contratos;

CREATE TABLE IF NOT EXISTS Contratos (
  contrato_id INTEGER PRIMARY KEY ,
  cliente_id INTEGER NOT NULL,
  plano_id INTEGER NOT NULL,
  data_inicio DATE NOT NULL,
  data_fim DATE,
  status TEXT CHECK(status IN ('Ativo', 'Inativo')) NOT NULL,
  tipo_servico TEXT NOT NULL,
  FOREIGN KEY (cliente_id) REFERENCES Clientes (cliente_id),
  FOREIGN KEY (plano_id) REFERENCES Planos (plano_id)
);

-- Tabela `Chamados`
DROP TABLE IF EXISTS Chamados;

CREATE TABLE IF NOT EXISTS Chamados (
  chamado_id INTEGER PRIMARY KEY ,
  cliente_id INTEGER NOT NULL,
  data_abertura DATETIME NOT NULL,
  data_fechamento DATETIME,
  status TEXT CHECK(status IN ('Aberto', 'Em Andamento', 'Fechado')) NOT NULL,
  prioridade TEXT CHECK(prioridade IN ('Baixa', 'Média', 'Alta')) NOT NULL,
  categoria TEXT CHECK(categoria IN ('Suporte', 'Financeiro', 'Comercial')) NOT NULL,
  descricao TEXT NOT NULL,
  resolucao TEXT,
  FOREIGN KEY (cliente_id) REFERENCES Clientes (cliente_id)
);

-- Tabela `Atendentes`
DROP TABLE IF EXISTS Atendentes;

CREATE TABLE IF NOT EXISTS Atendentes (
  atendente_id INTEGER PRIMARY KEY ,
  nome TEXT NOT NULL,
  email TEXT NOT NULL UNIQUE,
  telefone TEXT,
  especialidade TEXT CHECK(especialidade IN ('Suporte', 'Financeiro', 'Comercial')) NOT NULL
);

-- Tabela `Historico_Atendimento`
DROP TABLE IF EXISTS Historico_Atendimento;

CREATE TABLE IF NOT EXISTS Historico_Atendimento (
  historico_id INTEGER PRIMARY KEY ,
  chamado_id INTEGER NOT NULL,
  atendente_id INTEGER NOT NULL,
  data_atendimento DATETIME NOT NULL,
  descricao TEXT NOT NULL,
  historico_texto TEXT,
  FOREIGN KEY (chamado_id) REFERENCES Chamados (chamado_id),
  FOREIGN KEY (atendente_id) REFERENCES Atendentes (atendente_id)
);

-- Tabela `Faturas`
DROP TABLE IF EXISTS Faturas;

CREATE TABLE IF NOT EXISTS Faturas (
  fatura_id INTEGER PRIMARY KEY ,
  contrato_id INTEGER NOT NULL,
  boleto TEXT,
  data_emissao DATE NOT NULL,
  data_vencimento DATE NOT NULL,
  valor DECIMAL(10, 2) NOT NULL,
  status TEXT CHECK(status IN ('Paga', 'Pendente', 'Atrasada')) NOT NULL,  
  FOREIGN KEY (contrato_id) REFERENCES Contratos (contrato_id)
);

-- Tabela `Pagamentos`
DROP TABLE IF EXISTS Pagamentos;

CREATE TABLE IF NOT EXISTS Pagamentos (
  pagamento_id INTEGER PRIMARY KEY ,
  fatura_id INTEGER NOT NULL,
  data_pagamento DATE NOT NULL,
  valor_pago DECIMAL(10, 2) NOT NULL,
  forma_pagamento TEXT CHECK(forma_pagamento IN ('Boleto', 'Crédito', 'PIX', 'Outros')) NOT NULL,
  FOREIGN KEY (fatura_id) REFERENCES Faturas (fatura_id)
);
"""

# Passo 3: Executar o script SQL
cursor.executescript(script_sql)
conn.commit()

# Passo 4: Verificar as tabelas criadas
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

print('Tabelas criadas:')
for table in tables:
    print(table[0])

# Fechar a conexão com o banco de dados
conn.close