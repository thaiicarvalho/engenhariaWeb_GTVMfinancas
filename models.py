from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Lancamento(db.Model):
    __tablename__ = "lancamentos"

    id = db.Column(db.Integer, primary_key=True)

    tipo = db.Column(db.String(20), nullable=False)

    descricao = db.Column(db.String(200), nullable=False)

    valor = db.Column(db.Float, nullable=False)

    categoria = db.Column(db.String(50), nullable=False)

    data = db.Column(db.Date, nullable=False)

class Investimento(db.Model):

    __tablename__ = "investimentos"

    id = db.Column(db.Integer, primary_key=True)

    descricao = db.Column(db.String(200), nullable=False)

    meta = db.Column(db.Float, nullable=False)

    valor_investido = db.Column(db.Float, nullable=False)