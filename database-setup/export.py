from dotenv import load_dotenv, find_dotenv
import psycopg2

def export_csv(db, filename, tablename):
    cur = db.cursor()

    f = open(filename, 'r')

    copy = f""" COPY {tablename} FROM stdin WITH CSV HEADER
            DELIMITER as ','"""

    cur.copy_expert(sql=copy, file=f)

    db.commit()
    cur.close()

def export_products(db):
    export_csv(db, 'products.csv', 'products')

def export_profiles(db):
    export_csv(db, 'profiles.csv', 'profiles')

def export_orders(db):
    export_csv(db, 'orders.csv', 'orders(session_id, product_id)')

def export_sessions(db):
    export_csv(db, 'sessions.csv', 'sessions')

def export_recommended(db):
    export_csv(db, 'recommended.csv', 'recommended(profile_id, product_id)')


load_dotenv(find_dotenv())

db = psycopg2.connect(dbname=os.getenv("DBNAME"), user=os.getenv("DBUSER"), password=os.getenv("DBPASSWORD"))

export_orders(db)
export_profiles(db)
export_orders(db)
export_sessions(db)
export_recommended(db)

db.close()

#test2