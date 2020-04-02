from flask import Flask, redirect, url_for, jsonify
import os
from dotenv import load_dotenv
from dbsetup import db

app = Flask('api')

def remove_tuple(t):
    return str(t[0])

@app.route('/category/<string:product_id>/<int:count>')
def category(product_id, count):
    cur = db.cursor()

    cur.execute("""
        SELECT category
        FROM products
        WHERE id = %s
    """, (product_id,))

    category = remove_tuple(cur.fetchone())

    cur.execute("""
        SELECT *
        FROM products
        WHERE category = %s
        ORDER BY RANDOM();
    """, (category,))

    product_ids = list(map(remove_tuple, cur.fetchmany(count)))

    cur.close()

    return jsonify(product_ids)

@app.route('/profile/<string:profile_id>/<int:count>')
def profile(profile_id, count):
    cur = db.cursor()

    cur.execute("""
        SELECT id
        FROM products
        ORDER BY RANDOM();
    """)

    product_ids = list(map(remove_tuple, cur.fetchmany(count)))

    cur.close()

    return jsonify(product_ids)

@app.route('/others_bought/<string:product_id>/<int:count>')
def others(product_id, count):
    pass

app.run(host='0.0.0.0', debug=True, port=5001)
