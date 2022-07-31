from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField, DecimalField
from wtforms.validators import DataRequired, EqualTo, Email, NumberRange


class RegistrationForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    password1 = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")

class AddExpenseForm(FlaskForm):
    amount = DecimalField("Expense Amount", validators=[DataRequired(), NumberRange(min=0)])
    select = SelectField("Select Category", choices=["Food & Drinks", "Shopping", "Bills & Utilities", "Transport", "Others"])
    submit = SubmitField("Add Expense")

class AddBalanceForm(FlaskForm):
    amount = DecimalField("Amount To Add", validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField("Update Balance")    