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

    # Vind de categorie die bij het product id hoort.
    cur.execute("""
        SELECT category
        FROM products
        WHERE id = %s
    """, (product_id,))

    category = remove_tuple(cur.fetchone())

    # Vind een aantal producten die de categorie uit de vorige query hebben en randomize de uitkomst.
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
    # Deze functie is gemaakt om de werking van de testomgeving te testen om de andere twee recommendations te maken.

    cur = db.cursor()

    # Selecteer een aantal random producten.
    cur.execute("""
        SELECT id
        FROM products
        ORDER BY RANDOM();
    """)

    product_ids = fetch_amount(cur, count)

    cur.close()

    return jsonify(product_ids)

@app.route('/others_bougth/<string:product_id>/<int:count>')
def others(product_id, count):
    cur = db.cursor()
    # De query die producten selecteert die in het verleden vaker dan 10 keer samen zijn gekocht.
    cur.execute("""
        select product_id
        from
	       (select product_id
	        from orders
	        where session_id in
		          (select session_id
		           from orders
		           where product_id = %s)
	        and product_id != %s) as id
        group by product_id
        order by count(*) desc;
    """, (product_id, product_id))

    # Fetch een n aantal ids op basis van count die meegestuurd is.
    product_ids = fetch_amount(cur, count)

    cur.close()

    # Product ids worden teruggestuurd.
    return jsonify(product_ids)

@app.route('/most/<string:this_category>/<int:cat_count>/<int:count>')
def most(this_category, cat_count, count):
    cur = db.cursor()

    this_category = this_category.replace('-en-', ' & ')
    this_category = this_category.replace('-', ' ')
    this_category = this_category.capitalize()

    categories = ['category', 'sub_category', 'sub_sub_category', 'sub_sub_sub_category']

    if categories[cat_count] == 'category':
        cur.execute("""
            select product_id from
                (select product_id from
                orders where session_id in
                    (select session_id from orders
                    where product_id in
                        (select id from products where
                        category = %s)
                    )
                )
            as id group by product_id
            order by count(*) desc;
        """, (this_category,))
    elif categories[cat_count] == 'sub_category':
        cur.execute("""
                    select product_id from
                        (select product_id from
                        orders where session_id in
                            (select session_id from orders
                            where product_id in
                                (select id from products where
                                sub_category = %s)
                            )
                        )
                    as id group by product_id
                    order by count(*) desc;
                """, (this_category,))

    # Fetch een n aantal ids op basis van count die meegestuurd is.
    product_ids = fetch_amount(cur, count)

    cur.close()

    # Product ids worden teruggestuurd.
    return jsonify(product_ids)

app.run(host='0.0.0.0', debug=True, port=5001)
