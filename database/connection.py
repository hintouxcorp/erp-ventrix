import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "vendrix.db"


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