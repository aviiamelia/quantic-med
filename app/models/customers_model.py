from app.models.sessions_table_model import sessions
from datetime import date
from sqlalchemy.orm import backref, relationship
from app.configs.database import db
from dataclasses import dataclass
import sqlalchemy
db: sqlalchemy = db


@dataclass
class Customers(db.Model):
    id_paciente: int
    nm_paciente: str
    nr_cpf: str
    nr_rg: str
    nm_mae: str
    nm_pai: str
    nr_carteira: str
    ds_endereco: str
    nr_telefone_res: str
    nr_telefone_ces: str
    ds_email: str
    id_laudo: int
    dt_data_nasc: date

    id_paciente = db.Column(db.Integer, primary_key=True),
    nm_paciente = db.Column(db.String(50), nullable=False),
    nr_cpf = db.Column(db.String(11), nullable=False),
    nr_rg = db.Column(db.String(11), nullable=False),
    nm_mae = db.Column(db.String(50), nullable=True),
    nm_pai = db.Column(db.String(50), nullable=True),
    nr_carteira = db.Column(db.String(11), nullable=True),
    ds_endereco = db.Column(db.String(50), nullable=False),
    nr_telefone_res = db.Column(db.String(11), nullable=True),
    nr_telefone_ces = db.Column(db.String(11), nullable=True),
    ds_email = db.Column(db.String(50), nullable=True)
    id_laudo = db.Column(db.Integer, db.ForeignKey('LaudosModel.id_laudo')),
    dt_data_nasc = db.Column(db.Date, nullable=False)

    consultas = relationship(
        'TherapistModel',
        secondary=sessions,
        backref=backref('customers', uselist=False)
    )

    def __iter__(self):
        yield 'id_paciente', self.id_paciente
        yield 'nm_paciente', self.nm_paciente
        yield 'nr_cpf', self.nr_cpf
        yield 'nr_rg', self.nr_rg
        yield 'nm_mae', self.nm_mae
        yield 'nm_pai', self.nm_pai
        yield 'nr_carteira', self.nr_carteira
        yield 'ds_endereco', self.ds_endereco
        yield 'nr_telefone_res', self.nr_telefone_res
        yield 'nr_telefone_ces', self.nr_telefone_ces
        yield 'ds_email', self.ds_email
        yield 'id_laudo', self.id_laudo
        yield 'dt_data_nasc', self.dt_data_nasc
