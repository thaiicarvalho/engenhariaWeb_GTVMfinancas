# GTVM Finanças

## Descrição do Projeto

Este repositório contém o projeto desenvolvido para a disciplina de Engenharia Web. Trata-se de um sistema web de controle financeiro pessoal, no qual é possível registrar receitas e despesas, acompanhar metas de investimento e visualizar relatórios com gráficos.

O objetivo do trabalho é praticar conceitos de desenvolvimento web, como rotas, templates, persistência de dados com ORM e operações CRUD.

## Estrutura do Projeto

* `app.py`: rotas e regras de negócio da aplicação.
* `models.py`: modelos do banco de dados (`Lancamento` e `Investimento`).
* `templates/`: páginas HTML (Jinja2).
* `static/css/`: estilos de cada página.
* `static/js/`: scripts do front-end.
* `requirements.txt`: dependências do projeto.

## Requisitos

* Python 3.12 ou superior
* Banco de dados PostgreSQL
* Bibliotecas listadas em `requirements.txt` (Flask, Flask-SQLAlchemy, psycopg, python-dotenv)

## Funcionalidades do Sistema

* Menu principal com saldo atual e gráficos de gasto x não gasto e de despesas emergenciais x não emergenciais.
* Cadastro, edição e exclusão de lançamentos (receitas e despesas), com filtro por categoria.
* Relatórios com total de receitas, despesas, saldo final e gastos por categoria, com filtros por período, mês e ano.
* Cadastro, edição e exclusão de metas de investimento, com acompanhamento das metas concluídas e em andamento.

## Como Rodar

1. Clone o repositório:

```
git clone https://github.com/thaiicarvalho/engenhariaWeb_GTVMfinancas.git
```

2. Crie e ative um ambiente virtual:

```
python -m venv venv
venv\Scripts\activate
```

3. Instale as dependências:

```
pip install -r requirements.txt
```

4. Crie um arquivo `.env` na raiz do projeto com a conexão do banco:

```
DATABASE_URL=postgresql+psycopg://usuario:senha@localhost:5432/nome_do_banco
```

5. Execute a aplicação e acesse `http://localhost:5000`:

```
python app.py
```

## Observações

* Projeto desenvolvido para a disciplina de Engenharia Web.
* As tabelas do banco são criadas automaticamente na primeira execução.

## Licença

Projeto destinado apenas para fins educacionais.
