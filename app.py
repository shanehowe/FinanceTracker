from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin

app = Flask(__name__)
app.config['SECRET_KEY'] = '8f42a73054b1749f8f58848be5e6502c'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), index=True, unique=True)
    password_hash = db.Column(db.String(150))
    balance = db.Column(db.Float)

    def __repr__(self) -> str:
        return "<User {}>".format(self.email)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Expenses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), index=True, unique=False)
    amount = db.Column(db.Float)
    date = db.Column(db.String(10), index=True, unique=False)
    category_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __repr__(self) -> str:
        return "<Expense {} {} {}>".format(self.category, self.amount, self.date)
    
class CategorySums(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), index=True, unique=False)
    sum = db.Column(db.Float)
    category_sums_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __repr__(self) -> str:
        return "<Sum {} {} {}>".format(self.category, self.sum, self.category_sums_id)
    
import routes