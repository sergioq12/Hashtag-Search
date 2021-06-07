from flask import request, render_template, redirect, url_for, session, flash
from initapp import app
from models import *
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash
from forms import LoginForm, RegisterForm, SearchForm
from hashtagSearch import HashtagSearcher

db.init_app(app)

# New things to implement:
# - Implement the search engine, just being able to search the hashtag, and give the results
# - Create a python libray that searches for the hashtag, in order to use from other directories. Ask professor if it is a good idea.
# - Important to discuss with professor the possibility of implementing a database system for the hashtagas
#   This in order to see if it is optimal for the searches. This is what is going to allow us to work with a 
#   machine learning model. 
# - Get the search engine working with our program that we made with selenium (Big step) (probably it would be nice to get the 
#   program running with selenium on the background instead of in the front line. Ask professor also.)


# Database engine object from SQLAlchemy that manages connections to the database.
engine = create_engine("postgres://idddlpqpcgljyx:6281d126fbb94c36fa60991b8f973246e5db0053cff1313d7f207a55c09a7412@ec2-52-206-15-227.compute-1.amazonaws.com:5432/dcbo59m4pm4894")

# Create a 'scoped session' that ensures different users' interactions with the database are kept separate.
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    session.clear()
    return render_template("index.html")

@app.route("/login")
def login():
    form = LoginForm()
    return render_template("login.html", form=form)

@app.route("/loggedin", methods=["GET","POST"])
def loggedin():
    if request.method == "POST":
        # get the form information
        username = request.form.get("username")
        password = request.form.get("password")

        # Verify if the user information is sufficient to log in
        user = User.query.filter(User.username == username).first()

        # Need to see if the user is in the database
        if user is None:
            # return a flash message and tell the person to register
            flash("The username or password is incorrect. Please try again")
            return redirect(url_for('login'))

        # Check if password is correct 
        hashed_password = user.password
        if check_password_hash(hashed_password, password):
            # As the user logged in, then we can save his information in the session
            session["username"] = username
            session["password"] = password
            form = SearchForm()
            return render_template("recomendation.html", form=form)
        else:
            flash("The username or password is incorrect. Please try again")
            return redirect(url_for('login'))
    else:
        return render_template("error.html", message="Not valid method to get the form.")

@app.route("/register")
def register():
    form = RegisterForm()
    return render_template("register.html", form=form)

@app.route("/registered", methods=["GET","POST"])
def registered():
    if request.method == "POST":
        # get info from the form
        username = request.form.get("username")
        password = request.form.get("password")
        re_password = request.form.get("re_password")
        email = request.form.get("email")

        # We need to give a flash message if the person uses a used username
        used_username = User.query.filter(User.username == username).first()
        if used_username is not None:
            flash("The username is already taken. Try another one")
            return redirect(url_for('register'))

        # Also a flash message if the password is not the same as the re-password
        if password != re_password:
            flash("The passwords do not match.")
            return redirect(url_for('register'))
        
        # if the email is invalid, for the future we need to make this more complex
        if "@" not in email:
            flash("That email is not valid")
            return redirect(url_for('register'))

        # Hash the password in order to get it into the database
        hashed_password = generate_password_hash(password)

        # enter the information inside the database
        User.add_user(username=username, password=hashed_password, email=email)
        form = SearchForm()
        # As the user registers, we are going to log him/her in
        session["username"] = username
        session["password"] = password
        return render_template("recomendation.html", form=form)
        # redirect the user as logged in
    else:
        return render_template("error.html", message="Not valid method to get the form.")

# login required should be use here also in the function for the search, I mean, definitely we can do it without it, but still will be nice to learn
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route("/search", methods=["GET","POST"])
def search():
    # get information from form
    hashtag = request.form.get("search")
    hashtagSearchEngine = HashtagSearcher(hashtag)
    recommendedHashtags = hashtagSearchEngine.getRecommendedHashtags()
    # get the program searching for the hashtag and giving the result in a list of 10 items
    # we need to render another webpage which is the actual that is going to show the results
    # We need to pass the list to that html template to insert them in the website.
    return render_template("results.html", recommendedHashtags = recommendedHashtags)




