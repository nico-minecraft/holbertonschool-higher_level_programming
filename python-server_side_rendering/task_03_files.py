#!/usr/bin/python3
"""A Flask application that displays products from JSON or CSV files."""
import csv
import json
import os

from flask import Flask, render_template, request

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_FILE = os.path.join(BASE_DIR, 'products.json')
CSV_FILE = os.path.join(BASE_DIR, 'products.csv')
ITEMS_FILE = os.path.join(BASE_DIR, 'items.json')


def read_json_products():
    """Return the list of products stored in products.json."""
    with open(JSON_FILE, 'r') as file:
        return json.load(file)


def read_csv_products():
    """Return the list of products stored in products.csv."""
    products = []
    with open(CSV_FILE, 'r', newline='') as file:
        for row in csv.DictReader(file):
            products.append({
                'id': int(row['id']),
                'name': row['name'],
                'category': row['category'],
                'price': float(row['price'])
            })
    return products


@app.route('/')
def home():
    """Render the home page."""
    return render_template('index.html')


@app.route('/about')
def about():
    """Render the about page."""
    return render_template('about.html')


@app.route('/contact')
def contact():
    """Render the contact page."""
    return render_template('contact.html')


@app.route('/items')
def items():
    """Read the items from items.json and render them."""
    try:
        with open(ITEMS_FILE, 'r') as file:
            items_list = json.load(file).get('items', [])
    except (OSError, ValueError, AttributeError):
        items_list = []
    return render_template('items.html', items=items_list)


@app.route('/products')
def products():
    """Display products from a JSON or CSV file, optionally filtered by id."""
    source = request.args.get('source')
    product_id = request.args.get('id')

    if source == 'json':
        reader = read_json_products
    elif source == 'csv':
        reader = read_csv_products
    else:
        return render_template('product_display.html',
                               error='Wrong source')

    try:
        data = reader()
    except (OSError, ValueError, KeyError):
        return render_template('product_display.html',
                               error='Could not read the data file')

    if product_id is not None:
        data = [p for p in data if str(p['id']) == product_id.strip()]
        if not data:
            return render_template('product_display.html',
                                   error='Product not found')

    return render_template('product_display.html', products=data)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
