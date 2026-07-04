from routes.ledger import ledger_bp
from routes.stock import stock_bp
from routes.vouchers import voucher_bp
from models import db, Ledger, StockItem, SalesVoucher, PurchaseVoucher
from flask import Flask, render_template, redirect, url_for, request, jsonify, session

app = Flask(__name__)
app.secret_key = 'smarterp-secret-key-2026'
USERNAME = 'admin'
PASSWORD = 'smarterp123'

@app.before_request
def require_login():
    allowed = ['login', 'static']
    if 'logged_in' not in session and request.endpoint not in allowed:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == USERNAME and request.form['password'] == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('home'))
        return render_template('login.html', error='Invalid username or password!')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/NehaDeepak/smarterp/smarterp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

app.register_blueprint(ledger_bp)
app.register_blueprint(stock_bp)
app.register_blueprint(voucher_bp)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ledgers-page')
def ledgers_page():
    return render_template('ledgers.html')

@app.route('/stocks-page')
def stocks_page():
    return render_template('stocks.html')

@app.route('/sales-page')
def sales_page():
    return render_template('sales.html')

@app.route('/purchases-page')
def purchases_page():
    return render_template('purchases.html')

@app.route('/ledger/delete/<int:id>', methods=['POST'])
def delete_ledger(id):
    ledger = Ledger.query.get_or_404(id)
    db.session.delete(ledger)
    db.session.commit()
    return redirect(url_for('ledgers_page'))

@app.route('/ledger/edit/<int:id>', methods=['POST'])
def edit_ledger(id):
    ledger = Ledger.query.get_or_404(id)
    data = request.get_json()
    ledger.name = data['name']
    ledger.balance = data['balance']
    db.session.commit()
    return jsonify({"message": "Ledger updated!"})

@app.route('/stock/delete/<int:id>', methods=['POST'])
def delete_stock(id):
    item = StockItem.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Stock item deleted!"})

@app.route('/sale/delete/<int:id>', methods=['POST'])
def delete_sale(id):
    sale = SalesVoucher.query.get_or_404(id)
    item = StockItem.query.get(sale.item_id)
    if item:
        item.quantity += sale.quantity
    db.session.delete(sale)
    db.session.commit()
    return jsonify({"message": "Sale deleted!"})

@app.route('/purchase/delete/<int:id>', methods=['POST'])
def delete_purchase(id):
    purchase = PurchaseVoucher.query.get_or_404(id)
    item = StockItem.query.get(purchase.item_id)
    if item:
        item.quantity -= purchase.quantity
    db.session.delete(purchase)
    db.session.commit()
    return jsonify({"message": "Purchase deleted!"})

if __name__ == '__main__':
    app.run(debug=True)

