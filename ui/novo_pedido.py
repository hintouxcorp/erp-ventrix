from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QMessageBox,
    QComboBox,
    QSpinBox,
    QDoubleSpinBox,
    QTableWidget,
    QTableWidgetItem,
    QHBoxLayout
)

from PyQt5.QtCore import pyqtSignal
from services.pedido_service import PedidoService


class NovoPedidoWindow(QWidget):
    pedido_salvo = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Novo Pedido")
        self.resize(800, 600)

        self.itens = []  # 🧺 carrinho

        self.setup_ui()

    # =========================
    # UI
    # =========================
    def setup_ui(self):

        layout = QVBoxLayout()

        # -------------------------
        # CLIENTE
        # -------------------------
        self.cliente_input = QLineEdit()
        self.telefone_input = QLineEdit()

        layout.addWidget(QLabel("Cliente"))
        layout.addWidget(self.cliente_input)

        layout.addWidget(QLabel("Telefone"))
        layout.addWidget(self.telefone_input)

        # -------------------------
        # ITEM DO CARRINHO
        # -------------------------
        self.produto_input = QLineEdit()

        self.quantidade_input = QSpinBox()
        self.quantidade_input.setMinimum(1)

        self.valor_input = QDoubleSpinBox()
        self.valor_input.setMaximum(999999)

        self.custo_input = QDoubleSpinBox()
        self.custo_input.setMaximum(999999)

        self.desconto_tipo = QComboBox()

        self.desconto_tipo.addItems([
            "Nenhum",
            "Valor Fixo",
            "Percentual"
        ])

        self.desconto_valor = QDoubleSpinBox()
        self.desconto_valor.setMaximum(999999)

        item_layout = QHBoxLayout()

        # Produto
        produto_col = QVBoxLayout()
        produto_col.addWidget(QLabel("Produto"))
        produto_col.addWidget(self.produto_input)

        # Quantidade
        quantidade_col = QVBoxLayout()
        quantidade_col.addWidget(QLabel("Quantidade"))
        quantidade_col.addWidget(self.quantidade_input)

        # Valor
        valor_col = QVBoxLayout()
        valor_col.addWidget(QLabel("Valor Unitário"))
        valor_col.addWidget(self.valor_input)

        # Custo
        custo_col = QVBoxLayout()
        custo_col.addWidget(QLabel("Custo Unitário"))
        custo_col.addWidget(self.custo_input)

        item_layout.addLayout(produto_col, 4)
        item_layout.addLayout(quantidade_col, 1)
        item_layout.addLayout(valor_col, 1)
        item_layout.addLayout(custo_col, 1)

        layout.addLayout(item_layout)

        # botão adicionar item
        btn_add = QPushButton("Adicionar Item")
        btn_add.clicked.connect(self.adicionar_item)

        btn_layout = QHBoxLayout()

        btn_layout.addStretch()
        btn_layout.addWidget(btn_add)
        btn_layout.addStretch()

        layout.addLayout(btn_layout)

        # -------------------------
        # TABELA CARRINHO
        # -------------------------
        self.tabela_itens = QTableWidget()
        self.tabela_itens.setColumnCount(4)
        self.tabela_itens.setHorizontalHeaderLabels([
            "Produto",
            "Qtd",
            "Valor",
            "Total"
        ])

        layout.addWidget(self.tabela_itens)

        # =========================
        # DESCONTO + RESUMO
        # =========================

        resumo_layout = QHBoxLayout()

        # Tipo desconto
        tipo_layout = QVBoxLayout()
        tipo_layout.addWidget(QLabel("Tipo de Desconto"))
        tipo_layout.addWidget(self.desconto_tipo)

        # Valor desconto
        valor_layout = QVBoxLayout()
        valor_layout.addWidget(QLabel("Valor do Desconto"))
        valor_layout.addWidget(self.desconto_valor)

        # Subtotal
        subtotal_layout = QVBoxLayout()

        self.subtotal_label = QLabel("R$ 0,00")

        subtotal_layout.addWidget(QLabel("Subtotal"))
        subtotal_layout.addWidget(self.subtotal_label)

        # Desconto
        desconto_layout = QVBoxLayout()

        self.desconto_label = QLabel("R$ 0,00")

        desconto_layout.addWidget(QLabel("Desconto"))
        desconto_layout.addWidget(self.desconto_label)

        resumo_layout.addLayout(tipo_layout)
        resumo_layout.addLayout(valor_layout)
        resumo_layout.addLayout(subtotal_layout)
        resumo_layout.addLayout(desconto_layout)

        layout.addLayout(resumo_layout)

        # =========================
        # TOTAL FINAL
        # =========================

        self.total_label = QLabel("R$ 0,00")

        self.total_label.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #27ae60;
        """)

        layout.addWidget(QLabel("Total Final"))
        layout.addWidget(self.total_label)

        # -------------------------
        # ORIGEM
        # -------------------------
        self.origem_input = QComboBox()
        self.origem_input.addItems([
            "Shopee",
            "Instagram",
            "WhatsApp",
            "Facebook",
            "Outro"
        ])

        layout.addWidget(QLabel("Origem"))
        layout.addWidget(self.origem_input)

        # -------------------------
        # SALVAR
        # -------------------------
        btn_salvar = QPushButton("Salvar Pedido")
        btn_salvar.clicked.connect(self.salvar)
        layout.addWidget(btn_salvar)

        self.desconto_tipo.currentTextChanged.connect(
            self.calcular_totais
        )

        self.desconto_valor.valueChanged.connect(
            self.calcular_totais
        )

        self.setLayout(layout)
        self.calcular_totais()

    # =========================
    # CARRINHO
    # =========================
    def adicionar_item(self):

        produto = self.produto_input.text()
        qtd = self.quantidade_input.value()
        valor = self.valor_input.value()
        custo = self.custo_input.value()

        if not produto:
            QMessageBox.warning(self, "Erro", "Informe o produto")
            return

        item = {
            "produto": produto,
            "quantidade": qtd,
            "valor": valor,
            "custo": custo
        }

        self.itens.append(item)

        self.atualizar_tabela()
        self.limpar_campos()

    def calcular_totais(self):
        subtotal = sum(
            item["quantidade"] * item["valor"]
            for item in self.itens
        )

        desconto = 0

        if self.desconto_tipo.currentText() == "Valor Fixo":

            desconto = self.desconto_valor.value()

        elif self.desconto_tipo.currentText() == "Percentual":

            desconto = (
                subtotal *
                self.desconto_valor.value() / 100
            )

        total_final = max(
            0,
            subtotal - desconto
        )

        self.subtotal_label.setText(
            f"R$ {subtotal:.2f}"
        )

        self.desconto_label.setText(
            f"R$ {desconto:.2f}"
        )

        self.total_label.setText(
            f"R$ {total_final:.2f}"
        )

        self.total_pedido = total_final

    def atualizar_tabela(self):

        self.tabela_itens.setRowCount(len(self.itens))

        for row, item in enumerate(self.itens):

            total = item["quantidade"] * item["valor"]

            self.tabela_itens.setItem(row, 0, QTableWidgetItem(item["produto"]))
            self.tabela_itens.setItem(row, 1, QTableWidgetItem(str(item["quantidade"])))
            self.tabela_itens.setItem(row, 2, QTableWidgetItem(f"R$ {item['valor']:.2f}"))
            self.tabela_itens.setItem(row, 3, QTableWidgetItem(f"R$ {total:.2f}"))
        
        self.calcular_totais()

    def limpar_campos(self):
        self.produto_input.clear()
        self.quantidade_input.setValue(1)
        self.valor_input.setValue(0)
        self.custo_input.setValue(0)

    # =========================
    # SALVAR
    # =========================
    def salvar(self):

        if not self.itens:
            QMessageBox.warning(self, "Erro", "Adicione itens ao pedido")
            return

        codigo = PedidoService.criar_pedido(
            cliente=self.cliente_input.text(),
            telefone=self.telefone_input.text(),
            origem=self.origem_input.currentText(),
            itens=self.itens
        )

        self.pedido_salvo.emit()

        QMessageBox.information(
            self,
            "Sucesso",
            f"Pedido criado!\n\nCódigo: {codigo}"
        )

        self.close()