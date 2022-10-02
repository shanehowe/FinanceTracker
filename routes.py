from distutils.command.config import config
from flask import redirect, render_template, request, url_for, flash
from flask_login import (
    LoginManager,
    login_required,
    current_user,
    login_user,
    logout_user,
)
from werkzeug.security import check_password_hash
from app import User, Expenses, CategorySums, app, db
from forms import LoginForm, RegistrationForm, AddExpenseForm, AddBalanceForm
from datetime import datetime

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

todays_date = datetime.today().strftime("%Y-%m-%d")


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        try:
            new_user = User(email=form.email.data, balance=0.00)
            new_user.set_password(form.password.data)
            db.session.add(new_user)
            db.session.commit()
        except:
            flash("Email already registered. If you have an account try logging in.")
            return render_template("register.html", form=form)

        return redirect("/login")

    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                return redirect(url_for("index"))
            else:
                flash("Incorrect Password. Please try again.")
                return render_template("login.html", form=form)

    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/home", methods=["GET", "POST"])
@login_required
def index():
    form = AddExpenseForm()

    # variables to render amount spent in specific category
    shopping = CategorySums.query.filter_by(
        category="Shopping", category_sums_id=current_user.id
    ).first()
    food_drinks = CategorySums.query.filter_by(
        category="Food & Drinks", category_sums_id=current_user.id
    ).first()
    bills = CategorySums.query.filter_by(
        category="Bills & Utilities", category_sums_id=current_user.id
    ).first()
    transport = CategorySums.query.filter_by(
        category="Transport", category_sums_id=current_user.id
    ).first()
    others = CategorySums.query.filter_by(
        category="Others", category_sums_id=current_user.id
    ).first()

    # logic to calculate monthly income for mobile view
    user_expenses = CategorySums.query.filter_by(category_sums_id=current_user.id).all()
    total = 0
    if user_expenses:
        for expense in user_expenses:
            total += expense.sum

    if form.validate_on_submit():
        category = form.select.data
        amount = form.amount.data
        date = todays_date
        category_id = current_user.id
        new_expense = Expenses(
            category=category, amount=amount, date=date, category_id=category_id
        )
        current_user.balance -= float(amount)
        db.session.add(new_expense)

        user_sum = CategorySums.query.filter_by(
            category=category, category_sums_id=current_user.id
        ).first()

        # logic to add all expenses for slected category
        if user_sum == None:
            try:
                new_sum = CategorySums(
                    category=category, sum=amount, category_sums_id=current_user.id
                )
                db.session.add(new_sum)
            except:
                return redirect(url_for("index"))
        else:
            user_sum.sum += float(amount)

        db.session.commit()

        return redirect(url_for("index"))

    expenses = (
        Expenses.query.filter_by(category_id=current_user.id)
        .order_by(Expenses.date.desc())
        .all()
    )

    return render_template(
        "index.html",
        form=form,
        expenses=expenses,
        shopping=shopping,
        food_drinks=food_drinks,
        bills=bills,
        transport=transport,
        others=others,
        total=total,
    )


@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def account():
    add_form = AddBalanceForm()
    expenses = (
        Expenses.query.filter_by(category_id=current_user.id)
        .order_by(Expenses.date.desc())
        .all()
    )

    # variables for graph data
    shopping = CategorySums.query.filter_by(
        category="Shopping", category_sums_id=current_user.id
    ).first()
    food_drinks = CategorySums.query.filter_by(
        category="Food & Drinks", category_sums_id=current_user.id
    ).first()
    bills = CategorySums.query.filter_by(
        category="Bills & Utilities", category_sums_id=current_user.id
    ).first()
    transport = CategorySums.query.filter_by(
        category="Transport", category_sums_id=current_user.id
    ).first()
    others = CategorySums.query.filter_by(
        category="Others", category_sums_id=current_user.id
    ).first()

    if request.method == "POST":
        try:
            form_value = request.form.get("expenses")
            expense = Expenses.query.filter_by(id=form_value).first()
            current_user.balance += float(expense.amount)
            category_sum = CategorySums.query.filter_by(
                category=expense.category, category_sums_id=current_user.id
            ).first()
            category_sum.sum -= float(expense.amount)
            Expenses.query.filter_by(id=form_value).delete()
            db.session.commit()
            return redirect(url_for("account"))
        except:
            db.session.rollback()

        if add_form.validate_on_submit():
            new_balance = add_form.amount.data
            current_user.balance += float(new_balance)
            db.session.commit()
            return redirect(url_for("account"))

    return render_template(
        "account.html",
        add_form=add_form,
        expenses=expenses,
        shopping=shopping,
        food_drinks=food_drinks,
        bills=bills,
        transport=transport,
        others=others,
    )
