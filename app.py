from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Tweet
from forms import UserForm, TweetForm


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///login_demo'
app.config['SQLALCHEMY_TRACK_NOTIFICATIONS'] = False 
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'bluprint'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False 


connect_db(app)
db.create_all()


toolbar = DebugToolbarExtension(app)


@app.route('/')
def home_page():
    return render_template('index.html')


@app.route('/tweets', methods = ['GET', 'POST'])
def show_tweets():
    if 'user_id' not in session:
        flash('Please login first')
        return redirect('/')
    form = TweetForm()
    all_tweets = Tweet.query.all()
    if form.validate_on_submit():
        text = form.text.data
        new_tweet = Tweet(text = text, user_id = session['user_id'])
        db.session.add(new_tweet)
        db.session.commit()
        flash('Tweet created')
        redirect('/tweets')

    return render_template('tweets.html', form = form, tweets = all_tweets)


@app.route('/register', methods = ['GET', 'POST'])
def register_user():
    form = UserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data 
        new_user = User.register(username, password)
        db.session.add(new_user)
        db.session.commit()
        session['user_id'] = new_user.id
        flash('Welcome New User!')
        redirect('/tweets')
    return render_template('register.html', form = form)

@app.route('/login', methods = ['GET', 'POST'])
def login_user():
    form = UserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        User.authenticate(username, password)
        if user:
            flash('Welcome Back!')
            session['user_id'] = user.id
            return redirect('/tweets')
        else:
            form.username.errors = ['Invalid username/password']

    return render_template('login.html', form = form)

@app.route('/logout')
def logout_user():
    session.pop('user_id')
    flash('Goodbye!')
    return redirect('/)')

@app.route('/users/<username>/tweet/new', methods = ['GET', 'POST'])
def new_tweet(username):
    if 'username' not in session or username != session['username']:
        raise Unauthorized()
    form = TweetForm()
    if form.validate_on_submit():
        title = form.title.data
        text = form.text.data
        feedback = Feedback (
            title = title,
            text = text,
            username = username,
        )
        db.session.add(tweet)
        db.session.commit()
        return redirect(f'/users/{tweet.username}')
    else:
        return render_template('tweet/tweets.html', form = form)

@app.route('/tweets/<int:tweet_id>/update', methods = ['GET','POST'])
def update_tweet(tweet_id):
    tweet = Tweet.query.get(tweet_id)
    if "username" not in session or feedback.username != session['username']:
        raise Unauthorized()

    form = TweetForm(obj = tweet)

    if form.validate_on_submit():
        tweet.title = form.title.data
        tweet.text = form.text.data

        db.session.commit()

        return redirect(f"/users/{tweet.username}")

    return render_template("/tweets/edit.html", form = form, tweet = tweet)

@app.route("/tweet/<int:tweet_id>/delete", methods=["POST"])
def delete_tweet(tweet_id):
    tweet = tweet.query.get(tweet_id)
    if "username" not in session or feedback.username != session['username']:
        raise Unauthorized()

    form = DeleteForm()

    if form.validate_on_submit():
        db.session.delete(tweet)
        db.session.commit()

    return redirect(f"/tweets/{tweet.username}")