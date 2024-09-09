"""CRM - Skynet Provider."""
import random
import re
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timedelta
from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title='Skynet CRM API')

# Configuração do banco de dados
DATABASE = './db/Skynet.db'


@contextmanager
def get_db():
    """Gerenciador de contexto para conexão com o banco de dados."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


# Modelos Pydantic
class ClienteBase(BaseModel):
    """validação da tabela clientes."""

    cpf: str
    nome: str
    email: str
    telefone: str
    endereco: str


class ClienteCreate(ClienteBase):
    """passar."""

    pass


class Cliente(ClienteBase):
    """validação da tabela clientes."""

    cliente_id: int

    class Config:
        """configuração."""

        orm_mode = True


class ClienteUpdate(BaseModel):
    """validação update tabela clientes."""

    nome: Optional[str] = None
    email: Optional[str] = None
    telefone: Optional[str] = None
    endereco: Optional[str] = None


class Plano(BaseModel):
    """validação tabela plano."""

    plano_id: int
    nome: str
    descricao: Optional[str]
    velocidade: str
    preco: float
    tipo: str


class Chamado(BaseModel):
    """validação tabela chamado."""

    chamado_id: int
    cliente_id: int
    data_abertura: str   # datetime
    data_fechamento: str   # Optional[datetime]
    status: str
    prioridade: str
    categoria: str
    descricao: str
    resolucao: Optional[str]


class ChamadoCreate(BaseModel):
    """validação para criar chamado."""

    cliente_id: int
    categoria: str
    prioridade: str
    descricao: str


class BoletoResponse(BaseModel):
    """validação gerar boleto."""

    boleto_cod: str
    vencimento: str
    valor: float


class ResponseModel(BaseModel):
    """validação tabela fatura."""

    fatura_id: int
    contrato_id: int
    data_emissao: str
    data_vencimento: str
    valor: float
    status: str
    boleto: Optional[str] = None


# Função para gerar código de boleto
def gerar_codigo_boleto():
    """Gera um código de boleto aleatório."""
    campos = [f'{random.randint(10000, 99999):05d}' for _ in range(5)]
    dv = random.randint(0, 9)
    return f"23790.{campos[0]} {campos[1]}.{campos[2]} {campos[3]}.{campos[4]} {dv} {''.join(campos)}"


# Rotas CRUD
@app.post('/clientes/', response_model=Cliente)
def create_cliente(cliente: ClienteCreate):
    """Cria um novo cliente."""
    with get_db() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO Clientes (cpf, nome, email, telefone, endereco, data_cadastro)
                VALUES (?, ?, ?, ?, ?, DATE('now'))
            """,
                (
                    cliente.cpf,
                    cliente.nome,
                    cliente.email,
                    cliente.telefone,
                    cliente.endereco,
                ),
            )
            conn.commit()
            cliente_id = cursor.lastrowid
        except sqlite3.IntegrityError:
            raise HTTPException(
                status_code=400, detail='CPF ou email já cadastrado'
            )

    return {**cliente.dict(), 'cliente_id': cliente_id}


@app.get('/clientes/{cliente_id}', response_model=Cliente)
def read_cliente(cliente_id: int):
    """Retorna os dados de um cliente específico, informe o id do cliente."""
    with get_db() as conn:
        cursor = conn.cursor()
        cliente = cursor.execute(
            'SELECT * FROM Clientes WHERE cliente_id = ?', (cliente_id,)
        ).fetchone()

    if cliente is None:
        raise HTTPException(status_code=404, detail='Cliente não encontrado')
    return dict(cliente)


@app.get('/clientes/', response_model=List[Cliente])
def read_clientes():
    """Retorna a lista de todos os clientes."""
    with get_db() as conn:
        cursor = conn.cursor()
        clientes = cursor.execute('SELECT * FROM Clientes;').fetchall()
    return [dict(cliente) for cliente in clientes]


@app.put('/clientes/{cliente_id}', response_model=Cliente)
def update_cliente(cliente_id: int, cliente: ClienteUpdate):
    """Atualiza os dados de um cliente específico."""
    with get_db() as conn:
        cursor = conn.cursor()
        update_data = {
            k: v for k, v in cliente.dict().items() if v is not None
        }
        if not update_data:
            raise HTTPException(
                status_code=400, detail='Nenhum campo para atualizar'
            )

        set_clause = ', '.join(f'{k} = ?' for k in update_data.keys())
        values = list(update_data.values()) + [cliente_id]

        try:
            cursor.execute(
                f'UPDATE Clientes SET {set_clause} WHERE cliente_id = ?',
                values,
            )
            conn.commit()
        except sqlite3.IntegrityError:
            raise HTTPException(
                status_code=400, detail='Erro ao atualizar cliente'
            )

        updated_cliente = cursor.execute(
            'SELECT * FROM Clientes WHERE cliente_id = ?', (cliente_id,)
        ).fetchone()

    if updated_cliente is None:
        raise HTTPException(status_code=404, detail='Cliente não encontrado')
    return dict(updated_cliente)


@app.delete('/clientes/{cliente_id}')
def delete_cliente(cliente_id: int):
    """Remove um cliente do sistema."""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            'DELETE FROM Clientes WHERE cliente_id = ?', (cliente_id,)
        )
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=404, detail='Cliente não encontrado'
            )
    return {'message': 'Cliente deletado com sucesso'}


# Rota para buscar cliente pelo telefone
@app.get('/clientes/telefone/{telefone}', response_model=Cliente)
def get_cliente_by_telefone(telefone: str):
    """Busca um cliente pelo número de telefone. Formato exemplo: 81961028817."""
    with get_db() as conn:
        cursor = conn.cursor()
        cliente = cursor.execute(
            'SELECT * FROM Clientes WHERE telefone = ?', (telefone,)
        ).fetchone()

    if cliente is None:
        raise HTTPException(status_code=404, detail='Cliente não encontrado')
    return dict(cliente)


# Rota para listar chamados de um cliente
@app.get('/clientes/{cliente_id}/chamados', response_model=List[Chamado])
def get_chamados_by_cliente(cliente_id: int):
    """Lista todos os chamados de um cliente específico em ordem do mais Recente."""
    with get_db() as conn:
        cursor = conn.cursor()
        chamados = cursor.execute(
            """
            SELECT * FROM Chamados 
            WHERE cliente_id = ? 
            ORDER BY data_abertura DESC
        """,
            (cliente_id,),
        ).fetchall()

    if not chamados:
        raise HTTPException(
            status_code=404,
            detail='Nenhum chamado encontrado para este cliente',
        )
    return [dict(chamado) for chamado in chamados]


# Rota para resumo do cliente (dados básicos + últimos chamados)
@app.get('/clientes/{cliente_id}/resumo')
def get_cliente_resumo(cliente_id: int):
    """Retorna um resumo dos dados do cliente, incluindo últimos 5 chamados e contratos."""
    with get_db() as conn:
        cursor = conn.cursor()
        cliente = cursor.execute(
            'SELECT * FROM Clientes WHERE cliente_id = ?', (cliente_id,)
        ).fetchone()
        if cliente is None:
            raise HTTPException(
                status_code=404, detail='Cliente não encontrado'
            )

        ultimos_chamados = cursor.execute(
            """
            SELECT * FROM Chamados 
            WHERE cliente_id = ? 
            ORDER BY data_abertura DESC 
            LIMIT 5
        """,
            (cliente_id,),
        ).fetchall()

        contratos = cursor.execute(
            """
            SELECT c.*, p.nome as plano_nome, p.velocidade, p.preco
            FROM Contratos c
            JOIN Planos p ON c.plano_id = p.plano_id
            WHERE c.cliente_id = ?
            ORDER BY c.data_inicio DESC
        """,
            (cliente_id,),
        ).fetchall()

    return {
        'cliente': dict(cliente),
        'ultimos_chamados': [dict(chamado) for chamado in ultimos_chamados],
        'contratos': [dict(contrato) for contrato in contratos],
    }


# Rotas para Planos
@app.get('/planos/', response_model=List[Plano])
def read_planos():
    """Lista todos os planos disponíveis."""
    with get_db() as conn:
        cursor = conn.cursor()
        planos = cursor.execute('SELECT * FROM Planos').fetchall()
    return [dict(plano) for plano in planos]


@app.get('/planos/{plano_id}', response_model=Plano)
def read_plano(plano_id: int):
    """Retorna os detalhes de um plano específico pelo id do plano."""
    with get_db() as conn:
        cursor = conn.cursor()
        plano = cursor.execute(
            'SELECT * FROM Planos WHERE plano_id = ?', (plano_id,)
        ).fetchone()

    if plano is None:
        raise HTTPException(status_code=404, detail='Plano não encontrado')
    return dict(plano)


@app.get('/clientes/{cliente_id}/plano', response_model=Plano)
def get_plano_cliente(cliente_id: int):
    """Retorna o útimo plano ativo de um cliente específico."""
    with get_db() as conn:
        cursor = conn.cursor()
        plano = cursor.execute(
            """
            SELECT p.* FROM Planos p
            JOIN Contratos c ON p.plano_id = c.plano_id
            WHERE c.cliente_id = ? AND c.status = 'Ativo'
            ORDER BY c.data_inicio DESC
            LIMIT 1
        """,
            (cliente_id,),
        ).fetchone()

    if plano is None:
        raise HTTPException(
            status_code=404,
            detail='Plano ativo não encontrado para este cliente',
        )
    return dict(plano)


# Rotas para Suporte
@app.post('/suporte/chamados/', response_model=Chamado)
def create_chamado(chamado: ChamadoCreate):
    """Cria um novo chamado de suporte.Formatos."""
    """prioridade:['Alta', 'Baixa', 'Média'],
       categoria:['Suporte', 'Financeiro', 'Comercial'].
    """
    with get_db() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO Chamados (cliente_id, data_abertura, status, prioridade, categoria, descricao)
                VALUES (?, datetime('now'), 'Aberto', ?, ?, ?)
            """,
                (
                    chamado.cliente_id,
                    chamado.prioridade,
                    chamado.categoria,
                    chamado.descricao,
                ),
            )
            conn.commit()
            chamado_id = cursor.lastrowid
            novo_chamado = cursor.execute(
                'SELECT * FROM Chamados WHERE chamado_id = ?', (chamado_id,)
            ).fetchone()
        except sqlite3.IntegrityError:
            raise HTTPException(
                status_code=400, detail='Erro ao criar chamado'
            )
    return dict(novo_chamado)


@app.get('/suporte/chamados/', response_model=List[Chamado])
def read_chamados(
    status: Optional[str] = None, categoria: Optional[str] = None
):
    """Lista chamados de suporte."""
    """Opção de filtrar por status:['Aberto', 'Em Andamento', 'Fechado']
      e categoria: ['Suporte', 'Financeiro', 'Comercial']."""
    with get_db() as conn:
        cursor = conn.cursor()
        query = 'SELECT * FROM Chamados WHERE 1=1'
        params = []
        if status:
            query += ' AND status = ?'
            params.append(status)
        if categoria:
            query += ' AND categoria = ?'
            params.append(categoria)
        query += ' ORDER BY data_abertura DESC'
        chamados = cursor.execute(query, params).fetchall()
    return [dict(chamado) for chamado in chamados]


@app.put('/suporte/chamados/{chamado_id}', response_model=Chamado)
def update_chamado(
    chamado_id: int,
    status: Optional[str] = None,
    resolucao: Optional[str] = None,
):
    """Atualiza o status e/ou resolução de um chamado."""
    """Necessário informar:
    id do chamado;
    Status para alterar:['Aberto', 'Em Andamento', 'Fechado']
    Resolução: Informar um resumo.
    """
    with get_db() as conn:
        cursor = conn.cursor()
        update_fields = []
        params = []
        if status:
            update_fields.append('status = ?')
            params.append(status)
        if resolucao:
            update_fields.append('resolucao = ?')
            params.append(resolucao)
        if status == 'Fechado':
            update_fields.append("data_fechamento = datetime('now')")

        if not update_fields:
            raise HTTPException(
                status_code=400, detail='Nenhum campo para atualizar'
            )

        query = f"UPDATE Chamados SET {', '.join(update_fields)} WHERE chamado_id = ?"
        params.append(chamado_id)
        cursor.execute(query, params)
        conn.commit()

        chamado_atualizado = cursor.execute(
            'SELECT * FROM Chamados WHERE chamado_id = ?', (chamado_id,)
        ).fetchone()

    if chamado_atualizado is None:
        raise HTTPException(status_code=404, detail='Chamado não encontrado')
    return dict(chamado_atualizado)


# Rotas para Financeiro
@app.get('/financeiro/faturas/{cliente_id}')
def get_faturas_cliente(cliente_id: int, status: Optional[str] = None):
    """Lista todas as faturas de um cliente."""
    """Opção de filtrar por status:['Paga', 'Atrasada']."""
    with get_db() as conn:
        cursor = conn.cursor()
        query = """
            SELECT f.* FROM Faturas f
            JOIN Contratos c ON f.contrato_id = c.contrato_id
            WHERE c.cliente_id = ?
        """
        params = [cliente_id]
        if status:
            query += ' AND f.status = ?'
            params.append(status)
        query += ' ORDER BY f.data_vencimento DESC'
        faturas = cursor.execute(query, params).fetchall()

    if not faturas:
        raise HTTPException(
            status_code=404,
            detail='Nenhuma fatura encontrada para este cliente',
        )
    return [dict(fatura) for fatura in faturas]


@app.get('/financeiro/fatura/{cliente_id}')
def obter_boleto(cliente_id: int):
    """Obtém a última fatura de um cliente."""
    with get_db() as conn:
        cursor = conn.cursor()
        fatura = conn.execute(
            """SELECT f.* FROM Faturas f
            JOIN Contratos c ON f.contrato_id = c.contrato_id
            WHERE c.cliente_id = ?
            ORDER BY f.data_vencimento DESC
            LIMIT 1;""",
            (cliente_id,),
        ).fetchone()

        if not fatura:
            raise HTTPException(
                status_code=404,
                detail='Nenhuma fatura encontrada para este cliente',
            )
        return dict(fatura)


@app.post('/financeiro/pagamentos/')
def registrar_pagamento(
    fatura_id: int, valor_pago: float, forma_pagamento: str
):
    """Registra o pagamento de uma fatura."""
    """Forma de pagamento:['Boleto', 'Crédito', 'PIX', 'Outros']"""
    with get_db() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO Pagamentos (fatura_id, data_pagamento, valor_pago, forma_pagamento)
                VALUES (?, DATE('now'), ?, ?)
            """,
                (fatura_id, valor_pago, forma_pagamento),
            )

            cursor.execute(
                "UPDATE Faturas SET status = 'Paga' WHERE fatura_id = ?",
                (fatura_id,),
            )
            conn.commit()
        except sqlite3.IntegrityError:
            raise HTTPException(
                status_code=400, detail='Erro ao registrar pagamento'
            )

    return {'message': 'Pagamento registrado com sucesso'}


@app.post(
    '/financeiro/gerar-boleto/{cliente_id}', response_model=BoletoResponse
)
def gerar_boleto_cliente(cliente_id: int):
    """Gera um boleto para a última fatura do cliente e atualiza a data do vencimento, apenas se o cliente tiver fatura em aberto."""
    """Caso contrário retora que a fatura não foi encontrada."""
    with get_db() as conn:
        cursor = conn.cursor()
        fatura = conn.execute(
            """SELECT f.* FROM Faturas f
            JOIN Contratos c ON f.contrato_id = c.contrato_id
            WHERE c.cliente_id = ? AND f.status != 'Paga'
            ORDER BY f.data_vencimento DESC
            LIMIT 1;""",
            (cliente_id,),
        ).fetchone()

        if fatura is None:
            raise HTTPException(
                status_code=404, detail='Fatura não encontrada'
            )

        boleto_cod = gerar_codigo_boleto()
        fatura_id = fatura['fatura_id']
        data_form = datetime.now()
        data_emis = data_form.strftime('%Y-%m-%d')
        data_venc = (data_form + timedelta(days=5)).strftime('%Y-%m-%d')

        cursor.execute(
            """
            UPDATE Faturas
            SET boleto = ?,
            data_emissao = ?,
            data_vencimento = ?
            WHERE fatura_id = ?
        """,
            (boleto_cod, data_emis, data_venc, fatura_id),
        )
        conn.commit()

        return BoletoResponse(
            boleto_cod=boleto_cod, vencimento=data_venc, valor=fatura['valor']
        )


# Rotas para Comercial
@app.post('/comercial/upgrade-plano/{cliente_id}')
def upgrade_plano(cliente_id: int, novo_plano_id: int):
    """Realiza o upgrade do último plano ativo para um cliente."""
    with get_db() as conn:
        cursor = conn.cursor()
        contrato_ativo = cursor.execute(
            """
            SELECT contrato_id FROM Contratos
            WHERE cliente_id = ? AND status = 'Ativo'
            ORDER BY data_inicio DESC LIMIT 1
        """,
            (cliente_id,),
        ).fetchone()

        try:
            if contrato_ativo:
                cursor.execute(
                    """
                    UPDATE Contratos
                    SET plano_id = ?, data_inicio = DATE('now')
                    WHERE contrato_id = ?
                """,
                    (novo_plano_id, contrato_ativo['contrato_id']),
                )
            else:
                cursor.execute(
                    """
                    INSERT INTO Contratos (cliente_id, plano_id, data_inicio, status, tipo_servico)
                    VALUES (?, ?, DATE('now'), 'Ativo', 'Internet')
                """,
                    (cliente_id, novo_plano_id),
                )
            conn.commit()
        except sqlite3.IntegrityError:
            raise HTTPException(
                status_code=400, detail='Erro ao atualizar plano'
            )

    return {'message': 'Plano atualizado com sucesso'}


@app.post('/comercial/novo-contrato/{cliente_id}')
def novo_contrato(cliente_id: int, plano_id: int, tipo_servico: str):
    """Cria um novo contrato para um cliente."""
    """Formatos:
            cliente_id: int
            plano_id: int
            tipo_serviço: ['Combo', 'Internet']
    """
    with get_db() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO Contratos (cliente_id, plano_id, data_inicio, status, tipo_servico)
                VALUES (?, ?, DATE('now'), 'Ativo', ?)
            """,
                (cliente_id, plano_id, tipo_servico),
            )
            conn.commit()
        except sqlite3.IntegrityError:
            raise HTTPException(
                status_code=400, detail='Erro ao criar novo contrato'
            )

    return {'message': 'Novo contrato criado com sucesso'}


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host='0.0.0.0', port=8000)
