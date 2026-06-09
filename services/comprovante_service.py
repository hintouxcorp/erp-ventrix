from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime
import os

from database.connection import get_connection


class ComprovanteService:

    @staticmethod
    def gerar_pdf(codigo_pedido):

        conn = get_connection()
        cursor = conn.cursor()

        # =========================
        # PEDIDO
        # =========================

        cursor.execute("""
            SELECT
                codigo,
                cliente,
                telefone,
                origem,
                status,
                data_criacao
            FROM pedidos
            WHERE codigo = ?
        """, (codigo_pedido,))

        pedido = cursor.fetchone()

        if not pedido:
            conn.close()
            return None

        # =========================
        # ITENS
        # =========================

        cursor.execute("""
            SELECT
                produto,
                quantidade,
                valor_unitario
            FROM pedido_itens
            WHERE pedido_codigo = ?
        """, (codigo_pedido,))

        itens = cursor.fetchall()

        conn.close()

        # =========================
        # CALCULA TOTAL
        # =========================

        total = 0

        for item in itens:
            total += item[1] * item[2]

        # =========================
        # CRIA PASTA
        # =========================

        pasta = "comprovantes"

        os.makedirs(
            pasta,
            exist_ok=True
        )

        arquivo = os.path.join(
            pasta,
            f"{codigo_pedido}.pdf"
        )

        # =========================
        # PDF
        # =========================

        c = canvas.Canvas(
            arquivo,
            pagesize=A4
        )

        largura, altura = A4

        y = altura - 50

        # Logo/Título

        c.setFont(
            "Helvetica-Bold",
            18
        )

        c.drawCentredString(
            largura / 2,
            y,
            "Estamparia dos Reis"
        )

        y -= 30

        c.setFont(
            "Helvetica-Bold",
            12
        )

        c.drawCentredString(
            largura / 2,
            y,
            "COMPROVANTE DE COMPRA"
        )

        y -= 40

        # Dados pedido

        c.setFont(
            "Helvetica",
            11
        )

        c.drawString(
            50,
            y,
            f"Pedido: {pedido[0]}"
        )

        y -= 20

        c.drawString(
            50,
            y,
            f"Cliente: {pedido[1]}"
        )

        y -= 20

        c.drawString(
            50,
            y,
            f"Telefone: {pedido[2]}"
        )

        y -= 20

        c.drawString(
            50,
            y,
            f"Data: {pedido[5]}"
        )

        y -= 35

        # Linha

        c.line(
            50,
            y,
            largura - 50,
            y
        )

        y -= 25

        # Cabeçalho itens

        c.setFont(
            "Helvetica-Bold",
            11
        )

        c.drawString(50, y, "Produto")
        c.drawString(320, y, "Qtd")
        c.drawString(390, y, "Valor")
        c.drawString(480, y, "Subtotal")

        y -= 15

        c.line(
            50,
            y,
            largura - 50,
            y
        )

        y -= 25

        c.setFont(
            "Helvetica",
            10
        )

        quantidade_total = 0

        for produto, quantidade, valor in itens:

            subtotal = quantidade * valor

            quantidade_total += quantidade

            c.drawString(
                50,
                y,
                str(produto)
            )

            c.drawString(
                320,
                y,
                str(quantidade)
            )

            c.drawString(
                390,
                y,
                f"R$ {valor:.2f}"
            )

            c.drawString(
                480,
                y,
                f"R$ {subtotal:.2f}"
            )

            y -= 20

            # Nova página se necessário

            if y < 100:

                c.showPage()

                y = altura - 50

        y -= 20

        c.line(
            50,
            y,
            largura - 50,
            y
        )

        y -= 30

        c.setFont(
            "Helvetica-Bold",
            11
        )

        c.drawString(
            50,
            y,
            f"Quantidade Total: {quantidade_total}"
        )

        y -= 20

        c.drawString(
            50,
            y,
            f"Valor Total: R$ {total:.2f}"
        )

        y -= 40

        c.setFont(
            "Helvetica",
            10
        )

        c.drawCentredString(
            largura / 2,
            y,
            "Obrigado pela preferência!"
        )

        y -= 20

        c.drawCentredString(
            largura / 2,
            y,
            datetime.now().strftime(
                "%d/%m/%Y %H:%M"
            )
        )

        c.save()

        return arquivo