-- Dados de exemplo para o banco de dados do marketplace
-- Execute este arquivo após criar as tabelas com init.sql

-- 1. USUÁRIOS (5 vendedores + 10 compradores)
INSERT INTO Usuario (Nome, Email, Senha, Telefone, Tipo_Usuario) VALUES
-- Vendedores
('João Silva', 'joao.silva@email.com', 'senha123', '11987654321', 'vendedor'),
('Maria Santos', 'maria.santos@email.com', 'senha456', '11876543210', 'vendedor'),
('Pedro Costa', 'pedro.costa@email.com', 'senha789', '11765432109', 'vendedor'),
('Ana Oliveira', 'ana.oliveira@email.com', 'senha012', '11654321098', 'vendedor'),
('Carlos Ferreira', 'carlos.ferreira@email.com', 'senha345', '11543210987', 'vendedor'),
-- Compradores
('Lucas Almeida', 'lucas.almeida@email.com', 'compra123', '11432109876', 'comprador'),
('Juliana Souza', 'juliana.souza@email.com', 'compra456', '11321098765', 'comprador'),
('Rafael Martins', 'rafael.martins@email.com', 'compra789', '11210987654', 'comprador'),
('Amanda Lima', 'amanda.lima@email.com', 'compra012', '11109876543', 'comprador'),
('Bruno Pereira', 'bruno.pereira@email.com', 'compra345', '11098765432', 'comprador'),
('Carla Rodrigues', 'carla.rodrigues@email.com', 'compra678', '11987654320', 'comprador'),
('Diego Nascimento', 'diego.nascimento@email.com', 'compra901', '11876543209', 'comprador'),
('Fernanda Barbosa', 'fernanda.barbosa@email.com', 'compra234', '11765432108', 'comprador'),
('Gabriel Torres', 'gabriel.torres@email.com', 'compra567', '11654321097', 'comprador'),
('Helena Cardoso', 'helena.cardoso@email.com', 'compra890', '11543210986', 'comprador');

-- 2. VENDEDORES
INSERT INTO Vendedor (ID_Usuario, Nome_Loja, CNPJ) VALUES
(1, 'TechStore Brasil', '12.345.678/0001-90'),
(2, 'Moda & Estilo', '23.456.789/0001-01'),
(3, 'Casa & Decoração', '34.567.890/0001-12'),
(4, 'Livraria Cultural', '45.678.901/0001-23'),
(5, 'SportMax', '56.789.012/0001-34');

-- 3. COMPRADORES
INSERT INTO Comprador (ID_Usuario, CPF) VALUES
(6, '123.456.789-01'),
(7, '234.567.890-12'),
(8, '345.678.901-23'),
(9, '456.789.012-34'),
(10, '567.890.123-45'),
(11, '678.901.234-56'),
(12, '789.012.345-67'),
(13, '890.123.456-78'),
(14, '901.234.567-89'),
(15, '012.345.678-90');

-- 4. CATEGORIAS
INSERT INTO Categoria (Nome, Descricao) VALUES
('Eletrônicos', 'Produtos eletrônicos e tecnologia'),
('Roupas Femininas', 'Vestuário e acessórios femininos'),
('Roupas Masculinas', 'Vestuário e acessórios masculinos'),
('Casa e Jardim', 'Decoração e utensílios para casa'),
('Livros', 'Livros de diversos gêneros'),
('Esportes', 'Artigos esportivos e fitness'),
('Beleza', 'Produtos de beleza e cuidados pessoais'),
('Infantil', 'Produtos para crianças'),
('Automóveis', 'Acessórios e peças para carros'),
('Games', 'Jogos e acessórios para videogames');

-- 5. PRODUTOS
INSERT INTO Produto (Nome, Descricao, Preco, Estoque, ID_Vendedor) VALUES
-- TechStore Brasil (Vendedor 1)
('Smartphone Galaxy S23', 'Smartphone Android com 128GB', 2499.99, 50, 1),
('Notebook Dell Inspiron', 'Notebook com Intel i5 e 8GB RAM', 3299.99, 25, 1),
('Fone Bluetooth JBL', 'Fone de ouvido sem fio com cancelamento de ruído', 299.99, 100, 1),
('Smartwatch Apple Watch', 'Relógio inteligente com GPS', 1899.99, 30, 1),
-- Moda & Estilo (Vendedor 2)
('Vestido Floral Verão', 'Vestido leve para o verão', 89.99, 75, 2),
('Blusa Social Feminina', 'Blusa elegante para trabalho', 69.99, 60, 2),
('Calça Jeans Skinny', 'Calça jeans feminina modelo skinny', 119.99, 80, 2),
('Tênis Casual Feminino', 'Tênis confortável para o dia a dia', 159.99, 45, 2),
-- Casa & Decoração (Vendedor 3)
('Sofá 3 Lugares', 'Sofá confortável para sala de estar', 1299.99, 15, 3),
('Mesa de Jantar 6 Lugares', 'Mesa de madeira com 6 cadeiras', 899.99, 10, 3),
('Luminária LED Moderna', 'Luminária decorativa com LED', 149.99, 40, 3),
('Tapete Persa 2x3m', 'Tapete decorativo para sala', 399.99, 20, 3),
-- Livraria Cultural (Vendedor 4)
('Dom Casmurro - Machado de Assis', 'Clássico da literatura brasileira', 29.99, 200, 4),
('1984 - George Orwell', 'Romance distópico clássico', 34.99, 150, 4),
('Harry Potter Coleção', 'Coleção completa dos 7 livros', 199.99, 50, 4),
('Curso de Python', 'Livro de programação Python', 89.99, 75, 4),
-- SportMax (Vendedor 5)
('Bicicleta Mountain Bike', 'Bike para trilhas e aventuras', 1199.99, 20, 5),
('Kit Musculação Completo', 'Halteres e anilhas para treino', 599.99, 30, 5),
('Tênis Running Nike', 'Tênis profissional para corrida', 299.99, 60, 5),
('Raquete de Tênis Wilson', 'Raquete profissional de tênis', 449.99, 25, 5);

-- 6. ASSOCIAÇÕES PRODUTO-CATEGORIA
INSERT INTO Produto_Categoria (ID_Produto, ID_Categoria) VALUES
-- Eletrônicos
(1, 1), (2, 1), (3, 1), (4, 1),
-- Roupas/Moda
(5, 2), (6, 2), (7, 2), (8, 2),
-- Casa e Jardim
(9, 4), (10, 4), (11, 4), (12, 4),
-- Livros
(13, 5), (14, 5), (15, 5), (16, 5),
-- Esportes
(17, 6), (18, 6), (19, 6), (20, 6),
-- Algumas categorias cruzadas
(19, 2), -- Tênis também pode ser moda
(3, 10), -- Fone também pode ser games
(15, 8); -- Harry Potter também infantil

-- 7. ENDEREÇOS
INSERT INTO Endereco (Rua, Numero, CEP, Estado, Cidade, Complemento, ID_Comprador) VALUES
-- Múltiplos endereços para alguns compradores
('Rua das Flores', '123', '01234-567', 'SP', 'São Paulo', 'Apt 101', 6),
('Av. Paulista', '456', '01310-100', 'SP', 'São Paulo', 'Cobertura', 6),
('Rua do Comércio', '789', '20040-020', 'RJ', 'Rio de Janeiro', null, 7),
('Praia de Copacabana', '321', '22070-011', 'RJ', 'Rio de Janeiro', 'Frente ao mar', 7),
('Rua da Paz', '654', '30112-000', 'MG', 'Belo Horizonte', null, 8),
('Av. Afonso Pena', '987', '30130-002', 'MG', 'Belo Horizonte', 'Sala 205', 8),
('Rua dos Sonhos', '147', '80010-130', 'PR', 'Curitiba', null, 9),
('Av. Beira Mar', '258', '88010-400', 'SC', 'Florianópolis', null, 10),
('Rua Central', '369', '70040-010', 'DF', 'Brasília', 'Bloco A', 11),
('Rua da Liberdade', '741', '01503-001', 'SP', 'São Paulo', null, 12),
('Av. Boa Viagem', '852', '51011-000', 'PE', 'Recife', 'Apt 301', 13),
('Rua do Porto', '963', '40070-110', 'BA', 'Salvador', null, 14),
('Av. Amazonas', '159', '69020-100', 'AM', 'Manaus', null, 15);

-- 8. CARTÕES
INSERT INTO Cartao (Nome, Numero, Bandeira, Validade) VALUES
('Lucas Almeida', '1234 5678 9012 3456', 'Visa', '2027-12-31'),
('Juliana Souza', '2345 6789 0123 4567', 'Mastercard', '2028-06-30'),
('Rafael Martins', '3456 7890 1234 5678', 'Visa', '2026-09-30'),
('Amanda Lima', '4567 8901 2345 6789', 'Elo', '2027-03-31'),
('Bruno Pereira', '5678 9012 3456 7890', 'Mastercard', '2028-11-30');

-- 9. PAGAMENTOS
INSERT INTO Pagamento (Metodo_Pagamento, Data, Valor, Status) VALUES
('cartao', '2024-01-15', 2499.99, 'aprovado'),
('pix', '2024-01-20', 89.99, 'aprovado'),
('boleto', '2024-02-01', 3299.99, 'pendente'),
('cartao', '2024-02-10', 299.99, 'aprovado'),
('pix', '2024-02-15', 1299.99, 'aprovado'),
('cartao', '2024-03-01', 119.99, 'aprovado'),
('boleto', '2024-03-05', 899.99, 'aprovado'),
('pix', '2024-03-10', 29.99, 'aprovado'),
('cartao', '2024-03-15', 1199.99, 'aprovado'),
('boleto', '2024-03-20', 449.99, 'pendente');

-- 10. DETALHES DOS PAGAMENTOS
-- Pagamentos com Cartão
INSERT INTO PagamentoCartao (ID_Pagamento, ID_Cartao) VALUES
(1, 1), (4, 2), (6, 3), (9, 4);

-- Pagamentos PIX
INSERT INTO PagamentoPix (ID_Pagamento, ChavePix, Instituicao) VALUES
(2, 'lucas.almeida@email.com', 'Banco do Brasil'),
(5, '11321098765', 'Nubank'),
(8, 'rafael.martins@email.com', 'Itaú');

-- Pagamentos Boleto
INSERT INTO PagamentoBoleto (ID_Pagamento, Codigo_Barras, Vencimento) VALUES
(3, '34191790010104351004791020150008291070026000', '2024-02-08'),
(7, '34191790010104351004791020150008291070027000', '2024-03-12'),
(10, '34191790010104351004791020150008291070028000', '2024-03-27');

-- 11. PEDIDOS
INSERT INTO Pedido (Data, Status, ID_Comprador, ID_Endereco, ID_Pagamento) VALUES
('2024-01-15', 'entregue', 6, 1, 1),
('2024-01-20', 'entregue', 7, 3, 2),
('2024-02-01', 'processando', 8, 5, 3),
('2024-02-10', 'enviado', 9, 7, 4),
('2024-02-15', 'entregue', 10, 8, 5),
('2024-03-01', 'entregue', 11, 9, 6),
('2024-03-05', 'entregue', 12, 10, 7),
('2024-03-10', 'enviado', 13, 11, 8),
('2024-03-15', 'processando', 14, 12, 9),
('2024-03-20', 'pendente', 15, 13, 10);

-- 12. ITENS DOS PEDIDOS
INSERT INTO ItemDoPedido (ID_Pedido, ID_Produto, Quantidade, PrecoNaCompra) VALUES
-- Pedido 1: Smartphone
(1, 1, 1, 2499.99),
-- Pedido 2: Vestido
(2, 5, 1, 89.99),
-- Pedido 3: Notebook + Fone
(3, 2, 1, 3299.99),
(3, 3, 1, 299.99),
-- Pedido 4: Fone Bluetooth
(4, 3, 1, 299.99),
-- Pedido 5: Sofá + Luminária
(5, 9, 1, 1299.99),
(5, 11, 2, 149.99),
-- Pedido 6: Calça Jeans
(6, 7, 1, 119.99),
-- Pedido 7: Mesa de Jantar + Tapete
(7, 10, 1, 899.99),
(7, 12, 1, 399.99),
-- Pedido 8: Dom Casmurro
(8, 13, 1, 29.99),
-- Pedido 9: Bicicleta + Tênis
(9, 17, 1, 1199.99),
(9, 19, 1, 299.99),
-- Pedido 10: Raquete de Tênis
(10, 20, 1, 449.99);

-- 13. AVALIAÇÕES
INSERT INTO Avaliacao (Nota, Comentario, Data, ID_Produto, ID_Comprador) VALUES
(5, 'Excelente smartphone! Muito rápido e boa qualidade de câmera.', '2024-01-20', 1, 6),
(4, 'Vestido bonito, tecido bom, mas a cor é um pouco diferente da foto.', '2024-01-25', 5, 7),
(5, 'Notebook perfeito para trabalho! Recomendo muito.', '2024-02-15', 2, 8),
(5, 'Som excelente, bateria dura bastante. Vale cada centavo!', '2024-02-20', 3, 9),
(4, 'Sofá confortável, entrega rápida. Apenas o tecido poderia ser melhor.', '2024-02-25', 9, 10),
(3, 'Calça boa mas ficou um pouco apertada. Talvez seja o modelo.', '2024-03-10', 7, 11),
(5, 'Mesa linda e muito resistente! Família toda adorou.', '2024-03-15', 10, 12),
(5, 'Livro clássico em ótima edição. Chegou em perfeito estado.', '2024-03-20', 13, 13),
(4, 'Bicicleta boa para o preço, mas poderia vir com mais acessórios.', '2024-03-25', 17, 14),
(5, 'Raquete profissional mesmo! Melhorou muito meu jogo.', '2024-03-30', 20, 15);
