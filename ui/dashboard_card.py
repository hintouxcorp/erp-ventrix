from PyQt5.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout
)


class DashboardCard(QFrame):

    def __init__(self, titulo, valor):
        super().__init__()

        self.setObjectName("card")

        layout = QVBoxLayout()

        self.titulo = QLabel(titulo)
        self.valor = QLabel(str(valor))

        self.titulo.setObjectName("card_title")
        self.valor.setObjectName("card_value")

        layout.addWidget(self.titulo)
        layout.addWidget(self.valor)

        self.setLayout(layout)
    
    def atualizar_valor(self, valor):
        self.valor.setText(str(valor))
