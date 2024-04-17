from flask import Blueprint,render_template,redirect,url_for,flash,request
from flask import get_flashed_messages
from sqlalchemy import func
# from my_project.purchase_order.forms import InforForm
from sqlalchemy import insert 
from my_project import db
from my_project.models import Products
from datetime import datetime, timedelta

enter_products_form_blueprint=Blueprint('enter_products_form',__name__,template_folder='templates/products')
enter_num_products_blueprint=Blueprint('enter_num_products',__name__,template_folder='templates/enter_num_products')
view_products_blueprint=Blueprint('view_products',__name__,template_folder='templates/view_products')
products_form_blueprint=Blueprint('products_form',__name__,template_folder='templates/products')
view_products_name_blueprint=Blueprint('view_products_name',__name__,template_folder='templates/view_products_name')
enter_product_name_blueprint=Blueprint('enter_product_name',__name__,template_folder='templates/enter_product_name')

@enter_num_products_blueprint.route('/enter_num_products')
def enter_num_products():
    return render_template("enter_num_products.html")

@enter_products_form_blueprint.route('/enter_products_form', methods=['POST', 'GET'])
def enter_products_form():
    if  request.method == 'POST':
        num_products=request.form.get('num_input')
    return render_template('products.html',num_products=int(num_products))

@products_form_blueprint.route('/products_form', methods=['POST', 'GET'])
def products_form():
     if request.method == 'POST':
        num_products_str=request.form.get('num_input')        
        num_products=int(num_products_str)
        print(f'Just checking if num_products is a {num_products}')
        date_str = request.form.get("date")
        date = datetime.strptime(date_str, '%Y-%m-%d').date()

        # Extract form data for each row
        for row_counter in range(num_products):  # Assuming you have 5 rows
            form_data = {               
                'date': date,
                'id':request.form.get(f"product_id_{row_counter}"),
                'serial_number': request.form.get(f"serial_number_{row_counter}"),
                'supplier_id': request.form.get(f"supplier_name_{row_counter}"),                               
                'product_name': request.form.get(f"product_name_{row_counter}"),
                'product_category': request.form.get(f"product_category_{row_counter}"),
                'product_vertical': request.form.get(f"product_vertical_{row_counter}"),
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
            new_product = Products(**form_data)
            print([new_product])
            db.session.add(new_product)
            print(new_product.id)

        # Commit changes to the database
        db.session.commit()

        return redirect(url_for('view_products.view_products'))
     
@enter_product_name_blueprint.route('/enter_product_name')
def enter_product_name():
     return render_template('enter_product_name.html')


@view_products_name_blueprint.route('/view_products_name',methods=['GET', 'POST'])
def view_products_name():
    product_name=request.form.get('Product_name')
    product_name_view=  Products.query.filter_by(product_name=product_name).all()
    # Query all products
    net_price=0
    net_quantity=0
    total_cost=0
    
    for product in product_name_view:
        net_price+=product.qty * product.unit_price
        net_quantity+=product.qty

    total_cost=net_price  
    
    return render_template('view_products_name.html', product_view_name=product_name_view,total_cost=total_cost,net_price=net_price,net_quantity=net_quantity)



     
@view_products_blueprint.route('/view_products')
def view_products():
    all_products = Products.query.all()  

    return render_template('view_products.html', product_view=all_products)
    




        
    


