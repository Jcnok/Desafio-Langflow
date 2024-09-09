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