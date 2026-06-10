import sys, os
from PyQt5.QtWidgets import QApplication
from database.connection import create_tables
from ui.main_window import MainWindow

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

create_tables()

app = QApplication(sys.argv)

with open(
    resource_path("styles/dark.qss"),
    "r",
    encoding="utf-8"
) as file:
    app.setStyleSheet(file.read())

window = MainWindow()
window.show()

sys.exit(app.exec_())