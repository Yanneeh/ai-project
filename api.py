from flask import Flask, redirect, url_for, jsonify
import os
from dotenv import load_dotenv
from dbsetup import db
from func import *
import ast

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

@app.route('/others_bougth_cart/<string:product_ids>/<int:count>')
def others_cart(product_ids, count):
    ids = ast.literal_eval(product_ids)
    ids = tuple(ids)

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
		           where product_id in %s)
	        and product_id not in %s) as id
        group by product_id
        order by count(*) desc;
    """, (ids, ids))

    # Fetch een n aantal ids op basis van count die meegestuurd is.
    product_ids = fetch_amount(cur, count)

    cur.close()

    # Product ids worden teruggestuurd.
    return jsonify(product_ids)

@app.route('/most/<string:this_category>/<int:cat_count>/<int:count>')
def most(this_category, cat_count, count):
    cur = db.cursor()

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

@app.route('/product/<string:product>/<int:count>')
def product(product, count):

    this_product = ast.literal_eval(product)

    cur = db.cursor()

    cur.execute("""
    select id from(
        select id, (gender + cat + subcat + subsubcat + brand) as Total from
            (select id,
                sum(case when gender like %s then 1 else 0 end) AS gender,
	    	    sum(case when category = %s then 1 else 0 end) as cat,
	    	    sum(case when sub_category = %s then 1 else 0 end) as subcat,
	    	    sum(case when sub_sub_category = %s then 1 else 0 end) as subsubcat,
	    	    sum(case when brand = %s then 1 else 0 end) as brand
	        from products
	        where id != %s
	        group by id)
	    as id
	    order by Total desc)
	as id;
    """, (this_product[1], this_product[2], this_product[3], this_product[4], this_product[5], this_product[0]))

    product_ids = fetch_amount(cur, count)

    cur.close()

    return jsonify(product_ids)

app.run(host='0.0.0.0', debug=True, port=5001)
