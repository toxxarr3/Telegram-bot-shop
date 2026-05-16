import psycopg2, json



def con(func):
    def wr(*args, **kwargs):
        conn = psycopg2.connect(dbname="tgshop", user="postgres", password="1234", host="localhost")
        try:
            cur = conn.cursor()
            res = func(cur, *args, **kwargs)
            conn.commit()
            return res
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
    return wr

@con
def adduser(cur, userid, username):
     cur.execute("""insert into users(tgid, username, cart)
                  values (%s, %s, '')""", (userid, username))

@con
def useridinbase(cur, userid: int):
    cur.execute("select tgid from users")
    a=cur.fetchall()
    for i in a:
        if userid in i:
            return 1
            break
    return 0

@con
def allcats(cur):
    cur.execute("select distinct cat from products")
    catss=[]
    cats=cur.fetchall()
    for c in cats:
            catss.append(c[0])
    return catss

@con
def getuserid(cur, tguserid):
    cur.execute("select id from users where tgid=%s", (tguserid,))
    return cur.fetchone()

@con
def prodsincat(cur, cat):
    cur.execute("select name from products where cat=%s", (cat,))
    prods=cur.fetchall()
    prodss=[]
    for p in prods:
        prodss.append(p[0])
    return prodss

@con
def add_to_cart(cur, tgid, prod_name, qty=1):
    cur.execute("SELECT cart FROM users WHERE tgid=%s", (tgid,))
    ress = cur.fetchone()
    
    if ress and ress[0]:
        try:
            cart = json.loads(ress[0])
        except json.JSONDecodeError:
            cart = {}
    else:
        cart = {}
        
    cart[prod_name] = cart.get(prod_name, 0) + qty
    cur.execute("UPDATE users SET cart=%s WHERE tgid=%s", (json.dumps(cart, ensure_ascii=False), tgid))

@con
def add_order(cur, userid, cart, address, price):
    cur.execute("insert into orders(userid, cart, address, price) values(%s, %s, %s, %s)", (userid, json.dumps(cart, ensure_ascii=False), address, price))

@con
def showcart(cur, tgid):
    cur.execute("SELECT cart FROM users WHERE tgid=%s", (tgid,))
    res = cur.fetchone()
    if res and res[0]:
        try:
            return json.loads(res[0])
        except json.JSONDecodeError:
            return {}
    return {}

@con
def show_orders(cur, tgid):
    cur.execute("""select o.cart, o.address, o.price from orders o
join users u on o.userid=u.id where u.tgid=%s;""", (tgid, ))
    return cur.fetchall()

@con
def getorder(cur, userid):
    cur.execute("select cart from orders where userid=%s", (userid,))
    return json.loads(cur.fetchone()[0])

@con
def clearcart(cur, tgid):
    cur.execute("UPDATE users SET cart=%s WHERE tgid=%s", (json.dumps({}, ensure_ascii=False), tgid))


@con
def prod_info(cur, prodname):
    cur.execute("select description, price, photo from products where name=%s", (prodname, ))
    a=cur.fetchall()
    a=a[0]
    c=[]
    for b in a:
        c.append(b)
    return c