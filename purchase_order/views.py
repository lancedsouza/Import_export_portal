from flask import Blueprint,render_template,redirect,url_for,flash,request
from flask import get_flashed_messages
from sqlalchemy import func
# from my_project.purchase_order.forms import InforForm
from sqlalchemy import insert 
from my_project import db
from my_project.models import PurchaseOrder
from my_project.models import Supplier
from my_project.models import Products
from datetime import datetime, timedelta
# from wtforms import StringField,SubmitField,IntegerField,DateField,DateTimeField,FloatField
purchase_order_blueprint = Blueprint('purchase_order',__name__,template_folder='templates/purchase_order')
success_blueprint= Blueprint('success',__name__,template_folder='templates/success')
purchase_order_form_blueprint =Blueprint('purchase_order_form',__name__,template_folder='templates/purchase_order2')
calculate_net_price_blueprint=Blueprint('calculate_net_price',__name__,template_folder='templates/calculate_net_price')
enter_num_blueprint=Blueprint('enter_num',__name__,template_folder='templates/enter_num')

@purchase_order_blueprint.route('/purchase_order', methods=['POST', 'GET'])
def purchase_order():
    if request.method == 'POST':
        num_products_str=request.form.get('num_input')
        reference_num=request.form.get('Reference_number')
        num_products=int(num_products_str)
        print(f'Just checking if num_products is a {num_products}')
        date_str = request.form.get("date")
        date = datetime.strptime(date_str, '%Y-%m-%d').date()

        # Extract form data for each row
        for row_counter in range(num_products):  # Assuming you have 5 rows
            form_data = {
                'reference_num':reference_num,
                'date': date,
                'serial_number': request.form.get(f"serial_number_{row_counter}"),
                'supplier_name': request.form.get(f"supplier_name_{row_counter}"),
                'supplier_address': request.form.get(f"supplier_address_{row_counter}"),
                'product_name': request.form.get(f"item_name_{row_counter}"),
                'ean_code': request.form.get(f"ean_code_{row_counter}"),
                'color': request.form.get(f"color_{row_counter}"),
                'power': request.form.get(f"power_{row_counter}"),
                'label': request.form.get(f"label_{row_counter}"),
                'packing': request.form.get(f"packing_{row_counter}"),
                'qty': request.form.get(f"qty_{row_counter}"),
                'unit_price': request.form.get(f"unit_price_{row_counter}")
            }
             
            print("Form Data:", request.form)

            # Create a PurchaseOrder instance and add it to the database
            purchase_order = PurchaseOrder(**form_data)
            print([purchase_order])
            db.session.add(purchase_order)
            print(purchase_order.order_id)

        # Commit changes to the database
        db.session.commit()

        
    return redirect(url_for('calculate_net_price.calculate_net_price'))  # Redirect to the home page if not a POST request


@calculate_net_price_blueprint.route('/calculate_net_price', methods=['POST', 'GET'])
def calculate_net_price():
    # Query the database to retrieve purchase orders
    purchase_orders = PurchaseOrder.query.all()

    # Initialize variables for total net price and total quantity
    total_net_price = 0
    total_quantity = 0

    # Calculate net price for each purchase order and update totals
    for purchase_order in purchase_orders:
        purchase_order.net_price = purchase_order.qty * purchase_order.unit_price
        total_net_price += purchase_order.net_price
        total_quantity += purchase_order.qty

    # Assuming no discounts or taxes applied, the total net price equals the total cost
    total_cost = total_net_price

    # Pass data to the template for rendering
    return render_template("calculate_net_price.html", purchase_orders=purchase_orders,
                           total_net_price=total_net_price, total_quantity=total_quantity, total_cost=total_cost)


@success_blueprint.route('/success', methods=['POST', 'GET'])
def success():
    total = request.args.get('total', 0)
    messages = get_flashed_messages()
    return render_template('success.html', total=total, messages=messages)





@purchase_order_form_blueprint.route('/purchase_order_form', methods=['POST', 'GET'])
def purchase_order_form():
    if  request.method == 'POST':
        num_products=request.form.get('num_input')
    return render_template('purchase_order3.html',num_products=int(num_products))

@enter_num_blueprint.route('/enter_num')
def enter_num():
    return render_template('enter_num.html')
   
