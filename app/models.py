from datetime import datetime
from app import db


class Discount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.String(64), index=True)
    sku_id = db.Column(db.String(64), index=True, unique=True)
    discounted_sku_id = db.Column(db.String(64))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self, include_email=False):
        return {
            'id': self.id,
            'transaction_id': self.transaction_id,
            'sku_id': self.sku_id,
            'discounted_sku_id': self.discounted_sku_id,
            'timestamp': self.timestamp
        }

    def from_dict(self, data, new_user=False):
        self.transaction_id = data['transactionId']
        self.discounted_sku_id = data['selectedProduct']
        self.sku_id = data['skuId']
