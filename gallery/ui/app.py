from flask import Flask
from flask import render_template
from flask import request

from gallery.tools.db import *

app = Flask(__name__)

@app.route("/")
def  hello_world():
    return "hello world"

@app.route("/admin")
def admin_home():
    connect()
    users = list_users()
    return render_template('admin_home.html', users=users)

@app.route("/admin/modify/<username>")
def modify_user(username):
    connect()
    user = get_user(username)
    if user:
        return render_template('modify_form.html', full_name=user[2], username=username)
    else:
        return username + " does not exist.<br/><a href='/admin'>Return to Menu</a>"

@app.route("/admin/modified", methods = ['POST'])
def modified():
    connect()
    username = request.form['username'] 
    full_name = request.form['full_name'] if request.form['full_name'] else ""
    password = request.form['password'] if request.form['password'] else ""
    edit_user(username,password,full_name)
    return full_name + " has been modified.<br/><a href='/admin'>Return to Menu</a>"

@app.route("/admin/delete/<username>")
def delete(username):
    return render_template('areyousure.html', username=username)

@app.route("/admin/deleted/<username>")
def deleted(username):
    connect()
    delete_user(username)
    return username + " has been deleted.<br/><a href='/admin'>Return to Menu</a>"

@app.route("/admin/addUser")
def new_user_form():
    return render_template('add_form.html')

@app.route("/admin/added", methods = ['POST'])
def added():
    connect()
    username = request.form['username']
    full_name = request.form['full_name'] if request.form['full_name'] else ""
    password = request.form['password'] if request.form['password'] else ""
    if add_user(username,password,full_name):
        return username + " has been created.<br/><a href='/admin'>Return to Menu</a>"
    else:
        return "Could not create " + username + ".<br/><a href='/admin'>Return to Menu</a>"


