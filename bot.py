#!/usr/bin/env python3
# These are the dependecies. The bot depends on these to function, hence the name. Please do not change these unless your adding to them, because they can break the bot.
from boto3 import *
import asyncio
import requests
from discord.ext.commands import Bot
import markovify
from app import db
from forms import SearchSub, LoginForm, RegistrationAppForm, PostForm, Titles, Chapters
from models import User, Post, Bots, Result, Books, RedditPost, Subreddits
import json
from sqlalchemy import func, or_
import random
# Here you can modify the bot's prefix and description and wether it sends help in direct messages or not.
client = Bot(description="Babelli bot", command_prefix=".", pm_help = False)



# This is what happens everytime the bot launches. In this case, it prints information like server count, user count the bot is connected to, and the bot id in the console.
# Do not mess with it because the bot can break, if you wish to do so, please consult me or someone trusted.
#@client.event
#async def on_ready():
#    print("Yep")
# This is a basic example of a call and response command. You tell it do "this" and it does it.
@client.command()
async def ping(*args):

    await client.say(":ping_pong: Pong!")
    await asyncio.sleep(3)

@client.command()
async def test(ctx, arg):
    await ctx.send(arg)

@client.command()
async def babelli(ctx,arg, arg2):
        msg=""
        key=arg
        url="https://oaflopean.pythonanywhere.com/?key="+key
        data=requests.post(url, auth=('oaflopean', 'babellibot'))
        text_model = markovify.Text(data.content.decode("utf-8"))
        for i in range(int(arg2)):
            try:
                msg = msg + " " + text_model.make_sentence() + " "
            except TypeError:
                continue
        print(data)
        if len(msg)==0:
            await ctx.send("Sorry! Try more options.")
        else:
            chunks, chunk_size = len(msg), len(msg) / (len(msg)/1995)
            list=[msg[i:i + int(chunk_size)] for i in range(0, chunks, int(chunk_size))]
            for msg_pt in list:
                await ctx.send(msg_pt)
            book = Books()
            book.title = arg+" "+str(arg2)
            book.author = ctx.message.author.name
            book.description = msg
            s = "abcdefghijklmnopqrstuvwxyz"
            passlen = 12
            book.uri = "".join(random.sample(s, passlen))
            book.reddit_url = "http://oaflopean.pythonanywhere.com/?key="+book.uri
            post = RedditPost(uri=book.uri, reddit_url=book.reddit_url, title=book.title, body=book.description,
                              username=book.username)
            db.session.add(post)
            db.session.commit()
            db.session.add(book)
            db.session.commit()

            await ctx.send(book.reddit_url)

@client.command()
async def database(ctx, arg):
    search=Books.query.filter(or_(func.lower(Books.title).contains(arg),(func.lower(Books.author).contains(arg)))).all()
    if search:
        for books in search[:25]:
            await ctx.send(books.title+" by "+books.author+" https://oaflopean.pythonanywhere.com/?key="+books.uri)


    else:
        await ctx.send("No results")


#@client.command()
async def library(ctx, arg, arg2):
    if arg == "search":
        try:
            search = Books.query.filter(
                or_(func.lower(Books.title).contains(arg2), (func.lower(Books.author).contains(arg2)))).all()
            for books in search[:25]:
                await ctx.send(
                    books.title + " by " + books.author + " https://oaflopean.pythonanywhere.com/?key=" + books.uri)
        except Exception as e:
            await ctx.send("error: " + e)
    elif arg == "add":

        if arg2 == "all":
            books = Books.query.filter().all()

            a = open("babelli-copypasta.json", mode="r")
            b = a.read()
            c = {}
            json1 = json.loads(b)
            for bookid in json1.keys():
                books = Books.query.filter(Books.uri == str(bookid)).first()
                if books.uri:
                    await ctx.send(
                        books.title + " by " + books.author + " https://oaflopean.pythonanywhere.com/?key=" + books.uri + " already existed")


                else:
                    json2 = json1[str(bookid)]

                    book = Books()
                    book.title = json2.title
                    book.author = json2.author
                    s3 = boto3.client('s3',
                                      aws_access_key_id="python",
                                      aws_secret_access_key="ZPRZ5P6LFLB64B7KE554",
                                      region_name="sfo2"
                                      )
                    one = 0
                    for one in range(100):
                        one += 1

                        obj = s3.Bucket('paginated').Object("page_"+one+".json")
                        dlfile = s3.download_file(objp)
                        n = {}
                        m = json.loads(dlfile.read())
                        s = "adfhklnquvxyz"
                        passlen = 12
                        book.uri = arg2
                        book.reddit_url = "http://oaflopean.pythonanywhere.com/?key=" + book.uri
                        post = RedditPost(uri=book.uri, reddit_url=book.reddit_url, title=book.title,
                                          body=book.description,
                                          username=book.username)
                        db.session.add(post)
                        db.session.commit()
                        db.session.add(book)
                        db.session.commit()

                        await ctx.send(
                            book.title + " by " + book.author + " https://oaflopean.pythonanywhere.com/?key=" + book.uri + "added with uri key " + str(
                                bookid))


client.run('NjE5MDQzNDk3NDcwNTkwOTk3.XXNr1Q.HutZDq1RQ1CWwcydk0JlWH-uT1w')

# Basic Bot was created by Habchy#1665
# Please join this Discord server if you need help: https://discord.gg/FNNNgqb
# Please modify the parts of the code where it asks you to. Example: The Prefix or The Bot Token
# This is by no means a full bot, it's more of a starter to show you what the python language can do in Discord.
# Thank you for using this and don't forget to star my repo on GitHub! [Repo Link: https://github.com/Habchy/BasicBot]

# The help command is currently set to be not be Direct Messaged.
# If you would like to change that, change "pm_help = False" to "pm_help = True" on line 9.
