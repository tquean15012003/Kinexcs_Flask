from ..utils import db
from datetime import datetime

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer(), primary_key=True)
    item_name = db.Column(db.String(255), nullable=False)
    item_price = db.Column(db.Float(), nullable=False)
    customer_id = db.Column(db.Integer(), db.ForeignKey('customers.id'), nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return self.name

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()