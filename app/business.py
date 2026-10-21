from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
from .db import get_db
try:
 TZ=ZoneInfo('Asia/Dhaka')
except ZoneInfoNotFoundError:
 # Windows may not have tzdata installed; Bangladesh currently uses UTC+06 year-round.
 TZ=timezone(timedelta(hours=6),name='Asia/Dhaka')
def now(): return datetime.now(TZ).isoformat(timespec='seconds')
def local_today(): return datetime.now(TZ).date()
def record_sale(customer_id,guest_name,phone,address,rows,discount,paid,method,notes=''):
 db=get_db(); prepared=[]; subtotal=0
 if not rows: raise ValueError('Add at least one product to the sale')
 for row in rows:
  p=db.execute('SELECT * FROM products WHERE id=?',(int(row['product_id']),)).fetchone()
  if not p: raise ValueError('Product not found')
  q=int(row['quantity']); price=round(float(row.get('unit_price',p['price'])),2)
  if q<=0 or price<0: raise ValueError('Quantity must be positive and price nonnegative')
  if p['stock']<q: raise ValueError(f"Not enough stock for {p['name']}")
  prepared.append((p,q,price)); subtotal+=q*price
 discount=round(float(discount),2); paid=round(float(paid),2); total=round(subtotal-discount,2)
 if method not in ('Cash','bKash','Nagad','Bank','Card','Other'): raise ValueError('Choose a valid payment method')
 if discount<0 or discount>subtotal: raise ValueError('Discount must be between zero and subtotal')
 if paid<0 or paid>total: raise ValueError('Payment cannot exceed order total')
 cust=db.execute('SELECT * FROM customers WHERE id=?',(customer_id,)).fetchone() if customer_id else None
 name=cust['name'] if cust else (guest_name.strip() or 'Walk-in'); phone=cust['phone'] if cust else phone.strip(); address=cust['address'] if cust else address.strip()
 with db:
  cur=db.execute('INSERT INTO sales(customer_id,customer_name,customer_phone,customer_address,created_at,subtotal,discount,total,method,notes) VALUES(?,?,?,?,?,?,?,?,?,?)',(customer_id,name,phone,address,now(),round(subtotal,2),discount,total,method,notes)); sid=cur.lastrowid
  for p,q,price in prepared:
   db.execute('INSERT INTO sale_items(sale_id,product_id,product_name,category,quantity,unit_price,unit_cost) VALUES(?,?,?,?,?,?,?)',(sid,p['id'],p['name'],p['category'],q,price,p['cost']))
   if db.execute('UPDATE products SET stock=stock-? WHERE id=? AND stock>=?',(q,p['id'],q)).rowcount!=1: raise ValueError('Insufficient stock')
  if paid: db.execute('INSERT INTO payments(sale_id,amount,method,paid_at) VALUES(?,?,?,?)',(sid,paid,method,now()))
 return sid
def add_payment(sale_id,amount,method,note=''):
 db=get_db(); amount=round(float(amount),2); sale=db.execute('SELECT total,status FROM sales WHERE id=?',(sale_id,)).fetchone(); got=db.execute('SELECT COALESCE(SUM(amount),0) FROM payments WHERE sale_id=?',(sale_id,)).fetchone()[0]
 if method not in ('Cash','bKash','Nagad','Bank','Card','Other'): raise ValueError('Choose a valid payment method')
 if amount<=0 or not sale or sale['status']!='Active' or amount>sale['total']-got: raise ValueError('Invalid payment or amount exceeds balance')
 with db: db.execute('INSERT INTO payments(sale_id,amount,method,paid_at,note) VALUES(?,?,?,?,?)',(sale_id,amount,method,now(),note))
def void_sale(sale_id):
 db=get_db(); sale=db.execute('SELECT status FROM sales WHERE id=?',(sale_id,)).fetchone()
 if not sale or sale['status']!='Active': raise ValueError('Active sale not found')
 with db:
  for i in db.execute('SELECT product_id,quantity FROM sale_items WHERE sale_id=?',(sale_id,)).fetchall():
   if i['product_id']: db.execute('UPDATE products SET stock=stock+? WHERE id=?',(i['quantity'],i['product_id']))
  db.execute("UPDATE sales SET status='Voided' WHERE id=?",(sale_id,))






