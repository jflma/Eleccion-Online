from app import db
from app import ma

class Candidato(db.Model):
    __tablename__ = 'candidato'
    id_candidato  = db.Column(db.Integer, primary_key=True)
    nombres = db.Column(db.String(100), nullable=False)
    apellido_paterno = db.Column(db.String(100), nullable=False)
    apellido_materno = db.Column(db.String(100), nullable=False)
    rol = db.Column(db.String(100), nullable=False)
    denegado = db.Column(db.Boolean, nullable=True, default=False)
    id_lista = db.Column(db.Integer, db.ForeignKey('listacandidato.id_lista'),nullable=True)
    
    def __init__(self, nombres, apellido_paterno, apellido_materno, rol, id_lista_canditado,denegado=False):
        self.nombres = nombres
        self.apellido_paterno = apellido_paterno
        self.apellido_materno = apellido_materno
        self.id_lista = id_lista_canditado
        self.denegado = denegado
        self.rol = rol

class CandidatoSchema(ma.Schema):
    class Meta:
        fields = (
            'id_candidato',
            'nombres',
            'apellido_paterno',
            'apellido_materno',
            'rol',
            'denegado',
            'id_lista'
        )