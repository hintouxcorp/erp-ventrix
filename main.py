import sys

from PyQt5.QtWidgets import QApplication

from database.connection import create_tables
from ui.main_window import MainWindow


create_tables()

app = QApplication(sys.argv)

with open(
    "styles/dark.qss",
    "r",
    encoding="utf-8"
) as file:
    app.setStyleSheet(file.read())

window = MainWindow()
window.show()

sys.exit(app.exec_())