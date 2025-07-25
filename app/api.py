from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import uvicorn
from .database import MarketplaceDB

TABELAS_DISPONIVEIS = [
    "Usuario", "Comprador", "Vendedor", "Categoria", "Produto", 
    "Produto_Categoria", "Endereco", "Pagamento", "Cartao", 
    "PagamentoCartao", "PagamentoPix", "PagamentoBoleto", 
    "Pedido", "ItemDoPedido", "Avaliacao"
]

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

app = FastAPI(
    title="🏪 Marketplace Database API",
    description="""
    ## 📋 API REST completa para gerenciamento de marketplace
    
    **Funcionalidades principais:**
    - 🛍️ Gestão de produtos e categorias
    - 🛒 Processamento de pedidos 
    - 👥 Gerenciamento de usuários (compradores/vendedores)
    - 💳 Sistema de pagamentos
    - 📊 Analytics e relatórios
    - 🗃️ Acesso direto às tabelas do banco
    
    **Documentação interativa:** Explore todos os endpoints abaixo
    """,
    version="1.0.0",
    contact={
        "name": "Marketplace Database",
        "url": "https://github.com/viniciuslidington/marketplace-database",
    },
    tags_metadata=[
        {
            "name": "🛍️ Produtos",
            "description": "Gestão do catálogo de produtos, busca e filtros"
        },
        {
            "name": "📂 Categorias", 
            "description": "Gerenciamento de categorias de produtos"
        },
        {
            "name": "🛒 Pedidos",
            "description": "Criação e consulta de pedidos"
        },
        {
            "name": "👥 Usuários",
            "description": "Gestão de compradores e vendedores"
        },
        {
            "name": "📊 Analytics",
            "description": "Relatórios e métricas do marketplace"
        },
        {
            "name": "❤️ Sistema",
            "description": "Health checks e status da aplicação"
        },
        {
            "name": "🗃️ Tabelas",
            "description": "Acesso direto aos dados das tabelas (SELECT *)"
        }
    ]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/produtos", response_model=List[Dict], tags=["🛍️ Produtos"])
async def listar_produtos(
    categoria_id: Optional[int] = Query(None, description="ID da categoria"),
    preco_min: Optional[float] = Query(None, description="Preço mínimo"),
    preco_max: Optional[float] = Query(None, description="Preço máximo"),
    limite: int = Query(50, description="Limite de resultados"),
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


@app.get("/produtos/mais-vendidos", tags=["🛍️ Produtos"])
async def produtos_mais_vendidos(
    limite: int = Query(10, description="Número de produtos"),
):
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
            limite = int(limite)  # Garantir que limite é um inteiro
            produtos = db.get_produtos_mais_vendidos(limite)
            return produtos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/produtos/{produto_id}", tags=["🛍️ Produtos"])
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


@app.get("/categorias", tags=["📂 Categorias"])
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


@app.post("/pedidos", tags=["🛒 Pedidos"])
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
                {"id": item.id, "quantidade": item.quantidade, "preco": item.preco}
                for item in pedido.produtos
            ]

            resultado = db.criar_pedido(
                pedido.id_comprador,
                pedido.id_endereco,
                produtos_dict,
                pedido.metodo_pagamento,
            )

            if not resultado["success"]:
                raise HTTPException(status_code=400, detail=resultado["error"])

            return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/pedidos/comprador/{id_comprador}", tags=["🛒 Pedidos"])
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


@app.get("/dashboard", tags=["📊 Analytics"])
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


@app.get("/clientes/vip", tags=["📊 Analytics"])
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


@app.get("/estoque/critico", tags=["📊 Analytics"])
async def estoque_critico(
    limite_estoque: int = Query(30, description="Limite de estoque"),
):
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


@app.get("/comprador/email/{email}", tags=["👥 Usuários"])
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


@app.get("/comprador/{id_comprador}/enderecos", tags=["👥 Usuários"])
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


@app.get("/tabelas/usuarios", tags=["🗃️ Tabelas"])
async def listar_usuarios():
    """
    **SELECT * FROM Usuario**

    Retorna todos os registros da tabela Usuario.

    **Dados incluídos:**
    - ID_Usuario, Nome, Email, Telefone, Data_Cadastro

    **Uso:** Visualizar todos os usuários cadastrados no sistema
    """
    try:
        with MarketplaceDB() as db:
            db.cursor.execute("SELECT * FROM Usuario ORDER BY ID_Usuario")
            usuarios = db.cursor.fetchall()
            return [dict(usuario) for usuario in usuarios]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/tabelas/compradores", tags=["🗃️ Tabelas"])
async def listar_compradores():
    """
    **SELECT * FROM Comprador**

    Retorna todos os registros da tabela Comprador.

    **Dados incluídos:**
    - ID_Usuario, CPF (informações específicas de compradores)

    **Uso:** Visualizar dados específicos dos compradores
    """
    try:
        with MarketplaceDB() as db:
            db.cursor.execute("SELECT * FROM Comprador ORDER BY ID_Usuario")
            compradores = db.cursor.fetchall()
            return [dict(comprador) for comprador in compradores]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/tabelas/vendedores", tags=["🗃️ Tabelas"])
async def listar_vendedores():
    """
    **SELECT * FROM Vendedor**

    Retorna todos os registros da tabela Vendedor.

    **Dados incluídos:**
    - ID_Usuario, CNPJ, Nome_Loja, Endereco_Comercial

    **Uso:** Visualizar dados específicos dos vendedores
    """
    try:
        with MarketplaceDB() as db:
            db.cursor.execute("SELECT * FROM Vendedor ORDER BY ID_Usuario")
            vendedores = db.cursor.fetchall()
            return [dict(vendedor) for vendedor in vendedores]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/tabelas/enderecos", tags=["🗃️ Tabelas"])
async def listar_enderecos():
    """
    **SELECT * FROM Endereco**

    Retorna todos os registros da tabela Endereco.

    **Dados incluídos:**
    - ID_Endereco, ID_Comprador, Rua, Numero, Complemento, CEP, Cidade, Estado

    **Uso:** Visualizar todos os endereços cadastrados
    """
    try:
        with MarketplaceDB() as db:
            db.cursor.execute("SELECT * FROM Endereco ORDER BY ID_Endereco")
            enderecos = db.cursor.fetchall()
            return [dict(endereco) for endereco in enderecos]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/tabelas/categorias-completa", tags=["🗃️ Tabelas"])
async def listar_categorias_completa():
    """
    **SELECT * FROM Categoria**

    Retorna todos os registros da tabela Categoria.

    **Dados incluídos:**
    - ID_Categoria, Nome, Descricao

    **Uso:** Visualizar estrutura completa das categorias
    """
    try:
        with MarketplaceDB() as db:
            db.cursor.execute("SELECT * FROM Categoria ORDER BY ID_Categoria")
            categorias = db.cursor.fetchall()
            return [dict(categoria) for categoria in categorias]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/tabelas/produtos-completa", tags=["🗃️ Tabelas"])
async def listar_produtos_completa():
    """
    **SELECT * FROM Produto**

    Retorna todos os registros da tabela Produto.

    **Dados incluídos:**
    - ID_Produto, Nome, Descricao, Preco, ID_Categoria, ID_Vendedor, Data_Cadastro

    **Uso:** Visualizar estrutura completa dos produtos
    """
    try:
        with MarketplaceDB() as db:
            db.cursor.execute("SELECT * FROM Produto ORDER BY ID_Produto")
            produtos = db.cursor.fetchall()
            return [dict(produto) for produto in produtos]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/tabelas/estoque", tags=["🗃️ Tabelas"])
async def listar_estoque():
    """
    **SELECT * FROM Estoque**

    Retorna todos os registros da tabela Estoque.

    **Dados incluídos:**
    - ID_Estoque, ID_Produto, Quantidade, Data_Atualizacao

    **Uso:** Visualizar situação completa do estoque
    """
    try:
        with MarketplaceDB() as db:
            db.cursor.execute("SELECT * FROM Estoque ORDER BY ID_Estoque")
            estoque = db.cursor.fetchall()
            return [dict(item) for item in estoque]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/tabelas/pedidos-completa", tags=["🗃️ Tabelas"])
async def listar_pedidos_completa():
    """
    **SELECT * FROM Pedido**

    Retorna todos os registros da tabela Pedido.

    **Dados incluídos:**
    - ID_Pedido, ID_Comprador, ID_Endereco, Data, Status, Total

    **Uso:** Visualizar estrutura completa dos pedidos
    """
    try:
        with MarketplaceDB() as db:
            db.cursor.execute("SELECT * FROM Pedido ORDER BY ID_Pedido DESC")
            pedidos = db.cursor.fetchall()
            return [dict(pedido) for pedido in pedidos]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/tabelas/itens-pedido", tags=["🗃️ Tabelas"])
async def listar_itens_pedido():
    """
    **SELECT * FROM ItemPedido**

    Retorna todos os registros da tabela ItemPedido.

    **Dados incluídos:**
    - ID_Item, ID_Pedido, ID_Produto, Quantidade, Preco_Unitario

    **Uso:** Visualizar todos os itens de todos os pedidos
    """
    try:
        with MarketplaceDB() as db:
            db.cursor.execute("SELECT * FROM ItemPedido ORDER BY ID_Item")
            itens = db.cursor.fetchall()
            return [dict(item) for item in itens]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/tabelas/status-pedidos", tags=["🗃️ Tabelas"])
async def listar_status_pedidos():
    """
    **SELECT * FROM StatusPedido**

    Retorna todos os registros da tabela StatusPedido.

    **Dados incluídos:**
    - ID_Status, ID_Pedido, Status, Data_Mudanca

    **Uso:** Visualizar histórico completo de mudanças de status
    """
    try:
        with MarketplaceDB() as db:
            db.cursor.execute("SELECT * FROM StatusPedido ORDER BY ID_Status DESC")
            status = db.cursor.fetchall()
            return [dict(s) for s in status]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/tabelas/pagamentos", tags=["🗃️ Tabelas"])
async def listar_pagamentos():
    """
    **SELECT * FROM Pagamento**

    Retorna todos os registros da tabela Pagamento.

    **Dados incluídos:**
    - ID_Pagamento, ID_Pedido, Metodo, Valor, Status, Data_Processamento

    **Uso:** Visualizar todas as transações de pagamento
    """
    try:
        with MarketplaceDB() as db:
            db.cursor.execute("SELECT * FROM Pagamento ORDER BY ID_Pagamento DESC")
            pagamentos = db.cursor.fetchall()
            return [dict(pagamento) for pagamento in pagamentos]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/tabelas/cartoes", tags=["🗃️ Tabelas"])
async def listar_cartoes():
    """
    **SELECT * FROM Cartao**

    Retorna todos os registros da tabela Cartao.

    **Dados incluídos:**
    - ID_Cartao, ID_Comprador, Numero_Cartao, Nome_Titular, Validade, CVV

    **Uso:** Visualizar cartões cadastrados (dados sensíveis mascarados em produção)
    """
    try:
        with MarketplaceDB() as db:
            db.cursor.execute("SELECT * FROM Cartao ORDER BY ID_Cartao")
            cartoes = db.cursor.fetchall()
            return [dict(cartao) for cartao in cartoes]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/tabelas/avaliacoes", tags=["🗃️ Tabelas"])
async def listar_avaliacoes():
    """
    **SELECT * FROM Avaliacao**

    Retorna todos os registros da tabela Avaliacao.

    **Dados incluídos:**
    - ID_Avaliacao, ID_Pedido, Nota, Comentario, Data_Avaliacao

    **Uso:** Visualizar todas as avaliações e comentários
    """
    try:
        with MarketplaceDB() as db:
            db.cursor.execute("SELECT * FROM Avaliacao ORDER BY ID_Avaliacao DESC")
            avaliacoes = db.cursor.fetchall()
            return [dict(avaliacao) for avaliacao in avaliacoes]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/tabelas/resumo", tags=["🗃️ Tabelas"])
async def listar_resumo_tabelas():
    """
    **Resumo de todas as tabelas - Contagem de registros**

    Retorna uma visão geral com o número de registros em cada tabela do sistema.

    **Informações incluídas:**
    - Nome da tabela
    - Quantidade total de registros
    - Status (OK/Vazia)

    **Uso:**
    - Visão geral do sistema
    - Verificação de integridade
    - Monitoramento de crescimento de dados
    """
    try:
        with MarketplaceDB() as db:
            tabelas = [
                "Usuario",
                "Comprador",
                "Vendedor",
                "Categoria",
                "Produto",
                "Produto_Categoria",
                "Endereco",
                "Pagamento",
                "Cartao",
                "PagamentoCartao",
                "PagamentoPix",
                "PagamentoBoleto",
                "Pedido",
                "ItemDoPedido",
                "Avaliacao",
            ]

            resumo = []
            for tabela in tabelas:
                db.cursor.execute(f"SELECT COUNT(*) as total FROM {tabela}")
                total = db.cursor.fetchone()["total"]
                resumo.append(
                    {
                        "tabela": tabela,
                        "total_registros": total,
                        "status": "OK" if total > 0 else "Vazia",
                    }
                )

            return resumo
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/", tags=["❤️ Sistema"])
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
        "docs": "/docs",
    }


@app.get("/health", tags=["❤️ Sistema"])
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


def main():
    """Função principal para execução"""
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True, log_level="info")

if __name__ == "__main__":
    main()

