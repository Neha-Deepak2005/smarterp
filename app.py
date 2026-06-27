from flask import Flask, render_template
from models import db
from routes.ledger import ledger_bp
from routes.stock import stock_bp
from routes.vouchers import voucher_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:SqlPonnu%40240@localhost/smarterp'
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

if __name__ == '__main__':
    app.run(debug=True)