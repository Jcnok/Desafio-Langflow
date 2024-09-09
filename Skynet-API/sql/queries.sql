-- Listar todas as faturas pendentes
SELECT f.fatura_id, c.nome, f.data_emissao, f.data_vencimento, f.valor, f.status
FROM Faturas f
JOIN Contratos ct ON f.contrato_id = ct.contrato_id
JOIN Clientes c ON ct.cliente_id = c.cliente_id
WHERE f.status = 'Atrasada';

-- Verificar o histórico de pagamentos de um cliente específico
SELECT f.fatura_id, f.data_emissao, f.data_vencimento, f.valor, f.status, 
       p.data_pagamento, p.valor_pago, p.forma_pagamento
FROM Faturas f
LEFT JOIN Pagamentos p ON f.fatura_id = p.fatura_id
JOIN Contratos ct ON f.contrato_id = ct.contrato_id
WHERE ct.cliente_id = 17;

-- Calcular o total de receitas de um mês específico
SELECT strftime('%Y-%m', p.data_pagamento) AS mes, SUM(p.valor_pago) AS receita_total
FROM Pagamentos p
WHERE p.data_pagamento BETWEEN '2024-03-01' AND '2024-03-31'
GROUP BY mes;

-- Identificar clientes com pagamentos atrasados
SELECT DISTINCT c.cliente_id, c.nome, c.email, f.data_vencimento
FROM Clientes c
JOIN Contratos ct ON c.cliente_id = ct.cliente_id
JOIN Faturas f ON ct.contrato_id = f.contrato_id
WHERE f.status = 'Atrasada';

-- Relatório de faturas pagas e pendentes por mês
SELECT strftime('%Y-%m', f.data_emissao) AS mes,
       SUM(CASE WHEN f.status = 'Paga' THEN 1 ELSE 0 END) AS faturas_pagas,
       SUM(CASE WHEN f.status = 'Atrasada' THEN 1 ELSE 0 END) AS faturas_pendentes
FROM Faturas f
GROUP BY mes;

-- Listar todos os chamados abertos
SELECT chamado_id, cliente_id, data_abertura, status, prioridade, categoria, descricao
FROM Chamados
WHERE status = 'Aberto';

-- Verificar histórico de atendimento de um cliente específico
SELECT ha.historico_id, ha.chamado_id, a.nome AS atendente, ha.data_atendimento, ha.descricao
FROM Historico_Atendimento ha
JOIN Atendentes a ON ha.atendente_id = a.atendente_id
JOIN Chamados ch ON ha.chamado_id = ch.chamado_id
WHERE ch.cliente_id = 1;

-- Obter o número de chamados por categoria e prioridade
SELECT categoria, prioridade, COUNT(*) AS numero_chamados
FROM Chamados
GROUP BY categoria, prioridade;

-- Identificar atendentes mais ativos no mês atual
SELECT a.atendente_id, a.nome, COUNT(ha.historico_id) AS atendimentos
FROM Atendentes a
JOIN Historico_Atendimento ha ON a.atendente_id = ha.atendente_id
WHERE strftime('%Y-%m', ha.data_atendimento) = strftime('%Y-%m', 'now')
GROUP BY a.atendente_id
ORDER BY atendimentos DESC;

-- Monitorar a taxa de resolução no primeiro contato
SELECT COUNT(*) AS total_chamados, 
       SUM(CASE WHEN ha.historico_id IS NOT NULL THEN 1 ELSE 0 END) AS resolvidos_primeiro_contato
FROM Chamados c
LEFT JOIN (SELECT chamado_id, MIN(historico_id) AS historico_id FROM Historico_Atendimento GROUP BY chamado_id) ha
ON c.chamado_id = ha.chamado_id
WHERE c.status = 'Fechado';

-- Listar clientes que solicitaram upgrade de plano
SELECT c.cliente_id, c.nome, c.email, ch.descricao, ch.data_abertura
FROM Clientes c
JOIN Chamados ch ON c.cliente_id = ch.cliente_id
WHERE ch.categoria = 'Comercial' AND ch.descricao LIKE '%upgrade%';

-- Obter o número de novos contratos por mês
SELECT strftime('%Y-%m', data_inicio) AS mes, COUNT(*) AS novos_contratos
FROM Contratos
WHERE status = 'Ativo'
GROUP BY mes;

-- Identificar planos mais vendidos
SELECT p.nome, COUNT(*) AS quantidade_vendida
FROM Planos p
JOIN Contratos ct ON p.plano_id = ct.plano_id
GROUP BY p.nome
ORDER BY quantidade_vendida DESC;

-- Analisar taxa de cancelamento de contratos por motivo
SELECT status, COUNT(*) AS total_cancelamentos
FROM Contratos
WHERE status = 'Inativo'
GROUP BY status
ORDER BY total_cancelamentos DESC;

-- Identificar clientes em potencial para upsell
SELECT c.cliente_id, c.nome, c.email, p.nome AS plano_atual
FROM Clientes c
JOIN Contratos ct ON c.cliente_id = ct.cliente_id
JOIN Planos p ON ct.plano_id = p.plano_id
WHERE p.nome = 'Básico' AND ct.status = 'Ativo';

-- 



