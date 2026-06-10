import sqlite3
from pathlib import Path
import os

APP_DIR = Path(os.getenv("APPDATA")) / "Vendrix"

APP_DIR.mkdir(parents=True, exist_ok=True)

DB_PATH = APP_DIR / "vendrix.db"

APP_DIR = Path(os.getenv("APPDATA")) / "Vendrix"

RELATORIOS_DIR = APP_DIR / "relatorios"
COMPROVANTES_DIR = APP_DIR / "comprovantes"

APP_DIR.mkdir(parents=True, exist_ok=True)
RELATORIOS_DIR.mkdir(exist_ok=True)
COMPROVANTES_DIR.mkdir(exist_ok=True)


def get_connection():
    return sqlite3.connect(DB_PATH)


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # =========================
    # PEDIDOS (HEADER)
    # =========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pedidos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        codigo TEXT UNIQUE,
        cliente TEXT,
        telefone TEXT,
        desconto_tipo TEXT,
        desconto_valor REAL,
        origem TEXT,
        status TEXT,
        data_criacao TEXT
    )
    """)

    # =========================
    # ITENS DO PEDIDO (CARRINHO)
    # =========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pedido_itens (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pedido_codigo TEXT,
        produto TEXT,
        quantidade INTEGER,
        valor_unitario REAL,
        custo_unitario REAL
    )
    """)

    conn.commit()
    conn.close()