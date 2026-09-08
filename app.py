import os
from dotenv import load_dotenv

load_dotenv()

from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import extract
from models import db, Lancamento, Investimento
from collections import defaultdict
from datetime import datetime

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/")
def home():

    lancamentos = Lancamento.query.all()

    total_receitas = 0

    total_despesas = 0

    total_emergencial = 0

    total_nao_emergencial = 0

    # =========================
    # LEITURA DOS LANÇAMENTOS
    # =========================

    for lancamento in lancamentos:

        # RECEITA
        if lancamento.tipo == "Receita":

            total_receitas += lancamento.valor

        # DESPESA EMERGENCIAL
        elif lancamento.tipo == "Despesa Emergencial":

            total_despesas += lancamento.valor

            total_emergencial += lancamento.valor

        # DESPESA NORMAL
        else:

            total_despesas += lancamento.valor

            total_nao_emergencial += lancamento.valor

    # =========================
    # SALDO FINAL
    # =========================

    saldo = total_receitas - total_despesas

    # =========================
    # GRÁFICO 1
    # GASTO vs NÃO GASTO
    # =========================

    total_movimentado = (
        total_receitas +
        total_despesas
    )

    if total_movimentado > 0:

        porcentagem_gasto = (
            total_despesas /
            total_movimentado
        ) * 100

        porcentagem_nao_gasto = (
            total_receitas /
            total_movimentado
        ) * 100

    else:

        porcentagem_gasto = 0

        porcentagem_nao_gasto = 0

    # =========================
    # GRÁFICO 2
    # EMERGENCIAL
    # =========================

    total_despesas_geral = (
        total_emergencial +
        total_nao_emergencial
    )

    if total_despesas_geral > 0:

        porcentagem_emergencial = (
            total_emergencial /
            total_despesas_geral
        ) * 100

        porcentagem_nao_emergencial = (
            total_nao_emergencial /
            total_despesas_geral
        ) * 100

    else:

        porcentagem_emergencial = 0

        porcentagem_nao_emergencial = 0

    return render_template(

        "index.html",

        saldo=saldo,

        porcentagem_gasto=porcentagem_gasto,

        porcentagem_nao_gasto=porcentagem_nao_gasto,

        porcentagem_emergencial=porcentagem_emergencial,

        porcentagem_nao_emergencial=porcentagem_nao_emergencial
    )

@app.route("/investimentos")
def investimentos():

    investimentos = Investimento.query.all()

    # =========================
    # TOTAL INVESTIDO
    # =========================

    total_investido = sum(
        i.valor_investido
        for i in investimentos
    )

    # =========================
    # TOTAL DAS METAS
    # =========================

    total_metas = sum(
        i.meta
        for i in investimentos
    )

    # =========================
    # METAS CONCLUÍDAS
    # =========================

    metas_concluidas = len([
        i for i in investimentos
        if i.valor_investido >= i.meta
    ])

    # =========================
    # METAS EM ANDAMENTO
    # =========================

    metas_andamento = len([
        i for i in investimentos
        if i.valor_investido < i.meta
    ])

    return render_template(
        "investimentos.html",

        investimentos=investimentos,

        total_investido=total_investido,
        total_metas=total_metas,

        metas_concluidas=metas_concluidas,
        metas_andamento=metas_andamento
    )


@app.route("/adicionar-investimento", methods=["POST"])
def adicionar_investimento():

    descricao = request.form.get("descricao")

    meta = float(
        request.form.get("meta")
    )

    valor_investido = float(
        request.form.get("valor_investido")
    )

    novo_investimento = Investimento(

        descricao=descricao,

        meta=meta,

        valor_investido=valor_investido
    )

    db.session.add(novo_investimento)

    db.session.commit()

    return redirect(
        url_for("investimentos")
    )

@app.route("/excluir-investimento/<int:id>")
def excluir_investimento(id):

    investimento = Investimento.query.get_or_404(id)

    db.session.delete(investimento)

    db.session.commit()

    return redirect(
        url_for("investimentos")
    )

@app.route("/editar-investimento/<int:id>",
           methods=["GET", "POST"])
def editar_investimento(id):

    investimento = Investimento.query.get_or_404(id)

    if request.method == "POST":

        investimento.descricao = request.form.get("descricao")

        investimento.meta = float(
            request.form.get("meta")
        )

        investimento.valor_investido = float(
            request.form.get("valor_investido")
        )

        db.session.commit()

        return redirect(
            url_for("investimentos")
        )

    return render_template(
        "editar_investimento.html",
        investimento=investimento
    )

@app.route("/atualizar-investimento/<int:id>", methods=["POST"])
def atualizar_investimento(id):

    investimento = Investimento.query.get_or_404(id)

    investimento.descricao = request.form.get("descricao")

    investimento.meta = float(
        request.form.get("meta")
    )

    investimento.valor_investido = float(
        request.form.get("valor_investido")
    )

    db.session.commit()

    return redirect(
        url_for("investimentos")
    )

@app.route("/lancamentos")
def lancamentos():

    categoria = request.args.get("categoria")

    if categoria and categoria != "Todas as categorias":

        lista_lancamentos = Lancamento.query.filter_by(
            categoria=categoria
        ).all()

    else:

        lista_lancamentos = Lancamento.query.all()

    return render_template(
        "lancamentos.html",
        lancamentos=lista_lancamentos
    )
@app.route("/adicionar-lancamento", methods=["POST"])
def adicionar_lancamento():

    tipo = request.form["tipo"]
    descricao = request.form["descricao"]
    valor = float(request.form["valor"])
    categoria = request.form["categoria"]

    data = datetime.strptime(
        request.form["data"],
        "%Y-%m-%d"
    )

    novo_lancamento = Lancamento(
        tipo=tipo,
        descricao=descricao,
        valor=valor,
        categoria=categoria,
        data=data
    )

    db.session.add(novo_lancamento)
    db.session.commit()

    origem = request.form.get("origem")

    if origem == "home":
        return redirect(url_for("home"))

    return redirect(url_for("lancamentos"))


@app.route("/editar-lancamento/<int:id>")
def editar_lancamento(id):

    lancamento = Lancamento.query.get_or_404(id)

    return render_template(
        "editar_lancamento.html",
        lancamento=lancamento
    )

@app.route("/atualizar-lancamento/<int:id>", methods=["POST"])
def atualizar_lancamento(id):

    lancamento = Lancamento.query.get_or_404(id)

    lancamento.tipo = request.form["tipo"]
    lancamento.descricao = request.form["descricao"]
    lancamento.valor = float(request.form["valor"])
    lancamento.categoria = request.form["categoria"]
    lancamento.data = request.form["data"]

    db.session.commit()

    return redirect(url_for("lancamentos"))

@app.route("/excluir-lancamento/<int:id>")
def excluir_lancamento(id):

    lancamento = Lancamento.query.get_or_404(id)

    db.session.delete(lancamento)

    db.session.commit()

    return redirect(url_for("lancamentos"))

@app.route("/relatorios")
def relatorios():

    # =========================
    # PEGAR FILTROS DA URL
    # =========================

    data_inicial = request.args.get("data_inicial")
    data_final = request.args.get("data_final")
    mes = request.args.get("mes")
    ano = request.args.get("ano")

    # =========================
    # QUERY BASE
    # =========================

    query = Lancamento.query

    # =========================
    # FILTRO POR DATA
    # =========================

    if data_inicial:
        query = query.filter(Lancamento.data >= data_inicial)

    if data_final:
        query = query.filter(Lancamento.data <= data_final)

    # =========================
    # FILTRO POR MÊS
    # =========================

    if mes and mes != "Todos":
        query = query.filter(
            extract('month', Lancamento.data) == int(mes)
        )

    # =========================
    # FILTRO POR ANO
    # =========================

    if ano:
        query = query.filter(
            extract('year', Lancamento.data) == int(ano)
        )

    lancamentos = query.all()

    # =========================
    # CÁLCULOS FINANCEIROS
    # =========================

    total_receitas = sum(
        l.valor for l in lancamentos
        if l.tipo == "Receita"
    )

    total_despesas = sum(
        l.valor for l in lancamentos
        if l.tipo != "Receita"
    )

    saldo_final = total_receitas - total_despesas

    # =========================
    # GASTOS EMERGENCIAIS
    # =========================

    total_emergencial = sum(
        l.valor for l in lancamentos
        if l.tipo == "Despesa Emergencial"
    )

    if total_despesas > 0:
        porcentagem_emergencial = (
            total_emergencial / total_despesas
        ) * 100
    else:
        porcentagem_emergencial = 0

    # =========================
    # GASTOS POR CATEGORIA
    # =========================

    gastos_categoria = defaultdict(float)

    for l in lancamentos:

        if l.tipo != "Receita":
            gastos_categoria[l.categoria] += l.valor

    # =========================
    # PORCENTAGEM POR CATEGORIA
    # =========================

    cores = [
    "#5dd87a",
    "#f9a825",
    "#1a3d2b",
    "#e53935",
    "#2196f3",
    "#9c27b0",
    "#ff5722"
    ]

    categorias_formatadas = []

    circunferencia = 2 * 3.1416 * 66

    offset_atual = 0

    for i, (categoria, valor) in enumerate(gastos_categoria.items()):

        if total_despesas > 0:
            porcentagem = (valor / total_despesas) * 100
        else:
            porcentagem = 0

        tamanho_segmento = (
            porcentagem / 100
        ) * circunferencia

        restante = circunferencia - tamanho_segmento

        categorias_formatadas.append({
            "nome": categoria,
            "valor": valor,
            "porcentagem": porcentagem,
            "cor": cores[i % len(cores)],
            "dasharray": f"{tamanho_segmento} {restante}",
            "dashoffset": -offset_atual
        })

        offset_atual += tamanho_segmento

    return render_template(
        "relatorios.html",

        total_receitas=total_receitas,
        total_despesas=total_despesas,
        saldo_final=saldo_final,

        total_emergencial=total_emergencial,
        porcentagem_emergencial=porcentagem_emergencial,

        categorias=categorias_formatadas
    )
if __name__ == "__main__":
    app.run(debug=True)