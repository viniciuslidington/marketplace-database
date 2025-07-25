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
    """Listar produtos com filtros opcionais"""
    try:
        with MarketplaceDB() as db:
            produtos = db.get_produtos(categoria_id, preco_min, preco_max, limite)
            return produtos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/produtos/{produto_id}")
async def get_produto(produto_id: int):
    """Buscar produto por ID"""
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
    """Top produtos mais vendidos"""
    try:
        with MarketplaceDB() as db:
            produtos = db.get_produtos_mais_vendidos(limite)
            return produtos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== ENDPOINTS DE CATEGORIAS ====================

@app.get("/categorias")
async def listar_categorias():
    """Listar todas as categorias"""
    try:
        with MarketplaceDB() as db:
            categorias = db.get_categorias()
            return categorias
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== ENDPOINTS DE PEDIDOS ====================

@app.post("/pedidos")
async def criar_pedido(pedido: CriarPedido):
    """Criar um novo pedido"""
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
    """Buscar pedidos de um comprador"""
    try:
        with MarketplaceDB() as db:
            pedidos = db.get_pedidos_comprador(id_comprador)
            return pedidos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== ENDPOINTS DE ANÁLISES ====================

@app.get("/dashboard")
async def get_dashboard():
    """Dashboard com dados de vendas"""
    try:
        with MarketplaceDB() as db:
            dashboard = db.get_dashboard_vendas()
            return dashboard
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/clientes/vip")
async def clientes_vip(limite: int = Query(10, description="Número de clientes")):
    """Top clientes que mais gastaram"""
    try:
        with MarketplaceDB() as db:
            clientes = db.get_clientes_vip(limite)
            return clientes
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/estoque/critico")
async def estoque_critico(limite_estoque: int = Query(30, description="Limite de estoque")):
    """Produtos com estoque baixo"""
    try:
        with MarketplaceDB() as db:
            produtos = db.get_estoque_critico(limite_estoque)
            return produtos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== ENDPOINTS DE USUÁRIOS ====================

@app.get("/comprador/email/{email}")
async def get_comprador_por_email(email: str):
    """Buscar comprador por email"""
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
    """Buscar endereços de um comprador"""
    try:
        with MarketplaceDB() as db:
            enderecos = db.get_enderecos_comprador(id_comprador)
            return enderecos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== ENDPOINT DE SAÚDE ====================

@app.get("/")
async def root():
    """Endpoint de saúde da API"""
    return {
        "message": "Marketplace Database API",
        "status": "online",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Verificar saúde do banco de dados"""
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
