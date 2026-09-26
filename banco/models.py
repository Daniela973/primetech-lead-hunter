from datetime import datetime
from banco.database import db

class Lead(db.Model):
    __tablename__ = 'leads'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    segmento = db.Column(db.String(100), nullable=False)
    cidade = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(50))
    whatsapp = db.Column(db.String(50))
    website = db.Column(db.String(255))
    endereco = db.Column(db.String(255))
    
    # Redes Sociais
    instagram = db.Column(db.String(255))
    facebook = db.Column(db.String(255))
    linkedin = db.Column(db.String(255))
    
    origem = db.Column(db.String(100))
    data_captura = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Análise e Qualificação
    possui_site = db.Column(db.Boolean, default=False)
    site_funcionando = db.Column(db.Boolean, default=False)
    https = db.Column(db.Boolean, default=False)
    mobile = db.Column(db.Boolean, default=False)
    possui_instagram = db.Column(db.Boolean, default=False)
    
    pontuacao = db.Column(db.Integer, default=0)
    classificacao = db.Column(db.String(50), default='⚪ lead frio')
    status_crm = db.Column(db.String(50), default='novo lead')
