#! /usr/bin/env python3
# -*- config:utf-8 -*-
import json,os
from flask import Flask,render_template,url_for,redirect,abort

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

def file_data(name):
    path = '/home/shiyanlou/files/' + name +'.json'
    with open(path) as f:
        file_data = json.loads(f.read())
        return file_data
file1 = file_data('helloshiyanlou')
file2 = file_data('helloworld')


@app.route('/')
def index():
    return render_template('index.html',file1=file1,file2=file2)

@app.route('/files/<filename>')
def file(filename):
    if os.path.exists('/home/shiyanlou/files/' + filename + '.json') :
        data = file_data(filename)
        return render_template('file.html',data=data)
    else:
        abort(404)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'),404
