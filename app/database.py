"""
Módulo de conexão e operações com banco de dados PostgreSQL
"""
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
import os
from typing import List, Dict, Optional

class MarketplaceDB:
    def __init__(self):
        """Inicializa conexão com o banco de dados"""
        self.connection = psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            database=os.getenv("DB_NAME", "marketplace"),
            user=os.getenv("DB_USER", "admin"),
            password=os.getenv("DB_PASSWORD", "admin123"),
            port=os.getenv("DB_PORT", "5432")
        )
        self.cursor = self.connection.cursor(cursor_factory=RealDictCursor)
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
    
    def close(self):
        """Fecha conexões com o banco"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
    
    # ==================== PRODUTOS ====================
    
    def get_produtos(self, categoria_id: Optional[int] = None, 
                    preco_min: Optional[float] = None, 
                    preco_max: Optional[float] = None,
                    limite: int = 50) -> List[Dict]:
        """Buscar produtos com filtros opcionais"""
        query = """
        SELECT 
            p.ID_Produto,
            p.Nome,
            p.Descricao,
            p.Preco,
            p.Estoque,
            v.Nome_Loja AS vendedor,
            c.Nome AS categoria
        FROM Produto p
        JOIN Vendedor v ON p.ID_Vendedor = v.ID_Usuario
        LEFT JOIN Produto_Categoria pc ON p.ID_Produto = pc.ID_Produto
        LEFT JOIN Categoria c ON pc.ID_Categoria = c.ID_Categoria
        """
        
        conditions = []
        params = []
        
        if categoria_id:
            conditions.append("c.ID_Categoria = %s")
            params.append(categoria_id)
        
        if preco_min:
            conditions.append("p.Preco >= %s")
            params.append(preco_min)
        
        if preco_max:
            conditions.append("p.Preco <= %s")
            params.append(preco_max)
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        query += " ORDER BY p.Preco LIMIT %s"
        params.append(limite)
        
        self.cursor.execute(query, params)
        return [dict(row) for row in self.cursor.fetchall()]
    
    def get_produto_by_id(self, produto_id: int) -> Optional[Dict]:
        """Buscar produto específico por ID"""
        query = """
        SELECT 
            p.*,
            v.Nome_Loja AS vendedor,
            u.Nome AS nome_vendedor,
            u.Email AS email_vendedor
        FROM Produto p
        JOIN Vendedor v ON p.ID_Vendedor = v.ID_Usuario
        JOIN Usuario u ON v.ID_Usuario = u.ID_Usuario
        WHERE p.ID_Produto = %s
        """
        self.cursor.execute(query, (produto_id,))
        result = self.cursor.fetchone()
        return dict(result) if result else None
    
    def get_produtos_mais_vendidos(self, limite: int = 10) -> List[Dict]:
        """Top produtos mais vendidos"""
        query = """
        SELECT 
            p.Nome AS produto,
            v.Nome_Loja AS vendedor,
            SUM(idp.Quantidade) AS quantidade_vendida,
            SUM(idp.Quantidade * idp.PrecoNaCompra) AS receita_total,
            COUNT(DISTINCT idp.ID_Pedido) AS numero_pedidos
        FROM Produto p
        JOIN ItemDoPedido idp ON p.ID_Produto = idp.ID_Produto
        JOIN Pedido ped ON idp.ID_Pedido = ped.ID_Pedido
        JOIN Vendedor v ON p.ID_Vendedor = v.ID_Usuario
        WHERE ped.Status = 'entregue'
        GROUP BY p.ID_Produto, p.Nome, v.Nome_Loja
        ORDER BY quantidade_vendida DESC
        LIMIT %s
        """
        self.cursor.execute(query, (limite,))
        return [dict(row) for row in self.cursor.fetchall()]
    
    # ==================== CATEGORIAS ====================
    
    def get_categorias(self) -> List[Dict]:
        """Listar todas as categorias"""
        query = """
        SELECT 
            c.*,
            COUNT(pc.ID_Produto) AS total_produtos
        FROM Categoria c
        LEFT JOIN Produto_Categoria pc ON c.ID_Categoria = pc.ID_Categoria
        GROUP BY c.ID_Categoria, c.Nome, c.Descricao
        ORDER BY c.Nome
        """
        self.cursor.execute(query)
        return [dict(row) for row in self.cursor.fetchall()]
    
    # ==================== PEDIDOS ====================
    
    def criar_pedido(self, id_comprador: int, id_endereco: int, 
                    produtos: List[Dict], metodo_pagamento: str) -> Dict:
        """Criar um novo pedido"""
        try:
            # Calcular valor total
            valor_total = sum(item['preco'] * item['quantidade'] for item in produtos)
            
            # Inserir pagamento
            query_pagamento = """
            INSERT INTO Pagamento (Metodo_Pagamento, Data, Valor, Status)
            VALUES (%s, %s, %s, 'processando')
            RETURNING ID_Pagamento
            """
            self.cursor.execute(query_pagamento, (metodo_pagamento, datetime.now().date(), valor_total))
            id_pagamento = self.cursor.fetchone()['id_pagamento']
            
            # Inserir pedido
            query_pedido = """
            INSERT INTO Pedido (Data, Status, ID_Comprador, ID_Endereco, ID_Pagamento)
            VALUES (%s, 'processando', %s, %s, %s)
            RETURNING ID_Pedido
            """
            self.cursor.execute(query_pedido, (datetime.now().date(), id_comprador, id_endereco, id_pagamento))
            id_pedido = self.cursor.fetchone()['id_pedido']
            
            # Inserir itens do pedido
            for produto in produtos:
                query_item = """
                INSERT INTO ItemDoPedido (ID_Pedido, ID_Produto, Quantidade, PrecoNaCompra)
                VALUES (%s, %s, %s, %s)
                """
                self.cursor.execute(query_item, (id_pedido, produto['id'], produto['quantidade'], produto['preco']))
                
                # Atualizar estoque
                query_estoque = """
                UPDATE Produto SET Estoque = Estoque - %s WHERE ID_Produto = %s
                """
                self.cursor.execute(query_estoque, (produto['quantidade'], produto['id']))
            
            self.connection.commit()
            return {'success': True, 'pedido_id': id_pedido, 'pagamento_id': id_pagamento}
            
        except Exception as e:
            self.connection.rollback()
            return {'success': False, 'error': str(e)}
    
    def get_pedidos_comprador(self, id_comprador: int) -> List[Dict]:
        """Buscar pedidos de um comprador"""
        query = """
        SELECT 
            ped.ID_Pedido,
            ped.Data,
            ped.Status,
            pag.Valor,
            pag.Metodo_Pagamento,
            pag.Status AS status_pagamento,
            STRING_AGG(p.Nome, ', ') AS produtos
        FROM Pedido ped
        JOIN Pagamento pag ON ped.ID_Pagamento = pag.ID_Pagamento
        JOIN ItemDoPedido idp ON ped.ID_Pedido = idp.ID_Pedido
        JOIN Produto p ON idp.ID_Produto = p.ID_Produto
        WHERE ped.ID_Comprador = %s
        GROUP BY ped.ID_Pedido, ped.Data, ped.Status, pag.Valor, pag.Metodo_Pagamento, pag.Status
        ORDER BY ped.Data DESC
        """
        self.cursor.execute(query, (id_comprador,))
        return [dict(row) for row in self.cursor.fetchall()]
    
    # ==================== ANÁLISES E RELATÓRIOS ====================
    
    def get_dashboard_vendas(self) -> Dict:
        """Dados para dashboard de vendas"""
        # Faturamento por vendedor
        query_vendedores = """
        SELECT 
            v.Nome_Loja,
            SUM(idp.Quantidade * idp.PrecoNaCompra) AS faturamento,
            COUNT(DISTINCT ped.ID_Pedido) AS total_pedidos
        FROM Vendedor v
        JOIN Produto p ON v.ID_Usuario = p.ID_Vendedor
        JOIN ItemDoPedido idp ON p.ID_Produto = idp.ID_Produto
        JOIN Pedido ped ON idp.ID_Pedido = ped.ID_Pedido
        WHERE ped.Status = 'entregue'
        GROUP BY v.Nome_Loja
        ORDER BY faturamento DESC
        LIMIT 5
        """
        
        # Vendas por mês
        query_vendas_mes = """
        SELECT 
            EXTRACT(MONTH FROM ped.Data) AS mes,
            COUNT(*) AS total_pedidos,
            SUM(pag.Valor) AS faturamento
        FROM Pedido ped
        JOIN Pagamento pag ON ped.ID_Pagamento = pag.ID_Pagamento
        WHERE ped.Status = 'entregue'
        GROUP BY EXTRACT(MONTH FROM ped.Data)
        ORDER BY mes
        """
        
        # Métodos de pagamento
        query_pagamentos = """
        SELECT 
            Metodo_Pagamento,
            COUNT(*) AS total,
            SUM(Valor) AS valor_total
        FROM Pagamento
        WHERE Status = 'aprovado'
        GROUP BY Metodo_Pagamento
        """
        
        self.cursor.execute(query_vendedores)
        top_vendedores = [dict(row) for row in self.cursor.fetchall()]
        
        self.cursor.execute(query_vendas_mes)
        vendas_mes = [dict(row) for row in self.cursor.fetchall()]
        
        self.cursor.execute(query_pagamentos)
        metodos_pagamento = [dict(row) for row in self.cursor.fetchall()]
        
        return {
            'top_vendedores': top_vendedores,
            'vendas_por_mes': vendas_mes,
            'metodos_pagamento': metodos_pagamento
        }
    
    def get_clientes_vip(self, limite: int = 10) -> List[Dict]:
        """Top clientes que mais gastaram"""
        query = """
        SELECT 
            u.Nome AS comprador,
            c.CPF,
            COUNT(DISTINCT ped.ID_Pedido) AS total_pedidos,
            SUM(pag.Valor) AS valor_total_gasto,
            AVG(pag.Valor) AS ticket_medio
        FROM Usuario u
        JOIN Comprador c ON u.ID_Usuario = c.ID_Usuario
        JOIN Pedido ped ON c.ID_Usuario = ped.ID_Comprador
        JOIN Pagamento pag ON ped.ID_Pagamento = pag.ID_Pagamento
        WHERE ped.Status = 'entregue'
        GROUP BY u.ID_Usuario, u.Nome, c.CPF
        ORDER BY valor_total_gasto DESC
        LIMIT %s
        """
        self.cursor.execute(query, (limite,))
        return [dict(row) for row in self.cursor.fetchall()]
    
    def get_estoque_critico(self, limite_estoque: int = 30) -> List[Dict]:
        """Produtos com estoque baixo"""
        query = """
        SELECT 
            p.Nome AS produto,
            p.Estoque,
            p.Preco,
            v.Nome_Loja AS vendedor,
            COALESCE(SUM(idp.Quantidade), 0) AS total_vendido,
            CASE 
                WHEN p.Estoque <= 10 THEN 'CRÍTICO'
                WHEN p.Estoque <= 30 THEN 'BAIXO'
                ELSE 'OK'
            END AS status_estoque
        FROM Produto p
        JOIN Vendedor v ON p.ID_Vendedor = v.ID_Usuario
        LEFT JOIN ItemDoPedido idp ON p.ID_Produto = idp.ID_Produto
        LEFT JOIN Pedido ped ON idp.ID_Pedido = ped.ID_Pedido AND ped.Status = 'entregue'
        WHERE p.Estoque <= %s
        GROUP BY p.ID_Produto, p.Nome, p.Estoque, p.Preco, v.Nome_Loja
        ORDER BY p.Estoque ASC
        """
        self.cursor.execute(query, (limite_estoque,))
        return [dict(row) for row in self.cursor.fetchall()]

    # ==================== USUÁRIOS ====================
    
    def get_comprador_by_email(self, email: str) -> Optional[Dict]:
        """Buscar comprador por email"""
        query = """
        SELECT 
            u.ID_Usuario,
            u.Nome,
            u.Email,
            u.Telefone,
            c.CPF
        FROM Usuario u
        JOIN Comprador c ON u.ID_Usuario = c.ID_Usuario
        WHERE u.Email = %s
        """
        self.cursor.execute(query, (email,))
        result = self.cursor.fetchone()
        return dict(result) if result else None
    
    def get_enderecos_comprador(self, id_comprador: int) -> List[Dict]:
        """Buscar endereços de um comprador"""
        query = """
        SELECT * FROM Endereco 
        WHERE ID_Comprador = %s
        ORDER BY ID_Endereco
        """
        self.cursor.execute(query, (id_comprador,))
        return [dict(row) for row in self.cursor.fetchall()]
