-- CONSULTAS SQL PARA O MARKETPLACE DATABASE
-- Execute essas consultas para testar e analisar os dados

-- =============================================
-- 1. CONSULTAS BÁSICAS DE LISTAGEM
-- =============================================

-- 1.1 Listar todos os produtos com seus vendedores
SELECT 
    p.Nome AS Produto,
    p.Preco,
    p.Estoque,
    v.Nome_Loja AS Vendedor,
    u.Nome AS Nome_Vendedor
FROM Produto p
JOIN Vendedor v ON p.ID_Vendedor = v.ID_Usuario
JOIN Usuario u ON v.ID_Usuario = u.ID_Usuario
ORDER BY p.Preco DESC;

-- 1.2 Produtos por categoria
SELECT 
    c.Nome AS Categoria,
    p.Nome AS Produto,
    p.Preco,
    v.Nome_Loja AS Vendedor
FROM Categoria c
JOIN Produto_Categoria pc ON c.ID_Categoria = pc.ID_Categoria
JOIN Produto p ON pc.ID_Produto = p.ID_Produto
JOIN Vendedor v ON p.ID_Vendedor = v.ID_Usuario
ORDER BY c.Nome, p.Preco;

-- =============================================
-- 2. ANÁLISE DE VENDAS E FATURAMENTO
-- =============================================

-- 2.1 Faturamento por vendedor
SELECT 
    v.Nome_Loja AS Loja,
    u.Nome AS Vendedor,
    COUNT(DISTINCT ped.ID_Pedido) AS Total_Pedidos,
    SUM(idp.Quantidade * idp.PrecoNaCompra) AS Faturamento_Total,
    AVG(idp.PrecoNaCompra) AS Ticket_Medio
FROM Vendedor v
JOIN Usuario u ON v.ID_Usuario = u.ID_Usuario
JOIN Produto p ON v.ID_Usuario = p.ID_Vendedor
JOIN ItemDoPedido idp ON p.ID_Produto = idp.ID_Produto
JOIN Pedido ped ON idp.ID_Pedido = ped.ID_Pedido
WHERE ped.Status = 'entregue'
GROUP BY v.ID_Usuario, v.Nome_Loja, u.Nome
ORDER BY Faturamento_Total DESC;

-- 2.2 Produtos mais vendidos
SELECT 
    p.Nome AS Produto,
    v.Nome_Loja AS Vendedor,
    SUM(idp.Quantidade) AS Quantidade_Vendida,
    SUM(idp.Quantidade * idp.PrecoNaCompra) AS Receita_Total,
    COUNT(DISTINCT idp.ID_Pedido) AS Numero_Pedidos
FROM Produto p
JOIN ItemDoPedido idp ON p.ID_Produto = idp.ID_Produto
JOIN Pedido ped ON idp.ID_Pedido = ped.ID_Pedido
JOIN Vendedor v ON p.ID_Vendedor = v.ID_Usuario
WHERE ped.Status = 'entregue'
GROUP BY p.ID_Produto, p.Nome, v.Nome_Loja
ORDER BY Quantidade_Vendida DESC;

-- 2.3 Vendas por mês
SELECT 
    EXTRACT(YEAR FROM ped.Data) AS Ano,
    EXTRACT(MONTH FROM ped.Data) AS Mes,
    COUNT(DISTINCT ped.ID_Pedido) AS Total_Pedidos,
    SUM(idp.Quantidade * idp.PrecoNaCompra) AS Faturamento_Mensal
FROM Pedido ped
JOIN ItemDoPedido idp ON ped.ID_Pedido = idp.ID_Pedido
WHERE ped.Status = 'entregue'
GROUP BY EXTRACT(YEAR FROM ped.Data), EXTRACT(MONTH FROM ped.Data)
ORDER BY Ano, Mes;

-- =============================================
-- 3. ANÁLISE DE CLIENTES
-- =============================================

-- 3.1 Compradores que mais gastaram
SELECT 
    u.Nome AS Comprador,
    c.CPF,
    COUNT(DISTINCT ped.ID_Pedido) AS Total_Pedidos,
    SUM(pag.Valor) AS Valor_Total_Gasto,
    AVG(pag.Valor) AS Ticket_Medio
FROM Usuario u
JOIN Comprador c ON u.ID_Usuario = c.ID_Usuario
JOIN Pedido ped ON c.ID_Usuario = ped.ID_Comprador
JOIN Pagamento pag ON ped.ID_Pagamento = pag.ID_Pagamento
WHERE ped.Status = 'entregue'
GROUP BY u.ID_Usuario, u.Nome, c.CPF
ORDER BY Valor_Total_Gasto DESC;

-- 3.2 Clientes por estado
SELECT 
    e.Estado,
    e.Cidade,
    COUNT(DISTINCT c.ID_Usuario) AS Total_Clientes,
    COUNT(DISTINCT ped.ID_Pedido) AS Total_Pedidos
FROM Endereco e
JOIN Comprador c ON e.ID_Comprador = c.ID_Usuario
LEFT JOIN Pedido ped ON c.ID_Usuario = ped.ID_Comprador
GROUP BY e.Estado, e.Cidade
ORDER BY Total_Clientes DESC;

-- =============================================
-- 4. ANÁLISE DE PAGAMENTOS
-- =============================================

-- 4.1 Métodos de pagamento mais utilizados
SELECT 
    pag.Metodo_Pagamento,
    COUNT(*) AS Total_Transacoes,
    SUM(pag.Valor) AS Valor_Total,
    AVG(pag.Valor) AS Valor_Medio,
    COUNT(CASE WHEN pag.Status = 'aprovado' THEN 1 END) AS Aprovados,
    COUNT(CASE WHEN pag.Status = 'pendente' THEN 1 END) AS Pendentes
FROM Pagamento pag
GROUP BY pag.Metodo_Pagamento
ORDER BY Total_Transacoes DESC;

-- 4.2 Análise de cartões por bandeira
SELECT 
    cart.Bandeira,
    COUNT(*) AS Total_Cartoes,
    COUNT(DISTINCT pc.ID_Pagamento) AS Transacoes_Realizadas,
    SUM(pag.Valor) AS Valor_Total_Transacionado
FROM Cartao cart
LEFT JOIN PagamentoCartao pc ON cart.ID_Cartao = pc.ID_Cartao
LEFT JOIN Pagamento pag ON pc.ID_Pagamento = pag.ID_Pagamento
GROUP BY cart.Bandeira
ORDER BY Total_Cartoes DESC;

-- =============================================
-- 5. ANÁLISE DE AVALIAÇÕES
-- =============================================

-- 5.1 Produtos com melhor avaliação
SELECT 
    p.Nome AS Produto,
    v.Nome_Loja AS Vendedor,
    COUNT(a.ID_Avaliacao) AS Total_Avaliacoes,
    AVG(a.Nota) AS Media_Notas,
    MAX(a.Nota) AS Melhor_Nota,
    MIN(a.Nota) AS Pior_Nota
FROM Produto p
JOIN Vendedor v ON p.ID_Vendedor = v.ID_Usuario
JOIN ItemDoPedido idp ON p.ID_Produto = idp.ID_Produto
JOIN Avaliacao a ON idp.ID_Pedido = a.ID_Pedido
GROUP BY p.ID_Produto, p.Nome, v.Nome_Loja
HAVING COUNT(a.ID_Avaliacao) > 0
ORDER BY Media_Notas DESC, Total_Avaliacoes DESC;

-- 5.2 Avaliações por período
SELECT 
    EXTRACT(YEAR FROM a.Data) AS Ano,
    EXTRACT(MONTH FROM a.Data) AS Mes,
    COUNT(*) AS Total_Avaliacoes,
    AVG(a.Nota) AS Media_Notas,
    COUNT(CASE WHEN a.Nota >= 4 THEN 1 END) AS Avaliacoes_Positivas,
    COUNT(CASE WHEN a.Nota <= 2 THEN 1 END) AS Avaliacoes_Negativas
FROM Avaliacao a
GROUP BY EXTRACT(YEAR FROM a.Data), EXTRACT(MONTH FROM a.Data)
ORDER BY Ano, Mes;

-- =============================================
-- 6. CONSULTAS COMPLEXAS COM MÚLTIPLAS TABELAS
-- =============================================

-- 6.1 Relatório completo de pedidos
SELECT 
    ped.ID_Pedido,
    ped.Data AS Data_Pedido,
    ped.Status,
    comp.Nome AS Comprador,
    comp_usuario.Email AS Email_Comprador,
    STRING_AGG(prod.Nome, ', ') AS Produtos,
    SUM(idp.Quantidade) AS Total_Itens,
    pag.Valor AS Valor_Total,
    pag.Metodo_Pagamento,
    pag.Status AS Status_Pagamento,
    CONCAT(end.Rua, ', ', end.Numero, ' - ', end.Cidade, '/', end.Estado) AS Endereco_Entrega
FROM Pedido ped
JOIN Comprador comp_table ON ped.ID_Comprador = comp_table.ID_Usuario
JOIN Usuario comp ON comp_table.ID_Usuario = comp.ID_Usuario
JOIN Usuario comp_usuario ON comp_table.ID_Usuario = comp_usuario.ID_Usuario
JOIN ItemDoPedido idp ON ped.ID_Pedido = idp.ID_Pedido
JOIN Produto prod ON idp.ID_Produto = prod.ID_Produto
JOIN Pagamento pag ON ped.ID_Pagamento = pag.ID_Pagamento
JOIN Endereco end ON ped.ID_Endereco = end.ID_Endereco
GROUP BY ped.ID_Pedido, ped.Data, ped.Status, comp.Nome, comp_usuario.Email, 
         pag.Valor, pag.Metodo_Pagamento, pag.Status, end.Rua, end.Numero, 
         end.Cidade, end.Estado
ORDER BY ped.Data DESC;

-- 6.2 Produtos sem vendas
SELECT 
    p.Nome AS Produto,
    p.Preco,
    p.Estoque,
    v.Nome_Loja AS Vendedor,
    c.Nome AS Categoria
FROM Produto p
JOIN Vendedor v ON p.ID_Vendedor = v.ID_Usuario
LEFT JOIN ItemDoPedido idp ON p.ID_Produto = idp.ID_Produto
JOIN Produto_Categoria pc ON p.ID_Produto = pc.ID_Produto
JOIN Categoria c ON pc.ID_Categoria = c.ID_Categoria
WHERE idp.ID_Produto IS NULL
ORDER BY p.Preco DESC;

-- =============================================
-- 7. CONSULTAS DE PERFORMANCE E INSIGHTS
-- =============================================

-- 7.1 Taxa de conversão por vendedor (pedidos entregues vs total)
SELECT 
    v.Nome_Loja,
    COUNT(DISTINCT ped.ID_Pedido) AS Total_Pedidos,
    COUNT(DISTINCT CASE WHEN ped.Status = 'entregue' THEN ped.ID_Pedido END) AS Pedidos_Entregues,
    ROUND(
        (COUNT(DISTINCT CASE WHEN ped.Status = 'entregue' THEN ped.ID_Pedido END) * 100.0 / 
         COUNT(DISTINCT ped.ID_Pedido)), 2
    ) AS Taxa_Entrega_Percent
FROM Vendedor v
JOIN Produto p ON v.ID_Usuario = p.ID_Vendedor
JOIN ItemDoPedido idp ON p.ID_Produto = idp.ID_Produto
JOIN Pedido ped ON idp.ID_Pedido = ped.ID_Pedido
GROUP BY v.ID_Usuario, v.Nome_Loja
ORDER BY Taxa_Entrega_Percent DESC;

-- 7.2 Estoque crítico (produtos com estoque baixo)
SELECT 
    p.Nome AS Produto,
    p.Estoque,
    p.Preco,
    v.Nome_Loja AS Vendedor,
    COALESCE(SUM(idp.Quantidade), 0) AS Total_Vendido,
    CASE 
        WHEN p.Estoque <= 10 THEN 'CRÍTICO'
        WHEN p.Estoque <= 30 THEN 'BAIXO'
        ELSE 'OK'
    END AS Status_Estoque
FROM Produto p
JOIN Vendedor v ON p.ID_Vendedor = v.ID_Usuario
LEFT JOIN ItemDoPedido idp ON p.ID_Produto = idp.ID_Produto
LEFT JOIN Pedido ped ON idp.ID_Pedido = ped.ID_Pedido AND ped.Status = 'entregue'
GROUP BY p.ID_Produto, p.Nome, p.Estoque, p.Preco, v.Nome_Loja
ORDER BY p.Estoque ASC, Total_Vendido DESC;
