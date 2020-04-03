from flask import Flask, redirect, url_for, jsonify
import os
from dotenv import load_dotenv
from dbsetup import db
from func import *

app = Flask(__name__)
app.secret_key = os.urandom(16)

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

    product_ids = fetch_amount(cur, count)

    cur.close()

    return jsonify(product_ids)

@app.route('/personal/<string:profile_id>/<int:count>')
def profile(profile_id, count):
    cur = db.cursor()

    cur.execute("""
        SELECT id
        FROM products
        ORDER BY RANDOM();
    """)

    product_ids = fetch_amount(cur, count)

    cur.close()

    return jsonify(product_ids)

@app.route('/popular/<string:product_id>/<int:count>')
def others(product_id, count):
    cur = db.cursor()

    cur.execute("""
        select product_id
        from
        (select distinct product_id
        from orders
        where session_id in
        (select session_id
        from orders
        where product_id = %s) and product_id != %s) as id
        order by random();
    """, (product_id, product_id))

    product_ids = fetch_amount(cur, count)

    cur.close()

    return jsonify(product_ids)

app.run(host='0.0.0.0', debug=True, port=5001)
