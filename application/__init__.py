from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
bootstrap = Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

from application import views
