#!/usr/bin/python3
"""A Flask application that renders dynamic content with Jinja logic."""
import json
import os

from flask import Flask, render_template

app = Flask(__name__)

ITEMS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          'items.json')


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


if __name__ == '__main__':
    app.run(debug=True, port=5000)
