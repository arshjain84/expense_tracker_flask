from ast import Pass
from asyncio.windows_events import NULL
from binascii import Incomplete
from glob import glob
import imp
import re
from unicodedata import name
from unittest import removeResult, result
from flask import Flask,render_template,request,Response,json, flash, redirect, url_for,session
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from bson.objectid import ObjectId
import uuid
app = Flask(__name__)
app.secret_key = "arsh-239095jdms-dcj1248o"
# login_manager = LoginManager(app)
# login_manager.login_view = 'auth.login'
# login_manager.init_app(app) 
app.config['MONGO_URI'] = "mongodb://localhost:27017/expense_tracker_db"
mongo = PyMongo(app)
bcrypt = Bcrypt(app)

db = mongo.db.users
tasks = mongo.db.tasks

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
        name = request.form['User_name']
        email = request.form['email']
        password = request.form['Password']
        userpassword = db.find_one({'email':email},{'name':1,'_id':0})
        print(bcrypt.check_password_hash(userpassword['password'],password))
        if bcrypt.check_password_hash(userpassword['password'],password):
            flash(f'User logged in successfully','success')
            return redirect(url_for('home'))
    return render_template('login.html')
income=0 
expense=0
@app.route('/budget',methods=['GET','POST'])
def home():
    # return render_template('index.html')
    new_taskk_inc = []
    new_taskk_exp = []
    new_taskk_bal = []
    new_taskk_history = []
    if request.method=='POST':
        transaction_name = request.form['transactions']
        amount = request.form['enter_amount']

        global income
        global expense  
        amt=int(amount)
        if(amt>0):
            income=income+amt
        else:
            expense=expense+amt


        total = income + expense

        new_task = tasks.insert_one({
            # '_id': uuid.uuid4(),
            'name':transaction_name,
            'amount':amount,
            'income':income,
            'expense':expense,
            'total':total
        })
        income = int(income)
        expense = int(expense)
        total = int(total)
        inc_data=list(tasks.find({},{"income":1,"_id":0}))
        for i in inc_data:
            new_taskk_inc.append(i)
        
        # print(new_taskk_inc)
        exp_data = list(tasks.find({},{"expense":1,"_id":0}))
        for i in exp_data:
            new_taskk_exp.append(i)
        
        # print(new_taskk_exp)

        #calculating balance
        total_bal = list(tasks.find({},{"total":1,"_id":0}))
        for i in total_bal:
            new_taskk_bal.append(i)

        # flash("transaction added successfully")

        #APPLICATION HISTORY
        total_history = list(tasks.find({},{"name":1,"amount":1,"_id":0}))
        for i in total_history:
            new_taskk_history.append(i)  
    return render_template('index.html',new_task_inc = new_taskk_inc, new_task_exp = new_taskk_exp, new_task_bal = new_taskk_bal)


@app.route('/email')
def email():
    return render_template('email.html')

@app.route('/history',methods = ['GET','POST'])
def history1():
    new_taskk_history = []

        # flash("transaction added successfully")
        #APPLICATION HISTORY
    total_history = list(tasks.find({},{"name":1,"amount":1,"_id":1}))
    for i in total_history:
        new_taskk_history.append(i)       
    return render_template('transaction_history.html',new_task_history = new_taskk_history)

# @app.route("/delete/<id>", methods=["GET"])
# def delete(id):
#     db.tasks.delete_one({"_id":id})
#     tasks.delete_one({"_id":id})
#     return redirect(url_for("/"))

@app.route("/history_edit/<id>", methods=["GET","POST"])
def history_edit(id):
    # print('arsh')
    # print(id)
    if request.method=="POST":
        N = request.form['edit_name']
        A = request.form['edit_amount']
        print(N)
        print(A)
        print("hello")

        tasks.update_one({"_id": ObjectId(id)},{"$set":{'name':N,'amount':A}})
        return redirect(url_for('history'))
    if request.method=='GET':
        history_update=[]
        history_data=tasks.find({'_id':ObjectId(id)},{"name":1,"amount":1})
        # print(history_data)
        for i in history_data:
            history_update.append(i)
            print(history_update)

    return render_template ("transaction_history.html",new_task_history=history_update)

@app.route('/edit')
def edit():
    return render_template('edit.html')

@app.route('/nav')
def nav():
    return render_template('navbar.html')

@app.route('/')
def about():
    return render_template('home.html')

# @app.route('/logout')
# def logout():
#     logout_user()
#     return redirect('/')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.run(debug = True)