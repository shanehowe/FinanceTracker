# FinanceTracker

FinanceTracker is a web based application built with Flask that allows users to track their monthly expenses. 

Users can create an account and log in. Users will be redirected to the main page where they will be able to add an expense and pick a cetegory for that expense. Once the expense has been created it will be rendered on a table containing the amount, the category and the date the expense was added. Above the table users can see their remaining balance along with a summary of the all categories with the total amount spent for each category.

Users can then navigate to the dashboard page will allows users to update their balance through the completion of a form. Users can also remove an expense from the table if needs be. A chart is rendered on the dashboard page to give users a visualisation of their expenses in each category.

All animations that happen in the web app are made using Animation.ss library.

# Images

### Welcome

<img height="400" width="1000" alt="login_page" src="/readme_imgs/main.png">

<img width="1000" alt="login_page" src="/readme_imgs/main_responsive.png">

### Log In

<img width="1440" alt="login_page" src="/readme_imgs/login_page.png">

<img width="1440" alt="login page mobile" src="/readme_imgs/login_page_responsive.png">

### Register 

<img width="1440" alt="login_page" src="/readme_imgs/register.png">

<img width="1440" alt="login_page" src="/readme_imgs/register_responsive.png">

### Home 

<img width="1440" alt="login_page" src="/readme_imgs/home.png">

<img width="1440" alt="login_page" src="/readme_imgs/home-responsive.png">

### Dashboard 

<img width="1440" alt="login_page" src="/readme_imgs/dashboard.png">


## Forms

* All forms are created by utilizing flask_wtf & wtforms.

* Example:
    ``` python 
    class RegistrationForm(FlaskForm):
        email = StringField("Email", validators=[DataRequired(), Email()])
        password = PasswordField("Password", validators=[DataRequired()])
        password1 = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
        submit = SubmitField("Register")
    ```

## Models

* I decided to use SQLAlchemy to create the models for the database. 

* Example: 
    ``` python 
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
    ```

## Languages used 

* Python
* JavaScript
* HTML 
* CSS

## Libraries/Frameworks used

* Flask
* Animate.css
* Chart.js