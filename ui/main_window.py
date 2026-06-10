from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QFrame,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView
)

from ui.novo_pedido import NovoPedidoWindow
from ui.pedidos_window import PedidosWindow
from ui.pedido_detalhe_window import PedidoDetalheWindow
from ui.relatorios_window import RelatoriosWindow

from ui.dashboard_card import DashboardCard
from services.pedido_service import PedidoService


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Vendrix")
        self.resize(1200, 700)

        self.novo_pedido_window = None
        self.pedidos_window = None
        self.relatorios_window = None

        self.setup_ui()

    # =========================
    # UI
    # =========================
    def setup_ui(self):

        central = QWidget()
        self.setCentralWidget(central)

        layout_principal = QHBoxLayout()

        # =========================
        # MENU
        # =========================
        menu = QFrame()
        menu.setFixedWidth(220)

        menu_layout = QVBoxLayout()

        titulo = QLabel("VENDRIX")
        titulo.setObjectName("titulo")

        btn_novo = QPushButton("Novo Pedido")
        btn_pedidos = QPushButton("Pedidos")
        btn_relatorios = QPushButton("Relatórios")

        btn_novo.clicked.connect(self.abrir_novo_pedido)
        btn_pedidos.clicked.connect(self.abrir_pedidos)
        btn_relatorios.clicked.connect(self.abrir_relatorios)

        menu_layout.addWidget(titulo)
        menu_layout.addSpacing(20)
        menu_layout.addWidget(btn_novo)
        menu_layout.addWidget(btn_pedidos)
        menu_layout.addWidget(btn_relatorios)
        menu_layout.addStretch()

        menu.setLayout(menu_layout)

        # =========================
        # CONTEÚDO
        # =========================
        self.content = QWidget()
        content_layout = QVBoxLayout()

        dashboard = self.criar_dashboard()
        content_layout.addLayout(dashboard)

        titulo_pedidos = QLabel("Últimos Pedidos")
        titulo_pedidos.setObjectName("titulo_secao")
        content_layout.addWidget(titulo_pedidos)

        # =========================
        # TABELA
        # =========================
        self.tabela_ultimos = QTableWidget()
        self.tabela_ultimos.setColumnCount(6)

        self.tabela_ultimos.setHorizontalHeaderLabels([
            "Código",
            "Cliente",
            "Produto",
            "Quantidade",
            "Total Líquido",
            "Lucro Total",
        ])

        header = self.tabela_ultimos.horizontalHeader()

        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)

        self.tabela_ultimos.cellDoubleClicked.connect(self.abrir_detalhe_pedido)

        self.carregar_ultimos_pedidos()

        content_layout.addWidget(self.tabela_ultimos)

        self.content.setLayout(content_layout)

        layout_principal.addWidget(menu)
        layout_principal.addWidget(self.content)

        central.setLayout(layout_principal)

    # =========================
    # DETALHE
    # =========================
    def abrir_detalhe_pedido(self, row, column):

        pedidos = PedidoService.ultimos_pedidos()
        pedido = pedidos[row]

        self.janela_detalhe = PedidoDetalheWindow(pedido)
        self.janela_detalhe.pedido_editado.connect(
            self.atualizar_dashboard
        )
        self.janela_detalhe.pedido_excluido.connect(
            self.atualizar_dashboard
        )
        self.janela_detalhe.show()

    # =========================
    # NOVO PEDIDO
    # =========================
    def abrir_novo_pedido(self):

        self.novo_pedido_window = NovoPedidoWindow()

        self.novo_pedido_window.pedido_salvo.connect(
            self.atualizar_dashboard
        )

        self.novo_pedido_window.show()

    # =========================
    # DASHBOARD UPDATE
    # =========================
    def atualizar_dashboard(self):

        self.card_pedidos.atualizar_valor(
            PedidoService.total_pedidos()
        )

        self.card_faturamento_liquido.atualizar_valor(
            f"R$ {PedidoService.faturamento_liquido():.2f}"
        )

        self.card_faturamento_lucro.atualizar_valor(
            f"R$ {PedidoService.faturamento_lucro():.2f}"
        )

        self.card_hoje.atualizar_valor(
            PedidoService.pedidos_hoje()
        )

        self.card_origem.atualizar_valor(
            PedidoService.melhor_origem()
        )

        self.carregar_ultimos_pedidos()

    # =========================
    # PEDIDOS
    # =========================
    def abrir_pedidos(self):

        self.pedidos_window = PedidosWindow()
        self.pedidos_window.show()

    # =========================
    # RELATÓRIOS
    # =========================
    def abrir_relatorios(self):

        self.relatorios_window = RelatoriosWindow()
        self.relatorios_window.show()

    # =========================
    # DASHBOARD
    # =========================
    def criar_dashboard(self):

        pedidos = PedidoService.total_pedidos()

        faturamento_liquido = PedidoService.faturamento_liquido()
        faturamento_lucro = PedidoService.faturamento_lucro()

        pedidos_hoje = PedidoService.pedidos_hoje()
        melhor_origem = PedidoService.melhor_origem()

        layout = QHBoxLayout()

        self.card_pedidos = DashboardCard(
            "Pedidos",
            pedidos
        )

        self.card_faturamento_liquido = DashboardCard(
            "Faturamento Líquido",
            f"R$ {faturamento_liquido:.2f}"
        )

        self.card_faturamento_lucro = DashboardCard(
            "Faturamento Lucro",
            f"R$ {faturamento_lucro:.2f}"
        )

        self.card_hoje = DashboardCard(
            "Hoje",
            pedidos_hoje
        )

        self.card_origem = DashboardCard(
            "Melhor Canal",
            melhor_origem
        )

        layout.addWidget(self.card_pedidos, 1)
        layout.addWidget(self.card_faturamento_liquido, 1)
        layout.addWidget(self.card_faturamento_lucro, 1)
        layout.addWidget(self.card_hoje, 1)
        layout.addWidget(self.card_origem, 1)

        return layout

    # =========================
    # TABELA
    # =========================
    def carregar_ultimos_pedidos(self):

        self.tabela_ultimos.clearContents()

        pedidos = PedidoService.ultimos_pedidos()

        self.tabela_ultimos.setRowCount(len(pedidos))

        for row, pedido in enumerate(pedidos):

            total_liquido = sum(
                float(i["valor_unitario"]) * int(i["quantidade"])
                for i in pedido["itens"]
            )

            lucro_total = sum(
                (
                    float(i["valor_unitario"])
                    - float(i["custo_unitario"])
                ) * int(i["quantidade"])
                for i in pedido["itens"]
            )

            quantidade_total = sum(
                int(i["quantidade"])
                for i in pedido["itens"]
            )

            self.tabela_ultimos.setItem(row, 0, QTableWidgetItem(pedido["codigo"]))
            self.tabela_ultimos.setItem(row, 1, QTableWidgetItem(pedido["cliente"]))
            self.tabela_ultimos.setItem(row, 2, QTableWidgetItem(", ".join(i["produto"] for i in pedido["itens"])))
            self.tabela_ultimos.setItem(row, 3, QTableWidgetItem(str(quantidade_total)))
            self.tabela_ultimos.setItem(row, 4, QTableWidgetItem(f"R$ {total_liquido:.2f}"))
            self.tabela_ultimos.setItem(row, 5, QTableWidgetItem(f"R$ {lucro_total:.2f}"))