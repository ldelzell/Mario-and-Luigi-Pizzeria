from flask import Flask, render_template, redirect, flash
from flask import request, redirect
from flask import Flask, url_for, request
import os
from flask import send_from_directory
from flask import Flask
from flask_login import LoginManager, current_user
from models import User
from flask_login import login_required
import random

app = Flask(__name__, template_folder= 'templates')


@app.route('/')
def home():
    return render_template("homepage/home.html")

@app.route('/menu')
def menu():
    return render_template("homepage/menu.html")

@app.route('/aboutus')
def about():
    return render_template("homepage/about.html")

@app.route('/admin')
@login_required
def admin():
    if current_user.isAdmin:
        return render_template("authentication/admin.html")
    else:
        flash
        return redirect(url_for("auth.login"))

@app.route('/admin_orders')
def admin_orders():
    return render_template("admin/admin_order.html", current_orders=current_orders)

@app.route('/admin_done')
def admin_done():
    return render_template("admin/admin_done.html")

current_orders = []


data = [] 
@app.route("/oven_data", methods=['GET', 'POST']) 
def receive_data():
    global data
    if request.method == 'POST':
        receivedData = request.get_json()
        Newdata = (receivedData['time'], receivedData['temperature'], receivedData['timer'], receivedData['ovenID'])
    
        data.append(Newdata)
        if len(data) > 1:
            data.pop(0)
        return 'OK', 200
    else:
        return render_template("smartoven.html", oven_data = data)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

app.config['SECRET_KEY'] = 'a3d45f6dS2'

from auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

from main import main as main_blueprint
app.register_blueprint(main_blueprint)

login_manager = LoginManager()
# login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.get(id=user_id)

@login_manager.unauthorized_handler
def handle_needs_login():
    flash("You have to be logged in to access this page.")
    return redirect(url_for('auth.login', next=request.endpoint))

# gets the pressed item from menu and appends it to the list and display it on the order page
@app.route('/order', methods=['POST'])
@login_required
def add_order():
    global orderList, Total
    orderList.append([request.form.get('pizza'), request.form.get('price')])
    return redirect(url_for('menu'))  

orderList=[]
priceList=[]
Total=0
orderNumber = 1
prev_order =0


def clear_order_list():
    global orderList
    orderList.clear()
    return 

def calculate_total(List):
    total = 0
    for item in List:
        total +=float(item[1])
    return total

@app.route('/order')
@login_required
def order_start():
    Total = calculate_total(orderList)
    return render_template('order.html',orderList=orderList,priceList=priceList, Total=Total)

@app.route('/payment')
def payment():
    return render_template('payment.html')

@app.route('/order_ready', methods = ['POST'])
def order_ready():
    order_num = "#"+request.form['order']
    for i in current_orders:
        if i[0]==order_num:
            current_orders.remove(i)
        else:
            pass
    return redirect('/admin_orders')



@app.route('/finish_order')
def finish_order():
    global orderList, orderNumber, prev_order
    order = []
    order.append("#"+str(orderNumber))
    for i in orderList:
        order.append(i[0])
    current_orders.append(order)
    orderList = []
    prev_order = orderNumber
    orderNumber +=1
    return redirect('/thanks')

@app.route('/remove_last')
def remove_last():
    global orderList
    orderList.pop(-1)
    return redirect('/order')

@app.route('/thanks')
def thank_you():
    #clear_order_list()
    return render_template('thanks.html',orderNumber=prev_order)
@app.route('/progress')
def progress():
    return render_template('progress.html')
@app.route('/smartoven')
def smartoven():
    return render_template('smartoven.html')
