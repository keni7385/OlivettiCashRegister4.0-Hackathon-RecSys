from flask import jsonify, request, g
from sqlalchemy import func
from app.api import bp


@bp.route('/transaction', methods=['POST'])
def post_transaction():
    """
    {"transactionId" : "12483","transactionList" : [ "01234567891234", "01234567891233", "01234567891238", "01234567891233", "01234567891238", "01234567891233", "01234567891238"]}
    :return:
    """
    data = request.get_json()
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
    {"transactionId" : "12483","selectedProduct" : "01234567891234"}
    :return:
    """
    data = request.get_json()
    return jsonify({"discountSKU": "9789529368440"})
