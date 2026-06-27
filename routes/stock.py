from flask import Blueprint, request, jsonify
from models import db, StockItem

stock_bp = Blueprint('stock', __name__)

@stock_bp.route('/stock', methods=['POST'])
def create_stock():
    data = request.get_json()
    new_item = StockItem(
        name=data['name'],
        sku=data.get('sku', ''),
        purchase_price=data.get('purchase_price', 0.0),
        selling_price=data.get('selling_price', 0.0),
        quantity=data.get('quantity', 0)
    )
    db.session.add(new_item)
    db.session.commit()
    return jsonify({"message": "Stock item created!", "id": new_item.id}), 201

@stock_bp.route('/stocks', methods=['GET'])
def get_stocks():
    items = StockItem.query.all()
    result = [{"id": i.id, "name": i.name, "sku": i.sku, "purchase_price": i.purchase_price, "selling_price": i.selling_price, "quantity": i.quantity} for i in items]
    return jsonify(result)