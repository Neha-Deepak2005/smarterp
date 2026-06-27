from flask import Blueprint, request, jsonify
from models import db, Ledger, StockItem, SalesVoucher, PurchaseVoucher

voucher_bp = Blueprint('voucher', __name__)

@voucher_bp.route('/sale', methods=['POST'])
def create_sale():
    data = request.get_json()
    customer = Ledger.query.get(data['customer_id'])
    item = StockItem.query.get(data['item_id'])

    if not customer:
        return jsonify({"error": "Customer not found"}), 404
    if not item:
        return jsonify({"error": "Item not found"}), 404
    if item.quantity < data['quantity']:
        return jsonify({"error": "Not enough stock!"}), 400

    total = item.selling_price * data['quantity']
    item.quantity -= data['quantity']
    customer.balance += total

    sale = SalesVoucher(
        customer_id=data['customer_id'],
        item_id=data['item_id'],
        quantity=data['quantity'],
        total_amount=total
    )
    db.session.add(sale)
    db.session.commit()
    return jsonify({"message": "Sale recorded!", "total_amount": total, "remaining_stock": item.quantity, "customer_balance": customer.balance}), 201

@voucher_bp.route('/sales', methods=['GET'])
def get_sales():
    sales = SalesVoucher.query.all()
    result = [{"id": s.id, "customer_id": s.customer_id, "item_id": s.item_id, "quantity": s.quantity, "total_amount": s.total_amount} for s in sales]
    return jsonify(result)

@voucher_bp.route('/purchase', methods=['POST'])
def create_purchase():
    data = request.get_json()
    supplier = Ledger.query.get(data['supplier_id'])
    item = StockItem.query.get(data['item_id'])

    if not supplier:
        return jsonify({"error": "Supplier not found"}), 404
    if not item:
        return jsonify({"error": "Item not found"}), 404

    total = item.purchase_price * data['quantity']
    item.quantity += data['quantity']
    supplier.balance += total

    purchase = PurchaseVoucher(
        supplier_id=data['supplier_id'],
        item_id=data['item_id'],
        quantity=data['quantity'],
        total_amount=total
    )
    db.session.add(purchase)
    db.session.commit()
    return jsonify({"message": "Purchase recorded!", "total_amount": total, "new_stock": item.quantity, "supplier_balance": supplier.balance}), 201

@voucher_bp.route('/purchases', methods=['GET'])
def get_purchases():
    purchases = PurchaseVoucher.query.all()
    result = [{"id": p.id, "supplier_id": p.supplier_id, "item_id": p.item_id, "quantity": p.quantity, "total_amount": p.total_amount} for p in purchases]
    return jsonify(result)