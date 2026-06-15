from flask import Flask, render_template, request, redirect, session

# IMPORT DATABASE CONNECTION
from database import db, cursor

app = Flask(__name__)
app.secret_key = "secret123"

# ======================
# ROUTES
# ======================

@app.route('/')
def home():
    return render_template('index.html')

# REGISTER
@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']

    cursor.execute(
        "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
        (username, email, password)
    )
    db.commit()

    return redirect('/login')

# LOGIN PAGE
@app.route('/login')
def login_page():
    return render_template('login.html')

# LOGIN LOGIC
@app.route('/login_user', methods=['POST'])
def login_user():
    email = request.form['email']
    password = request.form['password']

    cursor.execute(
        "SELECT * FROM users WHERE email=%s AND password=%s",
        (email, password)
    )
    user = cursor.fetchone()

    if user:
        session['user_id'] = user[0]
        return redirect('/dashboard')   # ✅ FIXED
    else:
        return "Invalid Login"

# LOGOUT
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/login')

# ======================
# DASHBOARD
# ======================

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')

    # COUNT DATA
    cursor.execute("SELECT COUNT(*) FROM users")
    users = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM items")
    items = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM bids")
    bids = cursor.fetchone()[0]

    return render_template(
        'dashboard.html',
        users=users,
        items=items,
        bids=bids
    )

# ======================
# MAIN FUNCTIONALITY
# ======================

# VIEW ITEMS (USED FOR ADD/BID PAGE)
@app.route('/items')
def items():
    if 'user_id' not in session:
        return redirect('/login')

    cursor.execute("SELECT * FROM items")
    items = cursor.fetchall()

    return render_template('items.html', data=items)

# ADD ITEM
@app.route('/add_item', methods=['POST'])
def add_item():
    if 'user_id' not in session:
        return redirect('/login')

    title = request.form['title']
    description = request.form['description']
    price = request.form['price']

    cursor.execute(
        "INSERT INTO items (title, description, starting_price, user_id) VALUES (%s, %s, %s, %s)",
        (title, description, price, session['user_id'])
    )
    db.commit()

    return redirect('/items')

# PLACE BID
@app.route('/bid/<int:item_id>', methods=['POST'])
def bid(item_id):
    amount = request.form['amount']

    cursor.execute(
        "INSERT INTO bids (amount, user_id, item_id) VALUES (%s, %s, %s)",
        (amount, session['user_id'], item_id)
    )
    db.commit()

    return redirect('/items')

# ======================
# TABLE PAGES (IMPORTANT)
# ======================

@app.route('/users')
def users():
    cursor.execute("SELECT * FROM users")
    data = cursor.fetchall()
    return render_template('users.html', data=data)

@app.route('/items_page')
def items_page():
    cursor.execute("SELECT * FROM items")
    data = cursor.fetchall()
    return render_template('items.html', data=data)

@app.route('/bids')
def bids_page():
    cursor.execute("SELECT * FROM bids")
    data = cursor.fetchall()
    return render_template('bids.html', data=data)

@app.route('/categories')
def categories():
    cursor.execute("SELECT * FROM categories")
    data = cursor.fetchall()
    return render_template('categories.html', data=data)

@app.route('/watchlist')
def watchlist():
    cursor.execute("SELECT * FROM watchlist")
    data = cursor.fetchall()
    return render_template('watchlist.html', data=data)

@app.route('/auctions')
def auctions():
    cursor.execute("SELECT * FROM auctions")
    data = cursor.fetchall()
    return render_template('auctions.html', data=data)

@app.route('/payments')
def payments():
    cursor.execute("SELECT * FROM payments")
    data = cursor.fetchall()
    return render_template('payments.html', data=data)

# ======================
# HELPER FUNCTION
# ======================

def get_highest_bid(item_id):
    cursor.execute("SELECT MAX(amount) FROM bids WHERE item_id=%s", (item_id,))
    result = cursor.fetchone()[0]
    return result if result else "No bids"

app.jinja_env.globals.update(get_highest_bid=get_highest_bid)

# ADD CATEGORY
@app.route('/add_category', methods=['POST'])
def add_category():
    name = request.form['category_name']

    cursor.execute(
        "INSERT INTO categories (category_name) VALUES (%s)",
        (name,)
    )
    db.commit()

    return redirect('/categories')


# ADD AUCTION
@app.route('/add_auction', methods=['POST'])
def add_auction():
    item_id = request.form['item_id']
    start = request.form['start_time']
    end = request.form['end_time']

    cursor.execute(
        "INSERT INTO auctions (item_id, start_time, end_time) VALUES (%s, %s, %s)",
        (item_id, start, end)
    )
    db.commit()

    return redirect('/auctions')


# ADD PAYMENT
@app.route('/add_payment', methods=['POST'])
def add_payment():
    user_id = request.form['user_id']
    item_id = request.form['item_id']
    amount = request.form['amount']

    cursor.execute(
        "INSERT INTO payments (user_id, item_id, amount) VALUES (%s, %s, %s)",
        (user_id, item_id, amount)
    )
    db.commit()

    return redirect('/payments')


# ADD WATCHLIST
@app.route('/add_watchlist', methods=['POST'])
def add_watchlist():
    user_id = request.form['user_id']
    item_id = request.form['item_id']

    cursor.execute(
        "INSERT INTO watchlist (user_id, item_id) VALUES (%s, %s)",
        (user_id, item_id)
    )
    db.commit()

    return redirect('/watchlist')
# ======================
# RUN (ALWAYS LAST)
# ======================

if __name__ == '__main__':
    app.run(debug=True)