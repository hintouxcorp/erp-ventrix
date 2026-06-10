from PyQt5.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QComboBox,
    QPushButton,
    QMessageBox
)

from PyQt5.QtCore import pyqtSignal
from services.pedido_service import PedidoService

class EditarPedidoWindow(QDialog):

    pedido_editado = pyqtSignal()

    def __init__(self, pedido):
        super().__init__()

        self.pedido = pedido

        self.setWindowTitle("Editar Pedido")
        self.resize(450, 350)

        self.setup_ui()

    def setup_ui(self):

        layout = QVBoxLayout()

        # Cliente
        layout.addWidget(QLabel("Cliente"))

        self.cliente_input = QLineEdit(
            self.pedido["cliente"]
        )

        layout.addWidget(
            self.cliente_input
        )

        # Telefone
        layout.addWidget(QLabel("Telefone"))

        self.telefone_input = QLineEdit(
            self.pedido["telefone"]
        )

        layout.addWidget(
            self.telefone_input
        )

        # Origem
        layout.addWidget(QLabel("Origem"))

        self.origem_input = QComboBox()

        self.origem_input.addItems([
            "Shopee",
            "Instagram",
            "WhatsApp",
            "Facebook",
            "Outro"
        ])

        self.origem_input.setCurrentText(
            self.pedido["origem"]
        )

        layout.addWidget(
            self.origem_input
        )

        # Status
        layout.addWidget(QLabel("Status"))

        self.status_input = QComboBox()

        self.status_input.addItems([
            "PAGO",
            "ENVIADO",
            "ENTREGUE",
            "CANCELADO"
        ])

        self.status_input.setCurrentText(
            self.pedido["status"]
        )

        layout.addWidget(
            self.status_input
        )

        # Botão salvar
        btn_salvar = QPushButton(
            "Salvar Alterações"
        )

        btn_salvar.clicked.connect(
            self.salvar
        )

        layout.addWidget(
            btn_salvar
        )

        self.setLayout(layout)

    def salvar(self):

        PedidoService.editar_pedido(
            codigo=self.pedido["codigo"],
            cliente=self.cliente_input.text(),
            telefone=self.telefone_input.text(),
            origem=self.origem_input.currentText(),
            status=self.status_input.currentText()
        )

        self.pedido_editado.emit()

        QMessageBox.information(
            self,
            "Sucesso",
            "Pedido atualizado com sucesso."
        )

        self.close()