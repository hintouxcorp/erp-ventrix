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

        layout.addWidget(QLabel("Produto"))
        layout.addWidget(self.produto_input)

        layout.addWidget(QLabel("Quantidade"))
        layout.addWidget(self.quantidade_input)

        layout.addWidget(QLabel("Valor Unitário"))
        layout.addWidget(self.valor_input)

        layout.addWidget(QLabel("Custo Unitário"))
        layout.addWidget(self.custo_input)

        # botão adicionar item
        btn_add = QPushButton("Adicionar Item")
        btn_add.clicked.connect(self.adicionar_item)
        layout.addWidget(btn_add)

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

        self.setLayout(layout)

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

    def atualizar_tabela(self):

        self.tabela_itens.setRowCount(len(self.itens))

        for row, item in enumerate(self.itens):

            total = item["quantidade"] * item["valor"]

            self.tabela_itens.setItem(row, 0, QTableWidgetItem(item["produto"]))
            self.tabela_itens.setItem(row, 1, QTableWidgetItem(str(item["quantidade"])))
            self.tabela_itens.setItem(row, 2, QTableWidgetItem(f"R$ {item['valor']:.2f}"))
            self.tabela_itens.setItem(row, 3, QTableWidgetItem(f"R$ {total:.2f}"))

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