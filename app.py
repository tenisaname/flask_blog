from flask import Flask, render_template, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField
from wtforms.validators import DataRequired

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime

# Create a Flask Instance
app = Flask(__name__)
# Add Database

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# Secret Key!
app.config['SECRET_KEY'] = 'my secret key'
# Initialize The Database
db = SQLAlchemy(app)
Migrate = Migrate(app, db)

# Create Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    favorite_color = db.Column(db.String(120))
    data_added = db.Column(db.DateTime, default=datetime.now)

    # Create a String 
    def __repr__(self):
        return '<Name %r>' % self.name

@app.route('/delete/<int:id>')
def delete(id):
    user_to_delete = User.query.get_or_404(id)
    name = None
    form = UserForm()
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash('User Deleted Successfully!')

        our_users = User.query.order_by(User.data_added)   
        return render_template("add_user.html", 
                            form = form,
                            name=name,
                            our_users = our_users)
    except:
        flash("Whoops! There was a problem")
        return render_template("add_user.html", form = form, name=name, our_users = our_users)
    
# Create a Form Class
class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired()])
    favorite_color = StringField("Favorite Color")
    submit = SubmitField("Submit")

# Create a Form Class
class NameForm(FlaskForm):
    name = StringField("What's your name?", validators=[DataRequired()])
    submit = SubmitField("Submit")



# def index():
#     return "<h1>Hello World</h1>"

# FILTERS!!!
#safe
#capitalize
#lower
#upper
#title
#trim
#striptags

#Update Database Record
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    form = UserForm()
    name_to_update = User.query.get_or_404(id)
    if request.method == 'POST':
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.favorite_color = request.form['favorite_color']
        our_users = User.query.order_by(User.data_added)   
        try:
            db.session.commit()
            flash('User Updated Successfully!')
            return render_template("update.html",
                                   form = form,
                                   name_to_update = name_to_update,
                                   our_users = our_users)
        except Exception as e:
            flash(f'Error! Look like there was a problem {e}')
            return render_template("update.html",
                                   form = form,
                                   name_to_update = name_to_update)
    else:
        return render_template("update.html",
                                form = form,
                                name_to_update = name_to_update,
                                id = id)

@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            user = User(name = form.name.data, email = form.email.data, favorite_color = form.favorite_color.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        form.favorite_color.data = ''

        flash("User Added Successfully!")
    our_users = User.query.order_by(User.data_added)   
    return render_template("add_user.html", 
                           form = form,
                           name=name,
                           our_users = our_users)

# Create a route decorator
@app.route('/')
                  
def index():
    first_name = "John"
    stuff = "This is bold text"
    flash("Welcome To Our Website")
    favorite_pizza = ["Pepperoni","Cheese","Mushrooms", 41]
    return render_template("index.html", 
                           first_name = first_name,
                           stuff=stuff,
                           favorite_pizza = favorite_pizza
                           )

# localhost:5000/user/John
@app.route('/user/<name>')

def user(name):
    return render_template("user.html", user_name=name)

# Create Custom Error Pages

# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"),404

# Internal Server Error
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"),500

# Create a Name Page
@app.route('/name', methods=['GET', 'POST'])
def name():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ""
        flash(f"Form Submitted Successfully")

    return render_template("name.html",
                    name = name,
                    form = form)



