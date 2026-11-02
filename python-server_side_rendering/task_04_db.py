#!/usr/bin/python3
"""A Flask app that displays products from JSON, CSV or SQLite sources."""
import csv
import json
import os
import sqlite3
from pathlib import Path

from flask import Flask, render_template, request

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_FILE = os.path.join(BASE_DIR, 'products.json')
CSV_FILE = os.path.join(BASE_DIR, 'products.csv')
DB_FILE = os.path.join(BASE_DIR, 'products.db')
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


def read_sql_products():
    """Return the list of products stored in the Products table."""
    # Open read-only so a missing file is an error, not a new empty database.
    conn = sqlite3.connect(Path(DB_FILE).as_uri() + '?mode=ro', uri=True)
    try:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            'SELECT id, name, category, price FROM Products').fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


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
    """Display products from a JSON, CSV or SQL source, filtered by id."""
    source = request.args.get('source')
    product_id = request.args.get('id')

    readers = {
        'json': read_json_products,
        'csv': read_csv_products,
        'sql': read_sql_products
    }
    if source not in readers:
        return render_template('product_display.html',
                               error='Wrong source')

    try:
        data = readers[source]()
    except sqlite3.Error:
        return render_template('product_display.html',
                               error='Database error')
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
