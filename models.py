import uuid
from extensions import db

class Fact(db.Model):
    __tablename__ = 'facts'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))  # Генерация UUID
    text = db.Column(db.String(50), nullable=False)