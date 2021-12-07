from sqlalchemy.sql.sqltypes import String
from app.configs.database import db
from dataclasses import dataclass
import sqlalchemy

db: sqlalchemy = db


@dataclass
class Therapist(db.Model):
    id_medic: int
    nm_medic: str
    nr_cpf: str
    nr_crm: str
    ds_area: str
    nm_user: str
    ds_password: str
    fl_admin: str
    nr_access: int

    id_medic = db.Column(db.Integer, primary_key=True),
    nm_medic = db.Column(db.String(50), nullable=False),
    nr_cpf = db.Column(db.String(11), nullable=False),
    nr_crm = db.Column(db.String(15), nullable=False),
    ds_area = db.Column(db.String(20), nullable=False),
    nm_user = db.Column(db.String(15), nullable=False),
    ds_password = db.Column(db.String(15), nullable=False),
    fl_admin = db.Column(db.String(3), nullable=True),
    nr_access = db.Column(db.Integer, nullable=True)

    def __iter__(self):
        yield 'id_medico', self.id_medic
        yield 'nm_medico', self.nm_medic
        yield 'nr_cpf', self.nr_cpf
        yield 'nr_crm', self.nr_crm
        yield 'ds_area', self.ds_area
        yield 'nm_usuario', self.nm_user
        yield 'ds_senha', self.ds_password
        yield 'fl_admin', self.fl_admin
        yield 'nr_acessos', self.nr_access
