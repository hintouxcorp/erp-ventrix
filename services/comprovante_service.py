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

                desconto_tipo,
                desconto_valor,

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
        # CALCULA TOTAIS
        # =========================

        subtotal = 0

        for item in itens:
            subtotal += item[1] * item[2]

        desconto_tipo = pedido[3]
        desconto_valor = pedido[4] or 0

        desconto = 0

        if desconto_tipo == "Valor Fixo":
            desconto = desconto_valor

        elif desconto_tipo == "Percentual":
            desconto = subtotal * desconto_valor / 100

        total = subtotal - desconto

        if total < 0:
            total = 0

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

        # =========================
        # TÍTULO
        # =========================

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

        # =========================
        # DADOS DO CLIENTE
        # =========================

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
            f"Data: {pedido[7]}"
        )

        y -= 35

        # =========================
        # LINHA
        # =========================

        c.line(
            50,
            y,
            largura - 50,
            y
        )

        y -= 25

        # =========================
        # CABEÇALHO ITENS
        # =========================

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

            subtotal_item = quantidade * valor

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
                f"R$ {subtotal_item:.2f}"
            )

            y -= 20

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

        # =========================
        # RESUMO FINANCEIRO
        # =========================

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
            f"Subtotal: R$ {subtotal:.2f}"
        )

        y -= 20

        if desconto > 0:

            if desconto_tipo == "Percentual":

                c.drawString(
                    50,
                    y,
                    f"Cupom Aplicado: {desconto_valor:.0f}% OFF"
                )

            else:

                c.drawString(
                    50,
                    y,
                    f"Cupom Aplicado: R$ {desconto_valor:.2f} OFF"
                )

            y -= 20

            c.drawString(
                50,
                y,
                f"Desconto: -R$ {desconto:.2f}"
            )

            y -= 20

        c.setFont(
            "Helvetica-Bold",
            12
        )

        c.drawString(
            50,
            y,
            f"Total Pago: R$ {total:.2f}"
        )

        y -= 40

        # =========================
        # RODAPÉ
        # =========================

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