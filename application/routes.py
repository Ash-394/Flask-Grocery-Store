# routes.py
from flask import render_template, request, redirect, url_for, flash,Blueprint
from . import db
from flask_login import login_required,current_user
from .models import Section, Product, User,Cart,CartItem,Order
from .auth import is_admin 
import matplotlib
import os

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

routes = Blueprint('routes', __name__)

## Route for admin/store manager dashboard
@routes.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if not is_admin():
        flash('You are not authorized to access this page.', 'error')
        return redirect(url_for('auth.login'))
    sections = Section.query.all()
    is_empty = len(sections) == 0

    # Get products for each section
    products_by_section = {}
    for section in sections:
        products_by_section[section.id] = Product.query.filter_by(section_id=section.id).all()

    return render_template('admin_dashboard.html', user=current_user, sections=sections, is_empty=is_empty, products_by_section=products_by_section)


## Route for admin/store manager to add/edit/remove sections
@routes.route('/admin/dashboard/addsection', methods=['GET', 'POST'])
@routes.route('/admin/dashboard/editsection/<int:section_id>', methods=['GET', 'POST'])
@login_required
def section(section_id=None):
    if not is_admin():
        flash('You are not authorized to access this page.', 'error')
        return redirect(url_for('auth.login'))

    section = None
    if section_id:
        section = Section.query.get(section_id)

    if request.method == 'POST':
       
        if 'remove' in request.form:
            # If 'Remove' button is clicked, remove the section
            db.session.delete(section)
            db.session.commit()
            flash('Section removed successfully!', category='success')
            return redirect(url_for('routes.admin_dashboard'))

        name = request.form.get('sectionname')
        
        if not name:
            flash('Section name cannot be blank!', category='error')
            return render_template('section.html', user=current_user, section=section)

        else:
            if section:
                # If section exists, update its name
                section.name = name
                db.session.commit()
                flash('Section updated successfully!', category='success')
            else:
                # If section does not exist, create a new section
                new_section = Section(name=name)
                db.session.add(new_section)
                db.session.commit()
                flash('New section added successfully!', category='success')

            return redirect(url_for('routes.admin_dashboard'))

    return render_template('section.html', user=current_user, section=section)


## Route for admin/store manager to add/edit/remove products in each sections
@routes.route('/admin/dashboard/<int:section_id>/product', methods=['GET', 'POST'])
@routes.route('/admin/dashboard/<int:section_id>/product/<int:product_id>', methods=['GET', 'POST'])
@login_required
def product(section_id,product_id=None):
    if not is_admin():
        flash('You are not authorized to access this page.', 'error')
        return redirect(url_for('auth.login'))

    product = None
    if product_id:
        product = Product.query.get(product_id)

    if request.method == 'POST':
       
        if 'remove' in request.form:
            # If 'Remove' button is clicked, remove the product
            db.session.delete(product)
            db.session.commit()
            flash('Product removed successfully!', category='success')
            return redirect(url_for('routes.admin_dashboard'))

        name = request.form.get('name')
        price = request.form.get('price')
        quantity = request.form.get('quantity')
        image_url = request.form.get('image_url')
        section_id = request.form.get('section_id')
        date = request.form.get('date')

        sections = Section.query.all()
        # Check if price, quantity, and section_id are not empty
        if price and quantity and section_id:
            price = float(price)
            quantity = int(quantity)
            section_id = int(section_id)
            
            if product:
                # If product exists, update its details
                product.name = name
                product.price = price
                product.quantity = quantity
                product.image_url = image_url
                product.section_id = section_id
                product.date = date
                db.session.commit()
                flash('Product updated successfully!', category='success')
            else:
                # If product does not exist, create a new product
                new_product = Product(name=name, price=price, quantity=quantity, image_url=image_url, section_id=section_id,manufacture_date=date)
                db.session.add(new_product)
                db.session.commit()
                flash('New product added successfully!', category='success')
        else:
            flash('Error: Price, quantity, and section ID are required fields.', category='error')
            return render_template('product.html', user=current_user, product=product, sections=sections)

        return redirect(url_for('routes.admin_dashboard'))

    sections = Section.query.all()

    return render_template('product.html', user=current_user, product=product, sections=sections)


## Route for user dashboard
@routes.route('/user/dashboard', methods=['GET', 'POST'])
@login_required
def user_dashboard():
    search_query = request.args.get('search_query', '')

    if search_query:
        # If search_query is not empty, find sections that match the search query
        sections = Section.query.filter(Section.name.ilike(f"%{search_query}%")).all()

        if sections:
            # If sections are found, get their corresponding products
            products_by_section = {}

            for section in sections:
                products = Product.query.filter(Product.section_id == section.id)
                products_by_section[section.id] = products.all()
        else:
            # If no sections match, show an empty dashboard
            sections = []
            products_by_section = {}    
    else:
        # If no search query, show all products in each section
        sections = Section.query.all()
        products_by_section = {}

        for section in sections:
            products_by_section[section.id] = Product.query.filter_by(section_id=section.id).all()

    return render_template('user_dashboard.html', sections=sections, products_by_section=products_by_section)


## Routes for user to add/update/remive items from cart
@routes.route('/user/cart', methods=['GET', 'POST'])
@login_required
def user_cart():
    # Retrieve the user's cart and associated cart items
    user = current_user
    cart = user.cart
    if not cart:
        cart = Cart(user=user)
        db.session.add(cart)
        db.session.commit()
    cart_items = cart.cart_items if cart else []

    if request.method == 'POST':
        if 'remove' in request.form:
            product_id = int(request.form.get('remove'))
            cart_item_to_remove = next((item for item in cart_items if item.product.id == product_id), None)
            if cart_item_to_remove:
                # Update the product's available quantity in the database
                product = cart_item_to_remove.product
                product.quantity += cart_item_to_remove.quantity
                db.session.delete(cart_item_to_remove)
                db.session.commit()
                return redirect(url_for('routes.user_cart'))

        elif 'add_to_cart' in request.form:
            product_id = int(request.form.get('add_to_cart'))
            product = Product.query.get(product_id)
            quantity=int(request.form.get('quantity'))
            if product:
                # Check if the product is already in the cart
                existing_item = next((item for item in cart_items if item.product.id == product_id), None)
                if existing_item:
                    # If the product is already in the cart, update the quantity
                    existing_item.quantity += quantity
                else:
                    # If the product is not in the cart, add it with quantity 1
                    new_cart_item = CartItem(cart=cart, product=product, quantity=quantity)
                    db.session.add(new_cart_item)
                # Update the product's available quantity in the database
                product.quantity -= quantity
                db.session.commit()
                return redirect(url_for('routes.user_cart'))

        elif 'checkout' in request.form:
            if len(cart_items) == 0:
                flash('Cart is empty. Add products before checking out.', category='error')
                return redirect(url_for('routes.user_cart'))
            
            # Calculate the total amount to be paid for the transaction
            total_amount = sum(item.product.price * item.quantity for item in cart_items)
            # Create a new Order object and store the cart items in it
            new_order = Order(user_id=current_user.id, total_amount=total_amount)
            # Clear the cart by removing all cart items
            for cart_item in cart.cart_items:
            # Set the cart_id of the cart item to None before deleting it
                cart_item.cart_id = None
                db.session.delete(cart_item)

            db.session.delete(cart)
            db.session.commit()

            db.session.add(new_order)
            db.session.commit()

            flash('Checkout successful!', category='success')
            return redirect(url_for('routes.user_dashboard'))

        else:
            for item in cart_items:
                quantity = int(request.form.get(f'quantity_{item.product.id}'))
                # Ensure the quantity is greater than 0 and not more than the available quantity
                quantity = max(0, min(quantity, item.product.quantity))
                # Update the product's available quantity in the database
                product = item.product
                product.quantity += item.quantity - quantity
                item.quantity = quantity

            db.session.commit()
            

    # Calculate the total amount to be paid for the transaction after handling actions
    total_amount = sum(item.product.price * item.quantity for item in cart_items)

    return render_template('user_cart.html', user=user, cart=cart, cart_items=cart_items, total_amount=total_amount)


## Route to show summary to the admin
@routes.route('/admin/summary', methods=['GET'])
@login_required
def generate_summary():
    if not is_admin():
        flash('You are not authorized to access this page.', 'error')
        return redirect(url_for('auth.login'))
    # Retrieve the data from the database
    products = Product.query.all()
    completed_orders = Order.query.all()


    # Calculate summary data
    total_sections = Section.query.count()
    total_products = len(products)
    total_orders = len(completed_orders)
    total_order_amount = sum(order.total_amount for order in completed_orders)

    # Create a dictionary with summary data
    summary_data = {
        'total_sections': total_sections,
        'total_products': total_products,
        'total_orders': total_orders,
        'total_order_amount': total_order_amount,
        # Add more summary data as needed
    }
    

    # Generate the pie chart for product distribution
    section_names = [section.name for section in Section.query.all()]
    section_counts = [len(section.products) for section in Section.query.all()]

    plt.figure(figsize=(8, 6))
    plt.pie(section_counts, labels=section_names, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')  # Equal aspect ratio ensures the pie chart is circular.
    plt.title('Product Distribution by Section')
    path = 'application/static/summary/product_distribution.png'
    if(os.path.exists(path=path)):
            os.remove(path)
    plt.savefig(path)
    plt.close()

    # Generate the bar graph for order amounts
    order_dates = [order.order_date.strftime('%Y-%m-%d') for order in completed_orders]
    order_amounts = [order.total_amount for order in completed_orders]

    plt.figure(figsize=(10, 6))
    plt.bar(order_dates, order_amounts)
    plt.xlabel('Order Date')
    plt.ylabel('Total Order Amount')
    plt.title('Order Amounts by Date')
    plt.xticks(rotation=45)
    plt.tight_layout()
    path = 'application/static/summary/order_amounts.png'
    if(os.path.exists(path=path)):
            os.remove(path)
    plt.savefig(path)
    plt.close()

    # Now, render the summary.html template with the summary data
    return render_template('summary.html', summary_data=summary_data)