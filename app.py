# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
import requests
import logging.config
from caesarcipher import CaesarCipher
import os
import re

from flask import g, session, jsonify, Markup
from requests_oauthlib import OAuth2Session

from flask import Flask, current_app, render_template_string
from caesarcipher import CaesarCipher

# Flask constructor takes the name of
# current module (__name__) as argument.


from flask import render_template, request, url_for, redirect, flash

import ebooklib
from pymongo import MongoClient
from mongoengine import *
import json
import praw
import requests
import os
import random
from flask_wtf import Form
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from wtforms import StringField
from rake_nltk import Rake
from wtforms.validators import DataRequired
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

from flask_login import LoginManager
from flask_login import current_user, login_user
from werkzeug.urls import url_parse
from psycopg2 import errors
import praw

# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.

app = Flask(__name__)

login = LoginManager(app)
login.login_view = 'login'
app.config['SQLALCHEMY_DATABASE_URI']="postgresql://doadmin:yvga5z7c6g2py29n@copypub-co-do-user-1350609-0.db.ondigitalocean.com:25060/defaultdb?sslmode=require"
app.config['STATIC_FOLDER']='static/'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
OAUTH2_CLIENT_ID = "619043497470590997"
OAUTH2_CLIENT_SECRET = "Secret"
OAUTH2_REDIRECT_URI = 'http://oaflopean.pythonanywhere.com/callback'

API_BASE_URL = os.environ.get('API_BASE_URL', 'https://discordapp.com/api')
AUTHORIZATION_BASE_URL = API_BASE_URL + '/oauth2/authorize'
TOKEN_URL = API_BASE_URL + '/oauth2/token'
app.config['SECRET_KEY'] = OAUTH2_CLIENT_SECRET
from forms import SearchSub, LoginForm, RegistrationAppForm, PostForm, Titles, Chapters
from models import User, Post, Bots, Result, Books,  RedditPost, Subreddits


#@app.route('/<method>/<key>')
def hello_world(method, key):
    urls=[]
    for url_list in app.url_map.iter_rules():
        urls.append(url_list.rule)
        for abc in range(26):
            cipher = CaesarCipher(method,offset= abc).encoded
            print(cipher + url_list.rule)
            if cipher== url_list.rule.strip("/"):
                print("yes")
                method= cipher
                key = CaesarCipher(key, offset=abc).encoded
                print(key)
                print(method)
                return pod(method,key= key)
            else:
                continue
    return str([a for a in urls])



@app.route('/?key=<key>?titles=<yes>', methods=['GET', 'POST']) #allow both GET and POST requests
@app.route('/?key=<key>', methods=['GET', 'POST']) #allow both GET and POST requests
@app.route('/', methods=['GET', 'POST'])
def push():
    texts=[]
    if request.method == 'POST':
        reply=""
        if request.args.get("key"):
            key=request.args.get("key")

            count=Books.query.filter_by(uri=key).count()
            if count>0:
                content=Books.query.filter_by(uri=key).first()
                reply= content.description
                return reply
            else:
                reddit = praw.Reddit(client_id='FCBZa-yDqRLNag', client_secret="secret", password='secret', user_agent='Copypasta', username="caesarnaples2")
                for submission in reddit.subreddit(key).new():

                    if request.args.get("yes"):
                        reply=reply+" " + submission.title+" "
                    else:
                        reply=reply+" " + submission.selftext+" "
                return reply
    else:
        form2 = Titles()
        if form2.validate_on_submit():
            book = Books()
            book.title = form2.title.data
            book.author = form2.author.data
            book.description = form2.description.data
            try:
                book.username = "caesarnaples2"
            except AttributeError:
                book.username = "caesarnaples2"
            s = "abcdefghijklmnopqrstuvwxyz"
            passlen = 12
            book.uri = "".join(random.sample(s, passlen))

            kw = book.description
            title = book.title
            author = book.author
            this_bot = Bots.query.filter_by(username="caesarnaples2").first()
            try:
                client_id = this_bot.client_id
            except AttributeError:
                return redirect("register/app")
            secret = this_bot.secret
            password = this_bot.password
            username = this_bot.username
            reddit = praw.Reddit(client_id=client_id,
                                 client_secret=secret, password=password,
                                 user_agent='Copypasta', username="caesarnaples2")

            try:
                reddit_url = reddit.subreddit('publishcopypasta').name

                post = RedditPost(uri=book.uri, reddit_url=reddit_url, title=book.title, body=book.description,
                                  username=book.username)
                book.reddit_url = reddit_url
                db.session.add(post)
                db.session.commit()
                db.session.add(book)
                db.session.commit()
            except KeyError:
                print("error on db commit")
            return redirect(url_for(pod()))
        if request.args.get("key"):
            key=request.args.get("key")
            count=Books.query.filter_by(uri=key).count()
            if count>0:
                content=Books.query.filter_by(uri=key).first()
                return render_template_string(str(content.description))
            else:
                url = 'https://www.reddit.com/r/' + key + '/new/.json?limit=500'

                data = requests.get(url, headers={'user-agent': 'scraper by /u/ciwi'}).json()

                for link in data['data']['children']:
                    body = link['data']['selftext']
                    texts.append(body.replace("\\","").replace("}","").replace("{",""))
                newt="<br><br>".join(texts)
                return render_template_string(Markup(newt))
        else:
            content = Books.query.filter_by(username="caesarnaples2").all()
            string_response =  "<html>{%include 'header.html'%}<body>{%include 'books.html'%}"
            for box in content:
                string_response = string_response +"<h3>name: " + box.title + "</h3>"
                string_response = string_response +"<br><big>keyname: <a href='/?key="+ box.uri+"'>"+box.uri+ "</big></a><br>url:"
                string_response = string_response + box.description.replace('\n', "<br>").replace("{","").replace("}","")
            return render_template_string(string_response+"</html></body>", form2=form2)

@app.route("/pod", methods=['GET', 'POST'])
def pod():
    form2 = Titles()

    title = "Submit " + str(app)
    username = "caesarnaples2"

    if form2.validate_on_submit():
        book = Books()
        book.title = form2.title.data
        book.author = form2.author.data
        book.description = form2.description.data
        try:
            book.username = username
        except AttributeError:
            book.username = "caesarnaples2"
        s = "abcdefghijklmnopqrstuvwxyz"
        passlen = 6
        book.uri = "".join(random.sample(s, passlen))
        this_bot = Bots.query.filter_by(username="caesarnaples2").first()
        try:
            client_id = this_bot.client_id
        except AttributeError:
            return redirect("/")
        secret = this_bot.secret
        password = this_bot.password
        username = this_bot.username
        reddit = praw.Reddit(client_id=client_id,
                             client_secret=secret, password=password,
                             user_agent='Copypasta', username="caesarnaples2")

        try:
            reddit_url = reddit.subreddit('publishcopypasta').name
        except praw.exceptions.APIException:
            reddit_url = "No url"
        post = RedditPost(uri=book.uri, reddit_url=reddit_url, title=book.title, body=book.description,
                          username=book.username)
        book.reddit_url = reddit_url
        db.session.add(post)
        db.session.commit()
        db.session.add(book)
        db.session.commit()
        return redirect("/")

if 'http://' in OAUTH2_REDIRECT_URI:
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = 'true'


def token_updater(token):
    session['oauth2_token'] = token


def make_session(token=None, state=None, scope=None):
    return OAuth2Session(
        client_id=OAUTH2_CLIENT_ID,
        token=token,
        state=state,
        scope=scope,
        redirect_uri=OAUTH2_REDIRECT_URI,
        auto_refresh_kwargs={
            'client_id': OAUTH2_CLIENT_ID,
            'client_secret': OAUTH2_CLIENT_SECRET,
        },
        auto_refresh_url=TOKEN_URL,
        token_updater=token_updater)


@app.route('/bot')
def index():
    scope = request.args.get(
        'scope',
        'identify email connections guilds guilds.join')
    discord = make_session(scope=scope.split(' '))
    authorization_url, state = discord.authorization_url(AUTHORIZATION_BASE_URL)
    session['oauth2_state'] = state
    return redirect(authorization_url)


@app.route('/callback')
def callback():
    if request.values.get('error'):
        return request.values['error']
    discord = make_session(state=session.get('oauth2_state'))
    token = discord.fetch_token(
        TOKEN_URL,
        client_secret=OAUTH2_CLIENT_SECRET,
        authorization_response=request.url)
    session['oauth2_token'] = token
    return redirect(url_for('.me'))


@app.route('/me')
def me():
    discord = make_session(token=session.get('oauth2_token'))
    user = discord.get(API_BASE_URL + '/users/@me').json()
    guilds = discord.get(API_BASE_URL + '/users/@me/guilds').json()
    connections = discord.get(API_BASE_URL + '/users/@me/connections').json()
    return jsonify(user=user, guilds=guilds, connections=connections)


if __name__ == '__main__':
    # run() method of Flask class runs the application
    # on the local development server.
    app.run()
