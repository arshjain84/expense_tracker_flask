from ast import Pass
from asyncio.windows_events import NULL
from binascii import Incomplete
from glob import glob
import re
from unicodedata import name
from unittest import result
from flask import Flask,render_template,request,Response,json, flash, redirect, url_for,session
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['MONGO_URI'] = "mongodb://localhost:27017/expense_tracker_db"
mongo = PyMongo(app)
bcrypt = Bcrypt(app)

db = mongo.db.users
tasks = mongo.db.tasks

app.secret_key = "arsh-239095jdms-dcj1248o"
@app.route("/signup",methods = ["POST", "GET"])
def signup():  
    if request.method == "POST":
        Full_name = request.form['Full_name']
        Email = request.form['Email']
        User_name = request.form['User_name']
        Password = request.form['Password']
        print(Password)
        print(Email)
        hashed_password = bcrypt.generate_password_hash(Password).decode('utf-8')
        if((db.count_documents({'email':Email}))!=0):
            flash(f'Email Id already exists!!!','danger')
            
        else:
            new_user = {
                'name': Full_name,
                'email':Email,
                'User_name':User_name,
                'Password': hashed_password
            }
            db.insert_one(new_user)
            print(new_user)
            flash(f'User{Full_name} is successfully created','success')
            return redirect(url_for('login'))
    return render_template('signup.html')
    
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method=='POST':
        email = request.form['email']
        password = request.form['password']
        userpassword = db.find_one({'email':email},{'_id':0,'password':1})
        print(bcrypt.check_password_hash(userpassword['password'],password))
        if bcrypt.check_password_hash(userpassword['password'],password):
            flash(f'User logged in successfully','success')
            return redirect(url_for('home'))

    return render_template("login.html")
income=0 
expense=0
@app.route('/home',methods=['GET','POST'])
def home():
    task = "a"
    if request.method=='POST':
        transaction_name = request.form['transactions']
        amount = request.form['enter_amount']

        #application history

        global income
        global expense  
        amt=int(amount)
        if(amt>0):
            income=income+amt
        else:
            expense=expense+amt


        total = income + expense

        new_task = {
            'name':transaction_name,
            'amount':amount,
            'income':income,
            'expense':expense,
            'total':total
            }
        transaction_history = {
            'name': transaction_name,
            'amount': amount
        }
        print(new_task)

        # inc = tasks.aggregate([{$match:{}}, {$group:{_id:0,income:{$sum:"$income"}}}])
        
    return render_template('index.html',history = transaction_history, total = new_task['total'], inc = new_task['income'], exp = new_task['expense'])

if __name__ == "__main__":
    app.run(debug = True)
