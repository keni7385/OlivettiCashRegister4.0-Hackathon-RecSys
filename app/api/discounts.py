from flask import jsonify, request, g
from sqlalchemy import func
import requests
from random import randrange

from app import db, recommender
from app.api import bp
from app.models import Discount
from app.recommenders.sku_item_mapper import sku_item_mapper, item_sku_mapper


@bp.route('/transaction', methods=['POST'])
def post_transaction():
    """
    Compute the recommendation and possible discounts with product sku
    {"transactionId" : "12483","transactionList" : [ "01234567891234", "01234567891233", "01234567891238", "01234567891233", "01234567891238", "01234567891233", "01234567891238"]}
    :return:
    """
    # TODO filter out the discounted product before to fit to the recommender
    data = request.get_json()
    transactions = [p for p in data["transactionList"] if not p.startswith("discount_")]
    discounts = [p for p in data["transactionList"] if p not in transactions]
    prod_ids = [sku_item_mapper.get(p, 9) for p in transactions]  # Nutella as default TODO: handle errors in frontend

    # delete used discounts from our db
    Discount.query.filter(Discount.sku_id in discounts).delete()
    db.session.commit()
    # Delete used discounts from selfscan.net
    for d in discounts:
        prod = get_product_by_sku(d)
        if prod is not None:
            delete_product_by_id(prod['productId'])

    recommended_product = recommender.recommend_itemCFR(target_receipt=list(set(prod_ids)))
    new_discounts = [prod_sku_to_dict(item_sku_mapper[prod_id]) for prod_id in recommended_product]
    offers = {'offers': new_discounts}

    return jsonify(offers)  # jsonify(default_offers)


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
    data['skuId'] = new_sku if new_sku is not None else "no discount"
    # TODO handle errors front end side

    discount = Discount()
    discount.from_dict(data)
    db.session.add(discount)
    db.session.commit()
    return jsonify({"discountSKU": new_sku})


@bp.route("/discounts", methods=["DELETE"])
def clean_all_discounts():
    all_prods_url = "https://www.selfscanner.net/wsbackend/users/hackathon/products"
    r = requests.get(all_prods_url, headers={
        "Content-Type": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyTmFtZSI6ImhhY2thdGhvbiIsInVzZXJUeXBlIjoicmVndWxhciIsImlhdCI6MTU2OTMzNDk0Mn0.wf6JYu6zt0gCxNPMPRWFae9vvlZrj9eaRAgXJIDP3kM"
    })

    for prod in r.json()["data"]:
        if prod["productSku"].startswith("discount_"):
            delete_product_by_id(prod["productId"])
            print("Deleted sku %s id %d" % (prod['productSku'], prod['productId']))
    return jsonify({})


def copy_product_discount(sku, discount):
    """
    Returns the new sku id of the discounted product
    :param sku: the sku to copy
    :param discount: the discount to apply
    :return: the new sku id
    """
    data = get_product_by_sku(sku)
    if data is None:
        return None

    del data["productId"]

    # update data
    data["productSku"] = "discount_%s_%s" % (data["productSku"], str(randrange(1000)+1))
    data["productPrice"] = int(data["productPrice"] * (discount if discount > 1 or discount < -1 else discount/100))
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


def get_product_by_sku(sku):
    url = "https://www.selfscanner.net/wsbackend/users/hackathon/skus/%s" % sku
    r = requests.get(url=url)
    data = r.json().get("data", None)
    return data


def get_product_by_id(id):
    url = "https://www.selfscanner.net/wsbackend/users/hackathon/products/%s" % id
    r = requests.get(url=url)
    data = r.json().get("data", None)
    return data


def delete_product_by_id(id):
    url = "https://www.selfscanner.net/wsbackend/users/hackathon/products/%s" % id
    r = requests.delete(url=url, data={}, headers={
        "Content-Type": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyTmFtZSI6ImhhY2thdGhvbiIsInVzZXJUeXBlIjoicmVndWxhciIsImlhdCI6MTU2OTMzNDk0Mn0.wf6JYu6zt0gCxNPMPRWFae9vvlZrj9eaRAgXJIDP3kM"
    })


def prod_sku_to_dict(prod_sku):
    prod = get_product_by_sku(prod_sku)
    if prod is None:
        return default_offers["offers"][0]
    return {
        "sku": prod["productSku"],
        "name": prod["productName"],
        "picture_link": prod["productImageUrl"],
        "price": prod["finalPrices"]["priceAfterTax"],
        "discount": [5, 10, 20][len(prod_sku) % 3]
    }


default_offers = {'offers': [
    {
        "sku": "36436436",
        "name": "Coffee",
        "picture_link": "http://image.spaceify.net/thumbnails/fxS3yvmhArek5klbvBJE8nOr.png",
        "price": 230,
        "discount": 20
    }, {
        "sku": "80177173",
        "name": "Nutella",
        "picture_link": "http://image.spaceify.net/thumbnails/G0-ClMw3wJe662WfTnLUtdwe.jpg",
        "price": 540,
        "discount": 10
    }, {
        "sku": "6430039782525",
        "name": "Protein bar",
        "picture_link": "http://image.spaceify.net/thumbnails/foMkBeUrwK4V9LZIGqDrnRqQ.png",
        "price": 184,
        "discount": 40
    }]}
