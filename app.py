from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import logging
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Configure the SQLAlchemy part of the app instance
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
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
    
    logging.info(f"API called with fromDate={from_date} and toDate={to_date}")

    transactions = Transaction.query.filter(Transaction.Date >= from_date, Transaction.Date <= to_date).all()

    income = sum(transaction.Credit for transaction in transactions)
    expense = sum(transaction.Debit for transaction in transactions)
    transactions_list = [
        {
            'Date': transaction.Date.strftime('%Y-%m-%d'),
            'vendors': transaction.vendors,
            'Debit': transaction.Debit,
            'Credit': transaction.Credit,
            'account': transaction.account
        }
        for transaction in transactions
    ]
    
    return jsonify({
        'income': income,
        'expense': expense,
        'transactions': transactions_list
    })

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app.run(debug=True)
