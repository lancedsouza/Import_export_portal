from sqlalchemy import Column, Integer, ForeignKey, String, Float, Date
from sqlalchemy.orm import relationship

from my_project import db

class Supplier(db.Model):
    __tablename__ = 'supplier'
    serial_number = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date) 
    supplier_id = db.Column(db.Integer, primary_key=True, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))  # Make sure 'id' is lowercase
    supplier_name = db.Column(db.String(50), nullable=False)
    supplier_address = db.Column(db.String(255), nullable=False)
    country = db.Column(db.String(50), nullable=True)
    currency = db.Column(db.String(50), nullable=True)
    qty = db.Column(db.Integer, nullable=False)

    

class Products(db.Model):
    __tablename__ = 'products'

    date = db.Column(db.Date) 
    id = db.Column(db.Integer, primary_key=True)
    serial_number = db.Column(db.Integer, nullable=False)
    product_name = db.Column(db.String(255), nullable=False)
    supplier_id=Column(Integer, ForeignKey('supplier.supplier_id'))
    product_category = db.Column(db.String(50), nullable=True)
    product_vertical = db.Column(db.String(20), nullable=True)
    ean_code = db.Column(db.String(20), nullable=False)
    color = db.Column(db.String(20), nullable=False)
    power = db.Column(db.String(20), nullable=False)
    label = db.Column(db.String(20), nullable=False)
    packing = db.Column(db.String(20), nullable=False)        
    unit_price = db.Column(db.Float, nullable=False)
    country = db.Column(db.String(50), nullable=True)
    currency = db.Column(db.String(50), nullable=True)
    qty = db.Column(db.Integer, nullable=False)

    # One to Many relationship
    
    # One to Many relationship
    purchase_order = db.relationship('PurchaseOrder', backref='products', foreign_keys='PurchaseOrder.product_id')

    def __repr__(self):
        return f"Product name is {self.product_name} product_id is {self.id} and  supplier_id is {self.supplier_id} and quantity is {self.qty}"

class PurchaseOrder(db.Model):
    __tablename__ = 'purchase_order'
    reference_num=db.Column(db.String(50), nullable=False,primary_key=True)
    order_id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)  # Added date column
    serial_number = db.Column(db.Integer, nullable=False)
    ean_code= db.Column(db.String(50), nullable=False)    
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.supplier_id'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))  # Make sure 'id' is lowercase
    qty = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)        
    product_name=db.Column(db.String(50), nullable=False)
    color = db.Column(db.String(20), nullable=False)
    power = db.Column(db.String(20), nullable=False)
    label = db.Column(db.String(20), nullable=False)
    packing = db.Column(db.String(20), nullable=False)
    supplier_name = db.Column(db.String(50), nullable=False)
    supplier_address = db.Column(db.String(255), nullable=False)


    

    def __repr__(self):
        return f'<PurchaseOrder {self.order_id}>'
