from flask import Blueprint,render_template,redirect,url_for,flash,request
from flask import get_flashed_messages
# from my_project.purchase_order.forms import InforForm
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


@purchase_order_blueprint.route('/purchase_order', methods=['POST', 'GET'])
def purchase_order():
    print("Entering purchase_order function")

    if request.method == 'POST':
        print("Form Data:", request.form)

        date_str = request.form.get("date")
        date = datetime.strptime(date_str, '%Y-%m-%d').date()

        # Extract form data for each row
        # Counter for tracking the row number
        row_counter = 1
        serial_numbers = []
        print(serial_numbers)
        product_names = []
        ean_codes = []
        colors = []
        powers = []
        labels = []
        packings = []
        qtys = []
        supplier_names = []
        supplier_addresses = []
        unit_prices = []

        # Loop until all rows are processed
        while len(request.form.getlist('serial_number')) >= row_counter:
            serial_number = request.form.get(f'serial_number_{row_counter}')
            print(f"this is serial number{row_counter}")
            product_name = request.form.get(f'product_name_{row_counter}')
            ean_code = request.form.get(f'EAN_CODE_{row_counter}')
            color = request.form.get(f'color_{row_counter}')
            power = request.form.get(f'power_{row_counter}')
            label = request.form.get(f'label_{row_counter}')
            packing = request.form.get(f'packing_{row_counter}')
            qty = request.form.get(f'Qty_{row_counter}')
            supplier_name = request.form.get(f'Supplier_Name_{row_counter}')
            supplier_address = request.form.get(f'address_{row_counter}')
            unit_price = request.form.get(f'Unit_Price_{row_counter}')

            # Append the extracted data to the respective lists
            serial_numbers.append(serial_number)
            product_names.append(product_name)
            ean_codes.append(ean_code)
            colors.append(color)
            powers.append(power)
            labels.append(label)
            packings.append(packing)
            qtys.append(qty)
            supplier_names.append(supplier_name)
            supplier_addresses.append(supplier_address)
            unit_prices.append(unit_price)

            row_counter += 1

        # Calculate Net Price and total
        net_prices = [float(unit_price) * float(qty) for unit_price, qty in zip(unit_prices, qtys)]
        

        import sqlite3

        # Assuming you have already created the database file (e.g., my_database.db)
        db_path = 'C:\\Users\\Wishes Lawrence\\Desktop\\lace-data1\\Desktop\\Import_Software\\my_project\\data.sqlite3'
        db_connection = sqlite3.connect(db_path)
        db_cursor = db_connection.cursor()

        # Iterate through the zipped values and execute an insert statement for each row
        purchase_orders = list(zip(
            serial_numbers, product_names, colors, powers, labels, ean_codes, packings, qtys,
            supplier_names, supplier_addresses, unit_prices, net_prices
        ))
        print(f'list for {purchase_orders}')

        try:
            # Use executemany to insert multiple rows at once
            insert_query = """
                INSERT INTO purchase_order
                (serial_number, product_name, date, color, power, label, ean_code, packing, qty, supplier_name, supplier_address, unit_price, net_price, total)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            db_cursor.execute(insert_query, purchase_orders)

            # Commit the changes to the database
            db_connection.commit()
            flash("Orders added successfully!", "success")
        except Exception as e:
            # Rollback changes in case of an error
            db_connection.rollback()
            flash(f"Error adding orders: {e}", "error")
        finally:
            # Close the cursor and connection
            db_cursor.close()
            db_connection.close()

    return redirect(url_for('calculate_net_price.calculate_net_price'))



@success_blueprint.route('/success', methods=['POST', 'GET'])
def success():
    total = request.args.get('total', 0)
    messages = get_flashed_messages()
    return render_template('success.html', total=total, messages=messages)



@calculate_net_price_blueprint.route('/calculate_net_price', methods=['GET', 'POST'])
def calculate_net_price():
  
    # Retrieve data from the database, for example, all PurchaseOrders
    purchase_orders = PurchaseOrder.query.all()

    
    # Pass data to the template    
    return render_template('calculate_net_price.html') 


@purchase_order_form_blueprint.route('/purchase_order_form')
def purchase_order_form():
    return render_template('purchase_order2.html')