from flask import Flask, render_template, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Length
from wtforms.widgets import TextArea

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date


# Create a Flask Instance
app = Flask(__name__)
# Add Database

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# Secret Key!
app.config['SECRET_KEY'] = 'my secret key'
# Initialize The Database
db = SQLAlchemy(app)
Migrate = Migrate(app, db)

# Create a Blog Post model
class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    body = db.Column(db.Text)
    author = db.Column(db.String(255))
    date_posted = db.Column(db.DateTime, default = datetime.utcnow)
    slug = db.Column(db.String(255), unique=True)

# Add Psot Page
@app.route('/add_post', methods=['GET', 'POST'])
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Posts(title=form.title.data, body=form.content.data, author=form.author.data, slug=form.slug.data)
        # Clear The Form
        form.title.data = ''
        form.content.data = ''
        form.author.data = ''
        form.slug.data = ''

        # Add post data to database
        db.session.add(post)
        db.session.commit()

        # Return a Message
        flash('Blog Post Submitted Successfully!')
    return render_template('add_post.html', form=form)


# Create a Posts  Form
class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = StringField('Content', validators=[DataRequired()], widget=TextArea())
    author = StringField('Author', validators=[DataRequired()])
    slug = StringField('Slug', validators=[DataRequired()])
    submit= SubmitField('Submit')


# Json Thing
@app.route('/date')
def get_current_date():
    favorite_pizza ={
        "John": "Pepperoni",
        "Mary": "Cheese",
        "Tim": "Mushroom"
    }
    return favorite_pizza


# Create Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    favorite_color = db.Column(db.String(120))
    data_added = db.Column(db.DateTime, default=datetime.now)
    # Do some password stuff!
    password_hash = db.Column(db.String(128))

    @property 
    def password(self):
        raise AttributeError('password is not a readable attribute!')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
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
    password_hash = PasswordField("Password", validators=[DataRequired(), EqualTo('password_hash2', message='Passwords must match')])
    password_hash2 = PasswordField("Confirm Password", validators=[DataRequired()])
    submit = SubmitField("Submit")

# Create a Form Class
class NameForm(FlaskForm):
    name = StringField("What's your name?", validators=[DataRequired()])
    submit = SubmitField("Submit")

# Create a check form
class PasswordForm(FlaskForm):
    email = StringField("What's your email?", validators=[DataRequired()])
    password_hash = PasswordField("What's your password?", validators=[DataRequired()])
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
            # Hash the password
            hashed_pw = generate_password_hash(form.password_hash.data)
            user = User(name = form.name.data, email = form.email.data, favorite_color = form.favorite_color.data, password_hash = hashed_pw )
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
                           name = name,
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

# Create Password Test Page
@app.route('/test_pw', methods=['GET', 'POST'])
def test_pw():
    email = None
    password = None 
    pw_to_check = None
    passed = None 

    form = PasswordForm()
    # validate Form
    if form.validate_on_submit():
        email = form.email.data
        password = form.password_hash.data
        # Clear the form
        form.email.data = ""
        form.password_hash.data = ""

        pw_to_check = User.query.filter_by(email=email).first()

        # Lookup User By Email Address
        passed = check_password_hash(pw_to_check.password_hash, password)

        # flash(f"Form Submitted Successfully")

    return render_template("test_pw.html",
                    email = email,
                    password = password,
                    pw_to_check = pw_to_check,
                    passed = passed,
                    form = form)



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



