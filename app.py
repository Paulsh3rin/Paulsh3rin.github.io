from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

app = Flask(__name__)

#Configure the SQLAlchemy part of the app instance
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Select*From@localhost/BANKING'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create the SQLAlchemy db instance
db = SQLAlchemy(app)

# Define the model
class Transaction(db.Model):
    __tablename__ = 'CheqMay23_June24'
    Date = db.Column(db.Date, primary_key=True)
    vendors = db.Column(db.String(255))
    Debit = db.Column(db.Float)
    Credit = db.Column(db.Float)
    account = db.Column(db.String(255))


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/data', methods=['GET'])
def get_data():
    from_date = request.args.get('fromDate')
    to_date = request.args.get('toDate')

    query = Transaction.query
    if from_date:
        query = query.filter(Transaction.date >= from_date)
    if to_date:
        query = query.filter(Transaction.date <= to_date)

    transactions = query.all()

    income = query.with_entities(func.sum(Transaction.Credit)).scalar() or 0
    expense = query.with_entities(func.sum(Transaction.Debit)).scalar() or 0

    data = {
        'income': income,
        'expense': expense,
        'transactions': [{
            'date': t.Date.strftime('%Y-%m-%d'),
            'debit': t.Debit,
            'credit': t.Credit,
            'account': t.account
        } for t in transactions]
    }
    return jsonify(data)

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    app.run(debug=True)
