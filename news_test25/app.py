#! /usr/bin/env python3
# -*- config:utf-8 -*-

from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from pymongo import MongoClient

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/shiyanlou'
app.config['TEMPLATES_AUTO_RELOAD'] = True
db = SQLAlchemy(app)

#初始化Mongo
client = MongoClient('127.0.0.1',27017)
mongo_db = client.shiyanlou

class File(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(80),unique=True)
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

    def add_tag(self,tag_name):
        tag = {'title':self.title,'tag':tag_name}
        mongo_db.user.insert_one(tag)

    def remove_tag(self,tag_name):
        tag = {'title':self.title,'tag':tag_name}
        mongo_db.user.delete_one(tag)

    @property
    def tags(self):
        tag_list = []
        for i in mongo_db.user.find({'title':self.title}):
            tag_list.append(i['tag'])
        return tag_list

class Category(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80),unique=True)

    def __init__(self,name):
        self.name = name

    def __repr__(self):
        return '<Category %r>' % self.name


@app.route('/')
def index():
    File_All = File.query.all()
    return render_template('index.html',File_All=File_All) 

@app.route('/files/<file_id>')
def file(file_id):
    file_content = File.query.filter_by(id=file_id).first()
    if file_content is None:
        abort(404)
    else:
        return render_template('file.html',file_content=file_content)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html')

