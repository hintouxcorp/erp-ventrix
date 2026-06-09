from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QComboBox,
    QFrame,
    QMessageBox,
    QPushButton
)

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from services.pedido_service import PedidoService

from datetime import datetime
import os


class RelatoriosWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Relatórios")
        self.resize(1100, 700)

        self.setup_ui()

    def setup_ui(self):

        main = QVBoxLayout()
        main.setSpacing(15)
        main.setContentsMargins(15, 15, 15, 15)

        self.filtro = QComboBox()
        self.filtro.addItems(["Tudo", "Hoje", "7 dias"])
        self.filtro.currentTextChanged.connect(self.atualizar)

        main.addWidget(QLabel("Filtro de período"))
        main.addWidget(self.filtro)

        # =========================
        # PRIMEIRA LINHA DE CARDS
        # =========================

        self.card_pedidos = self.criar_card("Pedidos")
        self.card_faturamento = self.criar_card("Faturamento")
        self.card_lucro = self.criar_card("Lucro")
        self.card_ticket = self.criar_card("Ticket Médio")

        cards1 = QHBoxLayout()

        cards1.addWidget(self.card_pedidos)
        cards1.addWidget(self.card_faturamento)
        cards1.addWidget(self.card_lucro)
        cards1.addWidget(self.card_ticket)

        main.addLayout(cards1)

        # =========================
        # SEGUNDA LINHA DE CARDS
        # =========================

        self.card_quantidade = self.criar_card("Qtd. Vendida")
        self.card_lucro_medio = self.criar_card("Lucro Médio")
        self.card_valor_unidade = self.criar_card("Valor/Unidade")

        cards2 = QHBoxLayout()

        cards2.addWidget(self.card_quantidade)
        cards2.addWidget(self.card_lucro_medio)
        cards2.addWidget(self.card_valor_unidade)

        main.addLayout(cards2)

        # =========================
        # GRÁFICO
        # =========================

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        main.addWidget(self.canvas)

        self.btn_pdf = QPushButton("Exportar PDF")
        self.btn_pdf.clicked.connect(self.exportar_pdf)

        main.addWidget(self.btn_pdf)

        self.setLayout(main)

        self.atualizar()

    def criar_card(self, titulo):

        frame = QFrame()

        layout = QVBoxLayout()

        label_title = QLabel(titulo)
        label_value = QLabel("0")

        label_title.setStyleSheet("""
            font-size: 13px;
            color: #7f8c8d;
        """)

        label_value.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #2c3e50;
        """)

        layout.addWidget(label_title)
        layout.addWidget(label_value)

        frame.setLayout(layout)

        frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                padding: 12px;
            }
        """)

        frame.value_label = label_value

        return frame

    def atualizar(self):

        filtro = self.filtro.currentText()

        pedidos = PedidoService.total_pedidos()
        faturamento = PedidoService.faturamento_liquido()
        lucro = PedidoService.faturamento_lucro()

        quantidade_total = PedidoService.quantidade_total()

        ticket = (
            faturamento / pedidos
            if pedidos > 0 else 0
        )

        lucro_medio = (
            lucro / pedidos
            if pedidos > 0 else 0
        )

        valor_unidade = (
            faturamento / quantidade_total
            if quantidade_total > 0 else 0
        )

        self.card_pedidos.value_label.setText(
            str(pedidos)
        )

        self.card_faturamento.value_label.setText(
            f"R$ {faturamento:.2f}"
        )

        self.card_lucro.value_label.setText(
            f"R$ {lucro:.2f}"
        )

        self.card_ticket.value_label.setText(
            f"R$ {ticket:.2f}"
        )

        self.card_quantidade.value_label.setText(
            str(quantidade_total)
        )

        self.card_lucro_medio.value_label.setText(
            f"R$ {lucro_medio:.2f}"
        )

        self.card_valor_unidade.value_label.setText(
            f"R$ {valor_unidade:.2f}"
        )

        self.atualizar_grafico(filtro)

    def exportar_pdf(self):

        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas

        pedidos = PedidoService.total_pedidos()
        faturamento = PedidoService.faturamento_liquido()
        lucro = PedidoService.faturamento_lucro()
        quantidade_total = PedidoService.quantidade_total()

        ticket = (
            faturamento / pedidos
            if pedidos > 0 else 0
        )

        lucro_medio = (
            lucro / pedidos
            if pedidos > 0 else 0
        )

        valor_unidade = (
            faturamento / quantidade_total
            if quantidade_total > 0 else 0
        )

        pasta = "relatorios"
        os.makedirs(pasta, exist_ok=True)

        nome = (
            f"{pasta}/relatorio_"
            f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        )

        c = canvas.Canvas(nome, pagesize=A4)

        width, height = A4

        c.setFont("Helvetica-Bold", 16)
        c.drawString(
            50,
            height - 50,
            "RELATÓRIO DE VENDAS - ESTAMPARIA DOS REIS"
        )

        c.setFont("Helvetica", 10)

        c.drawString(
            50,
            height - 70,
            f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}"
        )

        y = height - 120

        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, "Resumo Geral")

        y -= 30

        c.setFont("Helvetica", 11)

        c.drawString(50, y, f"Pedidos: {pedidos}")
        y -= 20

        c.drawString(
            50,
            y,
            f"Faturamento: R$ {faturamento:.2f}"
        )
        y -= 20

        c.drawString(
            50,
            y,
            f"Lucro: R$ {lucro:.2f}"
        )
        y -= 20

        c.drawString(
            50,
            y,
            f"Ticket Médio: R$ {ticket:.2f}"
        )
        y -= 20

        c.drawString(
            50,
            y,
            f"Quantidade Vendida: {quantidade_total}"
        )
        y -= 20

        c.drawString(
            50,
            y,
            f"Lucro Médio por Pedido: R$ {lucro_medio:.2f}"
        )
        y -= 20

        c.drawString(
            50,
            y,
            f"Valor Médio por Unidade: R$ {valor_unidade:.2f}"
        )

        c.save()

        QMessageBox.information(
            self,
            "Exportação concluída",
            f"Relatório salvo com sucesso!\n\n{nome}"
        )

    def atualizar_grafico(self, filtro):

        self.figure.clear()

        ax = self.figure.add_subplot(111)

        dados = PedidoService.vendas_por_dia()

        dias = list(dados.keys())

        faturamento = [
            v["faturamento"]
            for v in dados.values()
        ]

        lucro = [
            v["lucro"]
            for v in dados.values()
        ]

        ax.plot(
            dias,
            faturamento,
            label="Faturamento",
            marker="o"
        )

        ax.plot(
            dias,
            lucro,
            label="Lucro",
            marker="o"
        )

        ax.set_title("Evolução de Vendas")
        ax.set_ylabel("R$")
        ax.legend()

        ax.grid(True, alpha=0.3)

        self.canvas.draw()