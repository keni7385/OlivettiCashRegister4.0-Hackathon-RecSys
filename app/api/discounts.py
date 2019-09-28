from flask import jsonify, request, g
from sqlalchemy import func
import requests
from random import randrange

from app import db
from app.api import bp
from app.models import Discount


@bp.route('/transaction', methods=['POST'])
def post_transaction():
    """
    Compute the recommendation and possible discounts with product sku
    {"transactionId" : "12483","transactionList" : [ "01234567891234", "01234567891233", "01234567891238", "01234567891233", "01234567891238", "01234567891233", "01234567891238"]}
    :return:
    """
    data = request.get_json()

    # TODO filter out the discounted product before to fit to the recommender
    # TODO delete used discounts

    return jsonify({'offers': [
        {
            "sku": "12334424643853",
            "discount": "20"
        }, {
            "sku": "36436436",
            "discount": "10"
        }, {
            "sku": "9789529368440",
            "discount": "20"
        }]})


@bp.route('/selection', methods=['POST'])
def post_selection():
    """
    Register the discount chosen by the user and print the new product
    {"transactionId" : "12483","selectedProduct" : "01234567891234"}
    :return:
    """
    data = request.get_json()
    data['skuId'] = "9789529368440"  # TODO generate new sku id smartly

    new_sku = copy_product_discount(data['selectedProduct'], data['discount'] or 0.80)
    data['skuId'] = new_sku

    discount = Discount()
    discount.from_dict(data)
    db.session.add(discount)
    db.session.commit()
    return jsonify({"discountSKU": new_sku})


def copy_product_discount(sku, discount):
    """
    Returns the new sku id of the discounted product
    :param sku: the sku to copy
    :param discount: the discount to apply
    :return: the new sku id
    """
    url = "https://www.selfscanner.net/wsbackend/users/hackathon/skus/%s" % sku
    r = requests.get(url=url)
    data = r.json()["data"]
    del data["productId"]

    # update data
    data["productSku"] = "discount_%s_%s" % (data["productSku"], str(randrange(1000)+1))
    data["productPrice"] = int(data["productPrice"] * discount)
    data["productName"] = "Discounted %s" % data["productName"]

    post_url = "https://www.selfscanner.net/wsbackend/users/hackathon/products"
    r = requests.post(post_url, headers={
        "Content-Type": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyTmFtZSI6ImhhY2thdGhvbiIsInVzZXJUeXBlIjoicmVndWxhciIsImlhdCI6MTU2OTMzNDk0Mn0.wf6JYu6zt0gCxNPMPRWFae9vvlZrj9eaRAgXJIDP3kM"
    }, json={
        "productSku": data["productSku"],
        "productName": data["productName"],
        "productDescription": data["productDescription"],
        "productImageName": data["productImageName"],
        "productPrice": data["productPrice"]
    })

    return data["productSku"]
