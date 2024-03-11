from flask import Blueprint,render_template,redirect,url_for,flash,request
from my_project import db
from my_project.models import PurchaseOrder
from datetime import datetime, timedelta

purchase_order_blueprint = Blueprint('purchase_order',__name__,template_folder='templates/purchase_order')
success_blueprint= Blueprint('success',__name__,template_folder='templates/success')

@purchase_order_blueprint.route('/purchase_order', methods=['POST','GET'])
def purchase_order():
    if request.method == 'POST':
        # Extract form data
        date = request.form.get('Date')  # Use None as a default value
        serial_number = request.form.get('serial_number')
        supplier_name = request.form.get('Supplier_Name')
        supplier_address = request.form.get('address')
        date = request.form.get('Date', None)  # First extraction
        product_name = request.form.get('product_name')
        ean_code = request.form.get('EAN_CODE')
        color = request.form.get('color')
        power = request.form.get('power')
        label = request.form.get('label')
        packing = request.form.get('packing')
        qty=float(request.form.get('Qty')) if request.form.get('Qty') is not None else 0.0
        unit_price = float(request.form.get('Unit_Price')) if request.form.get('Unit_Price') is not None else 0.0
        net_price = float(request.form.get('Net_Price')) if request.form.get('Net_Price') is not None else 0.0
        total = float(request.form.get('total')) if request.form.get('total') is not None else 0.0


        # Process the form data and save it to the database
        new_order = PurchaseOrder(
            serial_number=serial_number,
            supplier_name=supplier_name,
            supplier_address=supplier_address,
            date=date,
            product_name=product_name,
            ean_code=ean_code,
            color=color,
            power=power,
            label=label,
            packing=packing,
            qty=qty,
            unit_price=unit_price,
            net_price=net_price,
            total=total
        )

        try:
            db.session.add(new_order)
            db.session.commit()
            flash("Order added successfully!", "success")
        except Exception as e:
            db.session.rollback()  # Rollback changes in case of an error
            print(f"Error inserting data into the database: {e}")
            

            # Redirect or render a response
    return render_template('purchase_order.html')


@success_blueprint.route('/success', methods=['POST','GET'])
def success():
    if request.method == 'POST':
        total = request.form.get('total')
        return render_template('success.html', total=total)