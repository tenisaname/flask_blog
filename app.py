from flask import Flask, render_template

# Create a Flask Instance
app = Flask(__name__)

# Create a route decorator
@app.route('/')

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


def index():
    first_name = "John"
    stuff = "This is bold text"

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

app.run(debug=True)