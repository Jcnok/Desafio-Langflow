"""Gerar dados fictícios para alimentar o banco de dados de forma estruturada."""
import csv
import random
from datetime import datetime, timedelta

from faker import Faker

atendimento_situacoes = {
    'Suporte': [
        {
            'descricao': 'Cliente relata lentidão na conexão',
            'historico_texto': 'Realizado teste de velocidade e orientado a reiniciar o roteador',
            'resolucao': 'Problema resolvido após reinicialização do equipamento',
        },
        {
            'descricao': 'Sem conexão à internet',
            'historico_texto': 'Verificado status do sinal e realizado diagnóstico remoto',
            'resolucao': 'Identificado problema na fibra, agendada visita técnica',
        },
        {
            'descricao': 'Dificuldade em configurar roteador Wi-Fi',
            'historico_texto': 'Fornecidas instruções passo a passo para configuração',
            'resolucao': 'Cliente conseguiu configurar o roteador com sucesso',
        },
        {
            'descricao': 'Reclamação de instabilidade na conexão',
            'historico_texto': 'Analisado histórico de conexão e identificados picos de uso',
            'resolucao': 'Recomendada atualização do plano para melhor estabilidade',
        },
        {
            'descricao': 'Solicitação de suporte para instalação de câmeras IP',
            'historico_texto': 'Explicado processo de configuração e redirecionamento de portas',
            'resolucao': 'Cliente conseguiu configurar as câmeras com o suporte fornecido',
        },
        {
            'descricao': 'Problemas com e-mail corporativo',
            'historico_texto': 'Verificadas configurações de SMTP e IMAP no cliente de e-mail',
            'resolucao': 'Corrigidas configurações e e-mail funcionando normalmente',
        },
        {
            'descricao': 'Lentidão em serviços de streaming',
            'historico_texto': 'Realizado teste de velocidade e verificada qualidade do sinal',
            'resolucao': 'Identificada interferência Wi-Fi, recomendada mudança de canal',
        },
        {
            'descricao': 'Dúvidas sobre segurança da rede',
            'historico_texto': 'Explicadas medidas de segurança e recomendado uso de VPN',
            'resolucao': 'Cliente orientado sobre melhores práticas de segurança',
        },
        {
            'descricao': 'Solicitação de aumento temporário de velocidade',
            'historico_texto': 'Verificada disponibilidade técnica para upgrade',
            'resolucao': 'Realizado upgrade temporário conforme solicitação do cliente',
        },
        {
            'descricao': 'Problemas de conexão em jogos online',
            'historico_texto': 'Analisada latência e perda de pacotes',
            'resolucao': 'Ajustadas configurações de QoS no roteador do cliente',
        },
    ],
    'Financeiro': [
        {
            'descricao': 'Dúvidas sobre fatura mensal',
            'historico_texto': 'Explicado detalhamento dos serviços cobrados',
            'resolucao': 'Cliente compreendeu a fatura e confirmou o pagamento',
        },
        {
            'descricao': 'Solicitação de alteração de data de vencimento',
            'historico_texto': 'Verificadas opções de datas disponíveis',
            'resolucao': 'Alterada data de vencimento conforme solicitação do cliente',
        },
        {
            'descricao': 'Contestação de valor na fatura',
            'historico_texto': 'Analisado histórico de consumo e serviços contratados',
            'resolucao': 'Identificado erro de cobrança, emitida nova fatura corrigida',
        },
        {
            'descricao': 'Solicitação de parcelamento de débitos',
            'historico_texto': 'Apresentadas opções de parcelamento disponíveis',
            'resolucao': 'Realizado parcelamento em 3x sem juros conforme acordo',
        },
        {
            'descricao': 'Informações sobre métodos de pagamento',
            'historico_texto': 'Explicadas opções de pagamento: boleto, cartão e débito automático',
            'resolucao': 'Cliente optou por aderir ao débito automático',
        },
        {
            'descricao': 'Dúvidas sobre desconto de pontualidade',
            'historico_texto': 'Esclarecidas regras do programa de desconto por pagamento em dia',
            'resolucao': 'Cliente entendeu o funcionamento e decidiu manter pagamentos em dia',
        },
        {
            'descricao': 'Solicitação de segunda via de fatura',
            'historico_texto': 'Verificado sistema de faturamento e gerada segunda via',
            'resolucao': 'Enviada segunda via por e-mail conforme solicitação',
        },
        {
            'descricao': 'Informações sobre multa e juros por atraso',
            'historico_texto': 'Explicada política de cobrança de multas e juros',
            'resolucao': 'Cliente informado e orientado sobre prazos de pagamento',
        },
        {
            'descricao': 'Dúvidas sobre cobrança pro-rata na instalação',
            'historico_texto': 'Detalhado cálculo pro-rata para o primeiro mês de serviço',
            'resolucao': 'Cliente compreendeu o cálculo e aceitou os valores',
        },
        {
            'descricao': 'Solicitação de nota fiscal',
            'historico_texto': 'Verificado status de emissão da nota fiscal',
            'resolucao': 'Nota fiscal emitida e enviada por e-mail ao cliente',
        },
    ],
    'Comercial': [
        {
            'descricao': 'Interesse em upgrade de plano',
            'historico_texto': 'Apresentadas opções de planos superiores e seus benefícios',
            'resolucao': 'Cliente decidiu fazer upgrade para o plano 100Mbps',
        },
        {
            'descricao': 'Solicitação de informações sobre planos empresariais',
            'historico_texto': 'Explicadas opções de planos dedicados e suas vantagens',
            'resolucao': 'Agendada visita técnica para avaliação das necessidades da empresa',
        },
        {
            'descricao': 'Dúvidas sobre pacote combo (internet + TV)',
            'historico_texto': 'Detalhados canais inclusos e vantagens do combo',
            'resolucao': 'Cliente aderiu ao pacote combo com desconto promocional',
        },
        {
            'descricao': 'Interesse em serviços de cloud para empresa',
            'historico_texto': 'Apresentadas soluções de cloud computing e backup',
            'resolucao': 'Cliente solicitou proposta detalhada para avaliação interna',
        },
        {
            'descricao': 'Informações sobre cobertura em nova localidade',
            'historico_texto': 'Verificada disponibilidade de serviço no endereço informado',
            'resolucao': 'Confirmada cobertura e agendada instalação para nova localidade',
        },
        {
            'descricao': 'Solicitação de cancelamento de serviço',
            'historico_texto': 'Investigados motivos e oferecidas alternativas para retenção',
            'resolucao': 'Cliente decidiu permanecer após oferta de upgrade sem custo adicional',
        },
        {
            'descricao': 'Dúvidas sobre fidelidade contratual',
            'historico_texto': 'Explicadas condições de fidelidade e multa por quebra de contrato',
            'resolucao': 'Cliente compreendeu os termos e decidiu manter o contrato',
        },
        {
            'descricao': 'Interesse em serviço de IP fixo',
            'historico_texto': 'Apresentados benefícios e custos adicionais do IP fixo',
            'resolucao': 'Cliente contratou serviço de IP fixo para sua empresa',
        },
        {
            'descricao': 'Solicitação de proposta para condomínio',
            'historico_texto': 'Coletadas informações sobre o condomínio e suas necessidades',
            'resolucao': 'Elaborada proposta personalizada e agendada apresentação',
        },
        {
            'descricao': 'Dúvidas sobre prazo de instalação',
            'historico_texto': 'Verificado cronograma de instalações e disponibilidade de equipe',
            'resolucao': 'Informado prazo de 5 dias úteis e agendada data com o cliente',
        },
    ],
}

# Configuração do Faker
fake = Faker('pt_BR')

# Definir a data atual como 2024-09-03
current_date = datetime(2024, 9, 3)

# Mapeamento de DDD para Estado e Cidade
ddd_mapping = {
    '11': ('SP', 'São Paulo'),
    '21': ('RJ', 'Rio de Janeiro'),
    '31': ('MG', 'Belo Horizonte'),
    '41': ('PR', 'Curitiba'),
    '51': ('RS', 'Porto Alegre'),
    '61': ('DF', 'Brasília'),
    '71': ('BA', 'Salvador'),
    '81': ('PE', 'Recife'),
    '91': ('PA', 'Belém'),
}

# Função para gerar um número de telefone com DDD válido
def generate_phone(ddd):
    """Gerador de telefones."""
    return f'{ddd}9{fake.msisdn()[5:]}'


# Função para gerar um endereço baseado no DDD
def generate_address(ddd):
    """Gera endereçõ basado no ddd."""
    state, city = ddd_mapping[ddd]
    return f'{fake.street_address()}, {city}, {state}, {fake.postcode()}'


# Função para gerar um email com base no nome e sobrenome
def generate_email(name):
    """Gera email com base no nome e sobrenome."""
    first_name, last_name = name.split(' ', 1)
    username = f"{first_name.lower()}.{last_name.lower().replace(' ', '')}"
    return f'{username}@Skynet.com'


# Gerar dados para a tabela Clientes
def generate_clients(num_clients):
    """Gera dados para tabela clientes."""
    clients = []
    for _ in range(num_clients):
        name = fake.name()
        ddd = random.choice(list(ddd_mapping.keys()))
        client = {
            'cliente_id': _ + 1,
            'cpf': fake.cpf(),
            'nome': name,
            'email': generate_email(name),
            'telefone': generate_phone(ddd),
            'endereco': generate_address(ddd),
            'data_cadastro': fake.date_between(
                start_date=current_date - timedelta(days=2 * 365),
                end_date=current_date,
            ).strftime('%Y-%m-%d'),
        }
        clients.append(client)
    return clients


# Gerar dados para a tabela Planos
def generate_plans():
    """Gera dados para tabela planos."""
    plans = [
        {
            'plano_id': 1,
            'nome': 'Básico',
            'descricao': 'Plano de internet',
            'velocidade': '100 Mbps',
            'preco': 49.99,
            'tipo': 'Residencial',
        },
        {
            'plano_id': 2,
            'nome': 'Padrão',
            'descricao': 'Combo(internet + tv)',
            'velocidade': '200 Mbps',
            'preco': 79.99,
            'tipo': 'Residencial',
        },
        {
            'plano_id': 3,
            'nome': 'Premium',
            'descricao': 'Combo(internet + tv + mobile)',
            'velocidade': '300 Mbps',
            'preco': 119.99,
            'tipo': 'Residencial',
        },
        {
            'plano_id': 4,
            'nome': 'Gold',
            'descricao': 'Combo(internet + tv + mobile)',
            'velocidade': '500 Mbps',
            'preco': 199.99,
            'tipo': 'Residencial',
        },
        {
            'plano_id': 5,
            'nome': 'Empresarial',
            'descricao': 'Plano para empresas',
            'velocidade': '1 Gbps',
            'preco': 499.99,
            'tipo': 'Empresarial',
        },
    ]
    return plans


# Gerar dados para a tabela Chamados
def generate_tickets(num_tickets, clients):
    """Gera dados para tabela chamados."""
    tickets = []
    for i in range(num_tickets):
        client = random.choice(clients)
        open_date = datetime.strptime(
            client['data_cadastro'], '%Y-%m-%d'
        ) + timedelta(days=random.randint(1, 365))
        if open_date > current_date:
            open_date = current_date
        categoria = random.choice(['Suporte', 'Financeiro', 'Comercial'])
        situacao = random.choice(atendimento_situacoes[categoria])
        ticket = {
            'chamado_id': i + 1,
            'cliente_id': client['cliente_id'],
            'data_abertura': open_date.strftime('%Y-%m-%d'),
            'data_fechamento': (
                open_date + timedelta(days=random.randint(1, 7))
            ).strftime('%Y-%m-%d')
            if random.random() < 0.8
            else None,
            'status': random.choice(['Aberto', 'Em Andamento', 'Fechado']),
            'prioridade': random.choice(['Baixa', 'Média', 'Alta']),
            'categoria': categoria,
            'descricao': situacao['descricao'],
            'resolucao': situacao['resolucao']
            if random.random() < 0.8
            else None,
        }
        tickets.append(ticket)
    return tickets


# Gerar históricos
def generate_service_history(tickets, attendants):
    """Gera dados para histórico."""
    history = []
    for ticket in tickets:
        service_date = ticket['data_abertura']
        categoria = ticket['categoria']
        situacao = next(
            s
            for s in atendimento_situacoes[categoria]
            if s['descricao'] == ticket['descricao']
        )

        record = {
            'historico_id': len(history) + 1,
            'chamado_id': ticket['chamado_id'],
            'atendente_id': random.choice(attendants)['atendente_id'],
            'data_atendimento': service_date,
            'descricao': ticket['descricao'],
            'historico_texto': situacao['historico_texto'],
        }
        history.append(record)
    return history


# Gerar dados para a tabela Atendentes
def generate_attendants(num_attendants):
    """Gera dados para atendentes."""
    attendants = []
    for i in range(num_attendants):
        name = fake.name()
        ddd = random.choice(list(ddd_mapping.keys()))
        attendant = {
            'atendente_id': i + 1,
            'nome': name,
            'email': generate_email(name),
            'telefone': generate_phone(ddd),
            'especialidade': random.choice(
                ['Suporte', 'Financeiro', 'Comercial']
            ),
        }
        attendants.append(attendant)
    return attendants


# Função para gerar código dos boletos
def gerar_codigo_boleto():
    """Gera código de boletos."""
    campo1 = f'{random.randint(10000, 99999):05d}'
    campo2 = f'{random.randint(10000, 99999):05d}'
    campo3 = f'{random.randint(10000, 99999):05d}'
    campo4 = f'{random.randint(10000, 99999):05d}'
    campo5 = f'{random.randint(10000, 99999):05d}'
    dv = random.randint(0, 9)
    linha_digitavel = f'23790.{campo1} {campo2}.{campo3} {campo4}.{campo5} {dv} {campo1}{campo2}{campo3}{campo4}{campo5}'
    return linha_digitavel


# Gerar dados para a tabela Contratos
def generate_contracts(clients, plans):
    """Gera dados para contratos."""
    contracts = []
    for client in clients:
        plan = random.choice(plans)
        start_date = datetime.strptime(
            client['data_cadastro'], '%Y-%m-%d'
        ) + timedelta(days=random.randint(1, 30))
        contract = {
            'contrato_id': len(contracts) + 1,
            'cliente_id': client['cliente_id'],
            'plano_id': plan['plano_id'],
            'data_inicio': start_date.strftime('%Y-%m-%d'),
            'data_fim': None,
            'status': 'Ativo',
            'tipo_servico': 'Internet'
            if plan['nome'] == 'Básico'
            else 'Combo',
        }
        contracts.append(contract)
    return contracts


# Gerar dados para a tabela Faturas
def generate_invoices(contracts, plans):
    """Gera dados para faturas."""
    invoices = []
    for contract in contracts:
        plan = next(p for p in plans if p['plano_id'] == contract['plano_id'])
        start_date = datetime.strptime(contract['data_inicio'], '%Y-%m-%d')
        months = (
            (current_date.year - start_date.year) * 12
            + current_date.month
            - start_date.month
        )
        for i in range(months + 1):
            issue_date = start_date + timedelta(days=30 * i)
            if issue_date > current_date:
                break
            is_overdue = False
            current_year = current_date.year
            current_month = current_date.month
            if (
                issue_date.year == current_year
                and issue_date.month >= current_month - 2
            ):
                is_overdue = True

            invoice = {
                'fatura_id': len(invoices) + 1,
                'contrato_id': contract['contrato_id'],
                'boleto': gerar_codigo_boleto(),
                'data_emissao': issue_date.strftime('%Y-%m-%d'),
                'data_vencimento': (issue_date + timedelta(days=10)).strftime(
                    '%Y-%m-%d'
                ),
                'valor': plan['preco'],
                'status': random.choices(
                    ['Paga', 'Atrasada'], weights=[0.5, 0.5]
                )[0]
                if is_overdue
                else 'Paga',
            }
            invoices.append(invoice)
    return invoices


# Gerar dados para a tabela Pagamentos
def generate_payments(invoices):
    """Gera dados para pagamentos."""
    payments = []
    for invoice in invoices:
        if invoice['status'] == 'Paga':
            payment_date = datetime.strptime(
                invoice['data_vencimento'], '%Y-%m-%d'
            ) + timedelta(days=random.randint(-5, 2))
            if payment_date > current_date:
                payment_date = current_date
            payment = {
                'pagamento_id': len(payments) + 1,
                'fatura_id': invoice['fatura_id'],
                'data_pagamento': payment_date.strftime('%Y-%m-%d'),
                'valor_pago': invoice['valor'],
                'forma_pagamento': random.choice(
                    ['Boleto', 'Crédito', 'PIX', 'Outros']
                ),
            }
            payments.append(payment)
    return payments


# Definir quantidades
num_clients = 50
num_tickets = 100
num_attendants = 10

# Gerar dados
clients = generate_clients(num_clients)
plans = generate_plans()
contracts = generate_contracts(clients, plans)
tickets = generate_tickets(num_tickets, clients)
attendants = generate_attendants(num_attendants)
service_history = generate_service_history(tickets, attendants)
invoices = generate_invoices(contracts, plans)
payments = generate_payments(invoices)

# Salvar dados em arquivos CSV
def save_to_csv(data, filename):
    """Salva os dados gerados em arquivos .csv."""
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)


save_to_csv(clients, 'clientes.csv')
save_to_csv(plans, 'planos.csv')
save_to_csv(contracts, 'contratos.csv')
save_to_csv(tickets, 'chamados.csv')
save_to_csv(attendants, 'atendentes.csv')
save_to_csv(service_history, 'historico_atendimento.csv')
save_to_csv(invoices, 'faturas.csv')
save_to_csv(payments, 'pagamentos.csv')

print('Dados gerados e salvos em arquivos CSV.')
