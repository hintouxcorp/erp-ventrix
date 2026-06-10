from datetime import datetime

from database.connection import get_connection
from models.pedido import Pedido

class PedidoView:
    def __init__(self, row):
        self.codigo = row[0]
        self.cliente = row[1]
        self.telefone = row[2]
        self.origem = row[3]
        self.status = row[4]
        self.data_criacao = row[5]

        self.produto = row[6]
        self.quantidade = row[7]
        self.valor_unitario = row[8]
        self.custo_unitario = row[9]

    @property
    def total_liquido(self):
        return self.valor_unitario * self.quantidade

    @property
    def lucro_total(self):
        return (self.valor_unitario - self.custo_unitario) * self.quantidade

class PedidoService:

    @staticmethod
    def gerar_codigo():

        return datetime.now().strftime(
            "PED-%Y%m%d-%H%M%S"
        )

    @staticmethod
    def criar_pedido(cliente, telefone, origem, itens):

        conn = get_connection()
        cursor = conn.cursor()

        codigo = PedidoService.gerar_codigo()

        # 1. salva pedido (header)
        cursor.execute("""
            INSERT INTO pedidos (
                codigo, cliente, telefone, origem, status, data_criacao
            ) VALUES (?, ?, ?, ?, ?, ?)
        """, (
            codigo,
            cliente,
            telefone,
            origem,
            "PAGO",
            datetime.now().strftime("%d/%m/%Y %H:%M")
        ))

        # 2. salva itens
        for item in itens:

            cursor.execute("""
                INSERT INTO pedido_itens (
                    pedido_codigo,
                    produto,
                    quantidade,
                    valor_unitario,
                    custo_unitario
                ) VALUES (?, ?, ?, ?, ?)
            """, (
                codigo,
                item["produto"],
                item["quantidade"],
                item["valor"],
                item["custo"]
            ))

        conn.commit()
        conn.close()

        return codigo

    @staticmethod
    def listar_pedidos():

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                p.codigo,
                p.cliente,
                p.telefone,
                p.origem,
                p.status,
                p.data_criacao,

                i.produto,
                i.quantidade,
                i.valor_unitario,
                i.custo_unitario

            FROM pedidos p
            JOIN pedido_itens i ON i.pedido_codigo = p.codigo
            ORDER BY p.id DESC
        """)

        rows = cursor.fetchall()
        conn.close()

        return [PedidoView(row) for row in rows]
    
    @staticmethod
    def total_pedidos():

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT COUNT(*) FROM pedidos"
        )

        total = cursor.fetchone()[0]

        conn.close()

        return total

    @staticmethod
    def faturamento_liquido():

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT COALESCE(SUM(valor_unitario * quantidade), 0)
            FROM pedido_itens
        """)

        total = cursor.fetchone()[0]
        conn.close()

        return total
    
    @staticmethod
    def faturamento_lucro():

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT COALESCE(SUM((valor_unitario - custo_unitario) * quantidade), 0)
            FROM pedido_itens
        """)

        total = cursor.fetchone()[0]
        conn.close()

        return total

    @staticmethod
    def pedidos_hoje():

        hoje = datetime.now().strftime("%d/%m/%Y")

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM pedidos
            WHERE data_criacao LIKE ?
        """, (f"{hoje}%",))

        total = cursor.fetchone()[0]

        conn.close()

        return total
    
    @staticmethod
    def produto_mais_vendido():

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                produto,
                SUM(quantidade) as total
            FROM pedido_itens
            GROUP BY produto
            ORDER BY total DESC
            LIMIT 1
        """)

        resultado = cursor.fetchone()
        conn.close()

        return resultado[0] if resultado else "Sem dados"
    
    @staticmethod
    def melhor_origem():

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                origem,
                COUNT(*) as total
            FROM pedidos
            GROUP BY origem
            ORDER BY total DESC
            LIMIT 1
        """)

        resultado = cursor.fetchone()

        conn.close()

        if resultado:
            return resultado[0]

        return "Sem dados"
    
    @staticmethod
    def ultimos_pedidos(limite=5):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                p.codigo,
                p.cliente,
                p.telefone,
                p.origem,
                p.status,
                p.data_criacao,

                i.produto,
                i.quantidade,
                i.valor_unitario,
                i.custo_unitario

            FROM pedidos p
            JOIN pedido_itens i ON i.pedido_codigo = p.codigo
            ORDER BY p.id DESC
        """)

        rows = cursor.fetchall()
        conn.close()

        pedidos_map = {}

        for r in rows:
            codigo = r[0]

            if codigo not in pedidos_map:
                pedidos_map[codigo] = {
                    "codigo": r[0],
                    "cliente": r[1],
                    "telefone": r[2],
                    "origem": r[3],
                    "status": r[4],
                    "data_criacao": r[5],
                    "itens": []
                }

            pedidos_map[codigo]["itens"].append({
                "produto": r[6],
                "quantidade": r[7],
                "valor_unitario": r[8],
                "custo_unitario": r[9],
            })

        return list(pedidos_map.values())
    
    @staticmethod
    def vendas_por_dia():

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                substr(p.data_criacao, 1, 10) as dia,
                SUM(i.valor_unitario * i.quantidade) as faturamento,
                SUM((i.valor_unitario - i.custo_unitario) * i.quantidade) as lucro
            FROM pedidos p
            JOIN pedido_itens i ON p.codigo = i.pedido_codigo
            GROUP BY dia
            ORDER BY dia DESC
            LIMIT 7
        """)

        rows = cursor.fetchall()
        conn.close()

        resultado = {}

        for r in rows:
            resultado[r[0]] = {
                "faturamento": r[1] or 0,
                "lucro": r[2] or 0
            }

        return dict(sorted(resultado.items()))
    
    @staticmethod
    def quantidade_total():
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT COALESCE(SUM(quantidade), 0)
            FROM pedido_itens
        """)

        total = cursor.fetchone()[0]

        conn.close()

        return total

    @staticmethod
    def editar_pedido(
        codigo,
        cliente,
        telefone,
        origem,
        status
    ):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE pedidos
            SET
                cliente = ?,
                telefone = ?,
                origem = ?,
                status = ?
            WHERE codigo = ?
        """, (
            cliente,
            telefone,
            origem,
            status,
            codigo
        ))

        conn.commit()
        conn.close()
    
    @staticmethod
    def excluir_pedido(codigo):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM pedido_itens
            WHERE pedido_codigo = ?
        """, (codigo,))

        cursor.execute("""
            DELETE FROM pedidos
            WHERE codigo = ?
        """, (codigo,))

        conn.commit()
        conn.close()
