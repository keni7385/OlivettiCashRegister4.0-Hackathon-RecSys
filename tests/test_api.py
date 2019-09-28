import unittest

from app import create_app, db
from app.models import Discount
from tests.test_config import TestConfig


class ApiCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    ############
    # Discount API
    ############

    def testCreateDiscount(self):
        data = {"transactionId": "12483", "selectedProduct": "01234567891234"}
        d = Discount(id=1, transaction_id="12483", sku_id="9789529368440", discounted_sku_id="01234567891234")
        rv = self.client.post('/api/selection', json=data)

        # will need to be taken from the response and query for the object
        expected_return = {"discountSKU": "9789529368440"}

        self.assertEqual(200, rv.status_code)

        d_inserted = Discount.query.filter_by(sku_id=rv.json["discountSKU"]).first()
        self.assertEqual(d_inserted.transaction_id, d.transaction_id)
        self.assertEqual(d_inserted.id, d.id)
        self.assert_(d_inserted.sku_id.startswith("discount_01234567891234"))
        self.assertEqual(d_inserted.discounted_sku_id, d.discounted_sku_id)
