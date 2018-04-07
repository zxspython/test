#! /usr/bin/env python3
# -*- config:utf-8 -*-

from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/shiyanlou'
app.config['TEMPLATES_AUTO_RELOAD'] = True
db = SQLAlchemy(app)

class File(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(80))
    created_time = db.Column(db.DateTime)
    content = db.Column(db.Text)

    category_id = db.Column(db.Integer,db.ForeignKey('category.id'))
    category = db.relationship('Category',backref=db.backref('file',lazy='dynamic'))

    def __init__(self,title,content,category,created_time=None):
        self.title = title
        self.content = content
        if created_time is None:
            created_time = datetime.utcnow()
        self.created_time = created_time
        self.category = category

    def __repr__(self):
        return '<File %r)>' % self.title


class Category(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80))

    def __init__(self,name):
        self.name = name

    def __repr__(self):
        return '<Category %r>' % self.name

@app.route('/')
def index():
    title = File.query.all()
    return render_template('index.html',title=title) 

