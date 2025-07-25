"""
API FastAPI para o Marketplace Database
"""
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import uvicorn
from database import MarketplaceDB

# Modelos Pydantic para validação de dados
class ProdutoFiltro(BaseModel):
    categoria_id: Optional[int] = None
    preco_min: Optional[float] = None
    preco_max: Optional[float] = None
    limite: int = 50

class ItemPedido(BaseModel):
    id: int
    quantidade: int
    preco: float

class CriarPedido(BaseModel):
    id_comprador: int
    id_endereco: int
    produtos: List[ItemPedido]
    metodo_pagamento: str

# Inicializar FastAPI
app = FastAPI(
    title="Marketplace Database API",
    description="API REST para gerenciamento de marketplace",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== ENDPOINTS DE PRODUTOS ====================

@app.get("/produtos", response_model=List[Dict])
async def listar_produtos(
    categoria_id: Optional[int] = Query(None, description="ID da categoria"),
    preco_min: Optional[float] = Query(None, description="Preço mínimo"),
    preco_max: Optional[float] = Query(None, description="Preço máximo"),
    limite: int = Query(50, description="Limite de resultados")
):
    """
    **Listar produtos com filtros opcionais**
    
    Este endpoint permite buscar produtos do marketplace aplicando diversos filtros:
    
    - **categoria_id**: Filtrar por categoria específica (ex: 1 para Eletrônicos)
    - **preco_min**: Produtos com preço maior ou igual ao valor informado
    - **preco_max**: Produtos com preço menor ou igual ao valor informado  
    - **limite**: Máximo de produtos retornados (padrão: 50)
    
    **Exemplos de uso:**
    - `/produtos` - Lista todos os produtos
    - `/produtos?categoria_id=1` - Produtos da categoria 1
    - `/produtos?preco_min=100&preco_max=500` - Produtos entre R$ 100 e R$ 500
    - `/produtos?limite=10` - Apenas 10 produtos
    
    **Retorna:** Lista de produtos com ID, nome, preço, estoque, vendedor e categoria
    """
    try:
        with MarketplaceDB() as db:
            produtos = db.get_produtos(categoria_id, preco_min, preco_max, limite)
            return produtos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/produtos/{produto_id}")
async def get_produto(produto_id: int):
    """
    **Buscar produto específico por ID**
    
    Retorna informações detalhadas de um produto específico, incluindo:
    
    - Dados básicos: nome, descrição, preço, estoque
    - Informações do vendedor: nome da loja, nome e email do vendedor
    - ID único do produto para uso em pedidos
    
    **Parâmetros:**
    - **produto_id**: ID único do produto (número inteiro)
    
    **Exemplo:** `/produtos/1` - Busca o produto com ID 1
    
    **Retorna:** Objeto com dados completos do produto ou erro 404 se não encontrado
    
    **Uso típico:** Página de detalhes do produto, validação antes de adicionar ao carrinho
    """
    try:
        with MarketplaceDB() as db:
            produto = db.get_produto_by_id(produto_id)
            if not produto:
                raise HTTPException(status_code=404, detail="Produto não encontrado")
            return produto
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/produtos/mais-vendidos")
async def produtos_mais_vendidos(limite: int = Query(10, description="Número de produtos")):
    """
    **Top produtos mais vendidos**
    
    Retorna uma lista dos produtos com maior quantidade vendida, baseado em pedidos entregues.
    
    **Parâmetros:**
    - **limite**: Quantidade de produtos no ranking (padrão: 10, máximo recomendado: 50)
    
    **Dados retornados para cada produto:**
    - Nome do produto e vendedor
    - Quantidade total vendida
    - Receita total gerada
    - Número de pedidos diferentes
    
    **Exemplo:** `/produtos/mais-vendidos?limite=5` - Top 5 produtos
    
    **Uso típico:** Homepage com "Mais Vendidos", relatórios de performance, recomendações
    """
    try:
        with MarketplaceDB() as db:
            produtos = db.get_produtos_mais_vendidos(limite)
            return produtos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== ENDPOINTS DE CATEGORIAS ====================

@app.get("/categorias")
async def listar_categorias():
    """
    **Listar todas as categorias disponíveis**
    
    Retorna lista completa de categorias de produtos com informações adicionais:
    
    **Dados de cada categoria:**
    - ID da categoria (para filtros em outros endpoints)
    - Nome da categoria
    - Descrição detalhada
    - Total de produtos nesta categoria
    
    **Uso típico:** 
    - Menu de navegação do site
    - Filtros de busca
    - Página de categorias
    - Dashboards administrativos
    
    **Exemplo de retorno:**
    ```json
    [
      {
        "id_categoria": 1,
        "nome": "Eletrônicos", 
        "descricao": "Produtos eletrônicos e tecnologia",
        "total_produtos": 25
      }
    ]
    ```
    """
    try:
        with MarketplaceDB() as db:
            categorias = db.get_categorias()
            return categorias
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== ENDPOINTS DE PEDIDOS ====================

@app.post("/pedidos")
async def criar_pedido(pedido: CriarPedido):
    """
    **Criar um novo pedido no marketplace**
    
    Este endpoint processa um pedido completo, incluindo pagamento e atualização de estoque.
    
    **Dados necessários (JSON):**
    ```json
    {
      "id_comprador": 6,
      "id_endereco": 1, 
      "metodo_pagamento": "cartao",
      "produtos": [
        {
          "id": 1,
          "quantidade": 2,
          "preco": 1299.99
        }
      ]
    }
    ```
    
    **Parâmetros:**
    - **id_comprador**: ID do comprador (obtido via `/comprador/email/{email}`)
    - **id_endereco**: ID do endereço de entrega
    - **metodo_pagamento**: "cartao", "pix" ou "boleto"
    - **produtos**: Array com ID, quantidade e preço de cada item
    
    **Processamento automático:**
    - ✅ Criação do pagamento
    - ✅ Criação do pedido
    - ✅ Adição dos itens
    - ✅ Atualização do estoque
    - ✅ Transação segura (rollback em caso de erro)
    
    **Retorna:** ID do pedido e pagamento criados ou erro detalhado
    """
    try:
        with MarketplaceDB() as db:
            # Converter ItemPedido para dict
            produtos_dict = [
                {
                    'id': item.id,
                    'quantidade': item.quantidade,
                    'preco': item.preco
                }
                for item in pedido.produtos
            ]
            
            resultado = db.criar_pedido(
                pedido.id_comprador,
                pedido.id_endereco,
                produtos_dict,
                pedido.metodo_pagamento
            )
            
            if not resultado['success']:
                raise HTTPException(status_code=400, detail=resultado['error'])
            
            return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/pedidos/comprador/{id_comprador}")
async def pedidos_comprador(id_comprador: int):
    """
    **Histórico de pedidos de um comprador**
    
    Retorna todos os pedidos realizados por um comprador específico.
    
    **Parâmetros:**
    - **id_comprador**: ID único do comprador
    
    **Dados retornados:**
    - ID do pedido e data de criação
    - Status atual (processando, enviado, entregue, etc.)
    - Valor total e método de pagamento
    - Status do pagamento (aprovado, pendente, etc.)
    - Lista de produtos no pedido
    
    **Ordenação:** Pedidos mais recentes primeiro
    
    **Exemplo:** `/pedidos/comprador/6` - Pedidos do comprador ID 6
    
    **Uso típico:** 
    - Página "Meus Pedidos" 
    - Histórico de compras
    - Acompanhamento de status
    - Suporte ao cliente
    """
    try:
        with MarketplaceDB() as db:
            pedidos = db.get_pedidos_comprador(id_comprador)
            return pedidos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== ENDPOINTS DE ANÁLISES ====================

@app.get("/dashboard")
async def get_dashboard():
    """
    **Dashboard executivo com métricas de vendas**
    
    Endpoint principal para obter indicadores consolidados do marketplace.
    
    **Métricas incluídas:**
    
    **📊 Top 5 Vendedores:**
    - Nome da loja
    - Faturamento total (apenas pedidos entregues)
    - Número total de pedidos
    
    **📅 Vendas por Mês:**
    - Mês (1-12)
    - Total de pedidos no mês
    - Faturamento mensal
    
    **💳 Métodos de Pagamento:**
    - Tipo de pagamento (cartao, pix, boleto)
    - Número de transações aprovadas
    - Valor total transacionado
    
    **Uso típico:**
    - Dashboard administrativo
    - Relatórios gerenciais
    - KPIs de performance
    - Tomada de decisões estratégicas
    
    **Atualização:** Dados em tempo real baseados na última transação
    """
    try:
        with MarketplaceDB() as db:
            dashboard = db.get_dashboard_vendas()
            return dashboard
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/clientes/vip")
async def clientes_vip(limite: int = Query(10, description="Número de clientes")):
    """
    **Top clientes que mais gastaram**
    
    Lista os clientes mais valiosos baseado no valor total gasto em pedidos entregues.
    
    **Parâmetros:**
    - **limite**: Quantos clientes retornar no ranking (padrão: 10)
    
    **Métricas de cada cliente:**
    - Nome do comprador e CPF
    - Total de pedidos realizados
    - Valor total gasto (soma de todos os pedidos entregues)
    - Ticket médio por pedido
    
    **Critério de ordenação:** Valor total gasto (maior para menor)
    
    **Filtros aplicados:** 
    - Apenas pedidos com status "entregue"
    - Apenas pagamentos processados
    
    **Uso típico:**
    - Programas de fidelidade
    - Campanhas de marketing direcionadas
    - Análise de clientes
    - Relatórios comerciais
    """
    try:
        with MarketplaceDB() as db:
            clientes = db.get_clientes_vip(limite)
            return clientes
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/estoque/critico")
async def estoque_critico(limite_estoque: int = Query(30, description="Limite de estoque")):
    """
    **Produtos com estoque baixo - Alerta de reposição**
    
    Identifica produtos que precisam de reposição urgente baseado no nível de estoque.
    
    **Parâmetros:**
    - **limite_estoque**: Considera produtos com estoque até este valor (padrão: 30)
    
    **Classificação automática:**
    - 🚨 **CRÍTICO**: ≤ 10 unidades (reposição urgente)
    - ⚠️ **BAIXO**: ≤ 30 unidades (planejar reposição)
    
    **Dados de cada produto:**
    - Nome do produto e vendedor responsável
    - Quantidade atual em estoque
    - Preço unitário
    - Total vendido historicamente
    - Status do estoque (CRÍTICO/BAIXO)
    
    **Ordenação:** Menor estoque primeiro (produtos mais críticos no topo)
    
    **Uso típico:**
    - Gestão de estoque
    - Alertas automáticos
    - Planejamento de compras
    - Relatórios operacionais
    """
    try:
        with MarketplaceDB() as db:
            produtos = db.get_estoque_critico(limite_estoque)
            return produtos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== ENDPOINTS DE USUÁRIOS ====================

@app.get("/comprador/email/{email}")
async def get_comprador_por_email(email: str):
    """
    **Buscar comprador por endereço de email**
    
    Localiza um comprador usando seu email como identificador único.
    
    **Parâmetros:**
    - **email**: Endereço de email do comprador (ex: usuario@email.com)
    
    **Dados retornados:**
    - ID único do usuário (necessário para criar pedidos)
    - Nome completo
    - Email confirmado
    - Telefone (se cadastrado)
    - CPF do comprador
    
    **Exemplo:** `/comprador/email/lucas.almeida@email.com`
    
    **Uso típico:**
    - Login/autenticação
    - Busca de perfil de usuário
    - Validação antes de criar pedidos
    - Recuperação de dados de cliente
    
    **Importante:** Este endpoint é essencial para obter o `id_comprador` 
    necessário na criação de pedidos via POST `/pedidos`
    """
    try:
        with MarketplaceDB() as db:
            comprador = db.get_comprador_by_email(email)
            if not comprador:
                raise HTTPException(status_code=404, detail="Comprador não encontrado")
            return comprador
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/comprador/{id_comprador}/enderecos")
async def enderecos_comprador(id_comprador: int):
    """
    **Endereços cadastrados de um comprador**
    
    Lista todos os endereços de entrega cadastrados por um comprador específico.
    
    **Parâmetros:**
    - **id_comprador**: ID único do comprador
    
    **Dados de cada endereço:**
    - ID do endereço (necessário para criar pedidos)
    - Rua, número e complemento
    - CEP, cidade e estado
    - Vinculação ao comprador
    
    **Ordenação:** Por ID do endereço (mais antigo primeiro)
    
    **Exemplo:** `/comprador/6/enderecos` - Endereços do comprador ID 6
    
    **Uso típico:**
    - Seleção de endereço de entrega no checkout
    - Gerenciamento de endereços no perfil
    - Validação de endereços para pedidos
    - Cálculo de frete por região
    
    **Importante:** O `id_endereco` retornado aqui é necessário 
    para o campo `id_endereco` ao criar pedidos via POST `/pedidos`
    """
    try:
        with MarketplaceDB() as db:
            enderecos = db.get_enderecos_comprador(id_comprador)
            return enderecos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== ENDPOINT DE SAÚDE ====================

@app.get("/")
async def root():
    """
    **Endpoint de status da API**
    
    Endpoint principal que confirma se a API está online e operacional.
    
    **Retorna:**
    - Status da API (online/offline)
    - Versão atual da aplicação
    - Link para documentação interativa
    - Nome da aplicação
    
    **Uso típico:**
    - Health check básico
    - Verificação rápida de conectividade
    - Descoberta da documentação da API
    - Monitoramento de infraestrutura
    """
    return {
        "message": "Marketplace Database API",
        "status": "online",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """
    **Health check completo da aplicação**
    
    Verifica se a API e o banco de dados estão funcionando corretamente.
    
    **Testes realizados:**
    - ✅ Conectividade com banco de dados PostgreSQL
    - ✅ Execução de query simples de teste
    - ✅ Status geral da aplicação
    
    **Códigos de resposta:**
    - **200**: Tudo funcionando normalmente
    - **503**: Problema com banco de dados ou aplicação
    
    **Uso típico:**
    - Monitoramento de infraestrutura
    - Load balancers e health checks
    - Alertas de sistema
    - Verificação antes de deploy
    
    **Importante:** Este endpoint deve sempre responder rapidamente.
    Se demorar mais de 5 segundos, pode indicar problema na infraestrutura.
    """
    try:
        with MarketplaceDB() as db:
            db.cursor.execute("SELECT 1")
            return {"status": "healthy", "database": "connected"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Database error: {str(e)}")

# ==================== EXECUTAR SERVIDOR ====================

def main():
    """Função principal para execução"""
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    main()
