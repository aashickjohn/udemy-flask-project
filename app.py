from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os


project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(
    os.path.join(project_dir, "mydatabase.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)


# ORM method
class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(50), nullable=False)
    expansename = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(50), nullable=False)

@app.route('/')
def add():
    return render_template('add.html')

# Method to add expenses to database
@app.route('/addexpense', methods=["POST"])
def add_expense():
    date = request.form["date"]
    expansename = request.form["expensename"]
    amount = request.form["amount"]
    category = request.form["category"]
    expense = Expense(date=date, expansename=expansename,
                      amount=amount, category=category)
    db.session.add(expense)
    db.session.commit()
    return redirect('/expenses')

# Method to delete expenses in database
@app.route('/delete_expense/<int:id>')
def delete_expense(id):
    expense = Expense.query.filter_by(id=id).first()
    db.session.delete(expense)
    db.session.commit()
    return redirect('/expenses')

# Method to render update expense page
@app.route('/update_expense/<int:id>')
def update_expense(id):
    expense = Expense.query.filter_by(id=id).first()
    return render_template("update_expense.html", expense=expense)

# Method to edited expenses into database
@app.route('/edit', methods=["POST"])
def edit():
    id = request.form["id"]
    date = request.form["date"]
    expansename = request.form["expensename"]
    amount = request.form["amount"]
    category = request.form["category"]
    
    expense = Expense.query.filter_by(id=id).first()
    expense.date = date
    expense.expansename = expansename
    expense.amount = amount
    expense.category = category

    db.session.commit()
    return redirect('/expenses')

# Method to query all expenses from database
@app.route('/expenses')
def expenses():
    expenses = Expense.query.all()
    return render_template("expenses.html", expenses=expenses)


if __name__ == '__main__':
    print("App : ", app)
    db.create_all()
    app.run(debug=True)
