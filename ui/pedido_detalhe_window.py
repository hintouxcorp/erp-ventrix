from PyQt5.QtWidgets import (
    QDialog,
    QLabel,
    QVBoxLayout,
    QFrame,
    QScrollArea,
    QWidget,
    QMessageBox,
    QPushButton,
    QHBoxLayout
)
from PyQt5.QtCore import pyqtSignal
from services.comprovante_service import ComprovanteService
from services.pedido_service import PedidoService
from ui.editar_pedido_window import EditarPedidoWindow

class PedidoDetalheWindow(QDialog):
    pedido_excluido = pyqtSignal()
    pedido_editado = pyqtSignal()

    def __init__(self, pedido):
        super().__init__()

        self.pedido = pedido

        self.setWindowTitle("Detalhes do Pedido")
        self.resize(650, 550)
        self.setMinimumHeight(400)
        self.setMaximumHeight(650)

        self.setModal(True)

        self.setup_ui()

    def setup_ui(self):

        itens = self.pedido.get("itens", [])

        # =========================
        # CÁLCULOS ERP
        # =========================
        total_quantidade = sum(i["quantidade"] for i in itens)

        total_liquido = sum(
            i["valor_unitario"] * i["quantidade"]
            for i in itens
        )

        lucro_total = sum(
            (i["valor_unitario"] - i["custo_unitario"]) * i["quantidade"]
            for i in itens
        )

        # =========================
        # CONTAINER PRINCIPAL
        # =========================
        container = QWidget()
        main = QVBoxLayout(container)
        main.setSpacing(12)
        main.setContentsMargins(15, 15, 15, 15)

        # =========================
        # HEADER
        # =========================
        header = QFrame()
        header_layout = QVBoxLayout()

        header_title = QLabel("Pedido")
        header_title.setStyleSheet("font-size:14px; font-weight:bold;")

        header_layout.addWidget(header_title)
        header_layout.addWidget(QLabel(f"Código: {self.pedido['codigo']}"))
        header_layout.addWidget(QLabel(f"Cliente: {self.pedido['cliente']}"))

        header.setLayout(header_layout)
        header.setStyleSheet(self.card_style())

        # =========================
        # FINANCEIRO
        # =========================
        financeiro = QFrame()
        fin_layout = QVBoxLayout()

        fin_title = QLabel("Financeiro")
        fin_title.setStyleSheet("font-size:14px; font-weight:bold;")

        lucro_unit = lucro_total / total_quantidade if total_quantidade else 0

        label_valor = QLabel(f"Total vendido: R$ {total_liquido:.2f}")
        label_lucro_unit = QLabel(f"Lucro unit médio: R$ {lucro_unit:.2f}")
        label_lucro_total = QLabel(f"Lucro total: R$ {lucro_total:.2f}")

        if lucro_total >= 0:
            label_lucro_total.setStyleSheet(self.lucro_style())
        else:
            label_lucro_total.setStyleSheet(self.prejuizo_style())

        fin_layout.addWidget(fin_title)
        fin_layout.addWidget(label_valor)
        fin_layout.addWidget(label_lucro_unit)
        fin_layout.addWidget(label_lucro_total)

        financeiro.setLayout(fin_layout)
        financeiro.setStyleSheet(self.card_style())

        # =========================
        # RESUMO
        # =========================
        resumo = QFrame()
        res_layout = QVBoxLayout()

        res_title = QLabel("Resumo")
        res_title.setStyleSheet("font-size:14px; font-weight:bold;")

        label_total = QLabel(f"Total líquido: R$ {total_liquido:.2f}")
        label_qtd = QLabel(f"Quantidade: {total_quantidade}")

        label_total.setStyleSheet("font-size:16px; font-weight:bold;")

        res_layout.addWidget(res_title)
        res_layout.addWidget(label_total)
        res_layout.addWidget(label_qtd)

        resumo.setLayout(res_layout)
        resumo.setStyleSheet(self.card_style())

        # =========================
        # DETALHES
        # =========================
        detalhes = QFrame()
        det_layout = QVBoxLayout()

        det_title = QLabel("Detalhes")
        det_title.setStyleSheet("font-size:14px; font-weight:bold;")

        det_layout.addWidget(det_title)
        det_layout.addWidget(QLabel(f"Origem: {self.pedido['origem']}"))
        det_layout.addWidget(QLabel(f"Status: {self.pedido['status']}"))
        det_layout.addWidget(QLabel(f"Data: {self.pedido['data_criacao']}"))

        detalhes.setLayout(det_layout)
        detalhes.setStyleSheet(self.card_style())

        # =========================
        # ADD CARDS
        # =========================
        main.addWidget(header)
        main.addWidget(financeiro)
        main.addWidget(resumo)
        main.addWidget(detalhes)

        # =========================
        # BOTÕES
        # =========================

        btn_editar = QPushButton("Editar Pedido")

        btn_editar.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 6px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #2980b9;
            }
        """)

        btn_excluir = QPushButton("Excluir Pedido")

        btn_excluir.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 6px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #c0392b;
            }
        """)

        btn_editar.clicked.connect(
            self.editar_pedido
        )

        btn_excluir.clicked.connect(
            self.excluir_pedido
        )

        botoes = QHBoxLayout()

        botoes.addWidget(btn_editar)
        botoes.addWidget(btn_excluir)

        main.addLayout(botoes)

        btn_comprovante = QPushButton(
            "📄 Gerar Comprovante"
        )

        btn_comprovante.clicked.connect(
            self.gerar_comprovante
        )

        main.addWidget(btn_comprovante)

        # =========================
        # SCROLL AREA
        # =========================
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(container)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background: #f4f6f8;
            }
        """)

        layout_final = QVBoxLayout()
        layout_final.addWidget(scroll)

        self.setLayout(layout_final)

        # =========================
        # GLOBAL STYLE
        # =========================
        self.setStyleSheet("""
            QDialog {
                background-color: #f4f6f8;
            }

            QLabel {
                font-size: 13px;
                color: #2c3e50;
            }
        """)

    def editar_pedido(self):

        self.janela_editar = EditarPedidoWindow(
            self.pedido
        )

        self.janela_editar.pedido_editado.connect(
            self.accept
        )

        self.janela_editar.exec_()
    
    def excluir_pedido(self):

        resposta = QMessageBox.question(
            self,
            "Confirmar exclusão",
            "Deseja realmente excluir este pedido?",
            QMessageBox.Yes | QMessageBox.No
        )

        if resposta != QMessageBox.Yes:
            return

        PedidoService.excluir_pedido(
            self.pedido["codigo"]
        )

        self.pedido_excluido.emit()
        QMessageBox.information(
            self,
            "Sucesso",
            "Pedido excluído com sucesso."
        )
        
        self.accept()

    def gerar_comprovante(self):

        arquivo = ComprovanteService.gerar_pdf(
            self.pedido["codigo"]
        )

        if arquivo:

            QMessageBox.information(
                self,
                "Comprovante Gerado",
                f"Comprovante salvo com sucesso.\n\n{arquivo}"
            )

        else:

            QMessageBox.warning(
                self,
                "Erro",
                "Não foi possível gerar o comprovante."
            )

    # =========================
    # STYLES
    # =========================
    def card_style(self):
        return """
            QFrame {
                background-color: white;
                border-radius: 10px;
                padding: 12px;
            }
        """

    def lucro_style(self):
        return """
            font-size: 16px;
            font-weight: bold;
            color: #27ae60;
        """

    def prejuizo_style(self):
        return """
            font-size: 16px;
            font-weight: bold;
            color: #e74c3c;
        """