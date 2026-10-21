import sqlite3
from pathlib import Path
from flask import current_app,g
SCHEMA="""
CREATE TABLE IF NOT EXISTS schema_meta(version INTEGER NOT NULL);
INSERT INTO schema_meta(version) SELECT 1 WHERE NOT EXISTS(SELECT 1 FROM schema_meta);
CREATE TABLE IF NOT EXISTS products(id INTEGER PRIMARY KEY,name TEXT NOT NULL,category TEXT NOT NULL,sku TEXT UNIQUE,image TEXT,cost REAL NOT NULL CHECK(cost>=0),price REAL NOT NULL CHECK(price>=0),stock INTEGER NOT NULL DEFAULT 0 CHECK(stock>=0),threshold INTEGER NOT NULL DEFAULT 5 CHECK(threshold>=0),description TEXT,created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS customers(id INTEGER PRIMARY KEY,name TEXT NOT NULL,phone TEXT,address TEXT,notes TEXT,created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS sales(id INTEGER PRIMARY KEY,customer_id INTEGER REFERENCES customers(id) ON DELETE SET NULL,customer_name TEXT,customer_phone TEXT,customer_address TEXT,created_at TEXT NOT NULL,subtotal REAL NOT NULL,discount REAL NOT NULL CHECK(discount>=0),total REAL NOT NULL CHECK(total>=0),method TEXT NOT NULL,notes TEXT,status TEXT NOT NULL DEFAULT 'Active' CHECK(status IN ('Active','Voided')));
CREATE TABLE IF NOT EXISTS sale_items(id INTEGER PRIMARY KEY,sale_id INTEGER NOT NULL REFERENCES sales(id),product_id INTEGER REFERENCES products(id) ON DELETE SET NULL,product_name TEXT NOT NULL,category TEXT NOT NULL DEFAULT 'Other',quantity INTEGER NOT NULL CHECK(quantity>0),unit_price REAL NOT NULL CHECK(unit_price>=0),unit_cost REAL NOT NULL CHECK(unit_cost>=0));
CREATE TABLE IF NOT EXISTS payments(id INTEGER PRIMARY KEY,sale_id INTEGER NOT NULL REFERENCES sales(id),amount REAL NOT NULL CHECK(amount>0),method TEXT NOT NULL,paid_at TEXT NOT NULL,note TEXT);
CREATE INDEX IF NOT EXISTS idx_sales_date ON sales(created_at); CREATE INDEX IF NOT EXISTS idx_items_sale ON sale_items(sale_id); CREATE INDEX IF NOT EXISTS idx_customer_phone ON customers(phone);
"""
def connect(path):
 c=sqlite3.connect(path); c.row_factory=sqlite3.Row; c.execute('PRAGMA foreign_keys=ON'); return c
def get_db():
 if 'db' not in g: g.db=connect(Path(current_app.config['DATA_DIR'])/'business.sqlite3')
 return g.db
def close_db(e=None):
 c=g.pop('db',None)
 if c: c.close()
def init_app(app):
 app.teardown_appcontext(close_db)
 c=connect(Path(app.config['DATA_DIR'])/'business.sqlite3'); c.executescript(SCHEMA)
 columns={row['name'] for row in c.execute('PRAGMA table_info(sale_items)')}
 if 'category' not in columns: c.execute("ALTER TABLE sale_items ADD COLUMN category TEXT NOT NULL DEFAULT 'Other'")
 c.execute("UPDATE schema_meta SET version=2")
 c.close()

