from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView
)

from services.pedido_service import PedidoService


class PedidosWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Pedidos")
        self.resize(900, 500)

        self.setup_ui()

    def setup_ui(self):

        self.table = QTableWidget()

        self.table.setColumnCount(6)

        self.table.setHorizontalHeaderLabels([
            "Código",
            "Cliente",
            "Produto",
            "Valor",
            "Status",
            "Data"
        ])

        header = self.table.horizontalHeader()

        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # Código
        header.setSectionResizeMode(1, QHeaderView.Stretch)           # Cliente
        header.setSectionResizeMode(2, QHeaderView.Stretch)           # Produto
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # Valor
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)  # Status
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)  # Data


        self.carregar_dados()

        layout = QVBoxLayout()
        layout.addWidget(self.table)

        self.setLayout(layout)

    def carregar_dados(self):

        pedidos = PedidoService.listar_pedidos()

        self.table.setRowCount(len(pedidos))

        for row, pedido in enumerate(pedidos):

            total_liquido = pedido.total_liquido
            lucro_total = pedido.lucro_total

            self.table.setItem(
                row, 0,
                QTableWidgetItem(pedido.codigo)
            )

            self.table.setItem(
                row, 1,
                QTableWidgetItem(pedido.cliente)
            )

            self.table.setItem(
                row, 2,
                QTableWidgetItem(pedido.produto)
            )


            self.table.setItem(
                row, 3,
                QTableWidgetItem(f"R$ {total_liquido:.2f}")
            )

            self.table.setItem(
                row, 4,
                QTableWidgetItem(pedido.status)
            )

            self.table.setItem(
                row, 5,
                QTableWidgetItem(pedido.data_criacao)
            )