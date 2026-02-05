# FINLIN – Controle Financeiro Pessoal

O **FINLIN** é um aplicativo multiplataforma para **controle financeiro pessoal**, desenvolvido com **Flutter** no frontend e **FastAPI** no backend. O sistema permite o gerenciamento de contas, categorias e transações financeiras, além da visualização de relatórios mensais de entradas, saídas e saldo.

O projeto foi concebido com foco em **arquitetura moderna**, **segurança**, **boa experiência do usuário** e **portabilidade**, funcionando em **Web, Android (emulador e dispositivo físico)** e **Desktop**.

---

## 📌 Visão Geral

O FINLIN possibilita que usuários:
- Criem uma conta e façam login de forma segura
- Cadastrem contas bancárias
- Organizem categorias de receitas e despesas
- Registrem transações financeiras
- Visualizem relatórios mensais consolidados

A comunicação entre frontend e backend é feita via **API REST**, com autenticação baseada em **JWT (JSON Web Token)**.

---

## 🧰 Tecnologias Utilizadas

### Frontend
- **Flutter**
- **Material 3**
- Tema escuro moderno e consistente
- Compatível com Web, Android e Desktop

### Backend
- **FastAPI**
- **Python**
- **PostgreSQL**
- **SQLAlchemy (ORM)**
- **JWT para autenticação**
- **Uvicorn** como servidor ASGI


###Link para Download
https://www.mediafire.com/file/ieovctw70vxxgut/FinLIN_-_Controle_De_Finan%25C3%25A7as.apk/file

---

## ▶️ Como Rodar o Backend (FastAPI)

### Pré-requisitos
- Python 3.10+
- PostgreSQL configurado
- Ambiente virtual recomendado

### Passos
1. Instale as dependências:
   ```bash
   pip install -r requirements.txt
