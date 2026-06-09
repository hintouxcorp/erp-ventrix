Markdown
# 🚀 Vendrix ERP

> Sistema de Planejamento de Recursos Empresariais (ERP) robusto, ágil e focado na eficiência operacional.

O **Vendrix** é uma solução completa para gerenciamento empresarial, unificando controle de estoque, serviços, finanças e clientes em uma interface limpa e intuitiva. Desenvolvido em Python, o projeto foi estruturado de forma modular para garantir escalabilidade e manutenibilidade.

---

## 🛠️ Tecnologias Utilizadas

O ecossistema do Vendrix foi construído utilizando as seguintes tecnologias:

*   **Linguagem Principal:** Python 3.8
*   **Interface Gráfica (GUI):** [PyQt5]
*   **Banco de Dados:** SQLite
*   **Empacotamento:** PyInstaller

---

## 📂 Estrutura do Projeto

A arquitetura do projeto é dividida em módulos organizados para separar as responsabilidades do sistema:

```text
vendrix/
├── database/        # Conexão com o banco de dados
├── models/          # Modelos de Pedidos
├── pdfs/            # Tarefa de criação de PDFs
├── services/        # Serviços de Emissão de Comprovantede de Compra
├── styles/          # Estilos da Aplicação
├── ui/              # Telas e componentes da interface gráfica
├── main.py          # Ponto de entrada do aplicativo
└── README.md        # Documentação do projeto