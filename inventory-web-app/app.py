from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'inventory-secret-key'

inventory = {}
sales_data = []

@app.route('/')
def index():
    return render_template('index.html', inventory=inventory)

@app.route('/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        product_id = request.form['product_id']
        name = request.form['name']
        try:
            price = float(request.form['price'])
            quantity = int(request.form['quantity'])
        except ValueError:
            flash("Invalid price or quantity", "error")
            return redirect(url_for('add_product'))

        if product_id in inventory:
            flash("Product ID already exists", "error")
        else:
            inventory[product_id] = {'name': name, 'price': price, 'quantity': quantity}
            flash(f"Product '{name}' added successfully.", "success")
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/sell/<product_id>', methods=['POST'])
def sell_product(product_id):
    try:
        quantity = int(request.form['quantity'])
    except ValueError:
        flash("Invalid quantity", "error")
        return redirect(url_for('index'))

    if product_id in inventory:
        if inventory[product_id]['quantity'] >= quantity:
            inventory[product_id]['quantity'] -= quantity
            revenue = quantity * inventory[product_id]['price']
            sales_data.append({'product_id': product_id, 'quantity': quantity, 'revenue': revenue})
            flash("Sale successful.", "success")
        else:
            flash("Not enough stock.", "error")
    else:
        flash("Product not found.", "error")
    return redirect(url_for('index'))

@app.route('/restock/<product_id>', methods=['POST'])
def restock_product(product_id):
    try:
        quantity = int(request.form['quantity'])
    except ValueError:
        flash("Invalid quantity", "error")
        return redirect(url_for('index'))

    if product_id in inventory:
        inventory[product_id]['quantity'] += quantity
        flash("Product restocked successfully.", "success")
    else:
        flash("Product not found.", "error")
    return redirect(url_for('index'))

@app.route('/report')
def sales_report():
    total_items = sum(sale['quantity'] for sale in sales_data)
    total_revenue = sum(sale['revenue'] for sale in sales_data)
    return render_template('report.html', total_items=total_items, total_revenue=total_revenue)

if __name__ == '__main__':
    app.run(debug=True)