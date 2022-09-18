from ast import Pass
from asyncio.windows_events import NULL
from binascii import Incomplete
from glob import glob
import re
from unicodedata import name
from unittest import removeResult, result
from flask import Flask,render_template,request,Response,json, flash, redirect, url_for,session
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
import uuid
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
def history():
    new_taskk_history = []

        # flash("transaction added successfully")
        #APPLICATION HISTORY
    total_history = list(tasks.find({},{"name":1,"amount":1,"_id":1}))
    for i in total_history:
        new_taskk_history.append(i)       
    return render_template('transaction_history.html',new_task_history = new_taskk_history)

# @app.route("/edit/<id>", methods=["GET","POST"])
# def update(id):
#     if request.method=='GET':
#         history_update=[]
#         history_data=tasks.find({'_id':id})
#         for i in history_data:
#             history_update.append(i)
#             print(history_update)
            
#     if request.method=="POST":
#         N = request.form.get("name")
#         i = request.form.get("employee_id")
#         p = request.form.get("phone")
#         jd = request.form.get("job")
#         d = request.form.get("dateemployed")
#         ad = request.form.get("resaddress")
#         jl = request.form.get("reslocation")


#         tasks.update_one({"Employee_id": i},{"$set":{'Employee_name':N,'Employee_id':i,'Phone_Number':p,'Designation':jd,'Date_of_Joining':d,'Address':ad,'Location':jl}})
#         return redirect(url_for('employeelist'))
#     return render_template ("edit.html",newuser=history_update)

@app.route('/edit')
def edit():
    return render_template('edit.html')

@app.route('/nav')
def nav():
    return render_template('navbar.html')

@app.route('/')
def about():
    return render_template('home.html')
if __name__ == "__main__":
    app.run(debug = True)