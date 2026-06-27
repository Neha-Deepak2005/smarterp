from flask import Blueprint, request, jsonify
from models import db, Ledger

ledger_bp = Blueprint('ledger', __name__)

@ledger_bp.route('/ledger', methods=['POST'])
def create_ledger():
    data = request.get_json()
    new_ledger = Ledger(
        name=data['name'],
        ledger_type=data['ledger_type'],
        balance=data.get('balance', 0.0)
    )
    db.session.add(new_ledger)
    db.session.commit()
    return jsonify({"message": "Ledger created!", "id": new_ledger.id}), 201

@ledger_bp.route('/ledgers', methods=['GET'])
def get_ledgers():
    ledgers = Ledger.query.all()
    result = [{"id": l.id, "name": l.name, "type": l.ledger_type, "balance": l.balance} for l in ledgers]
    return jsonify(result)