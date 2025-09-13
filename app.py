from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-change-in-prod'
DB_PATH = 'yumm.db'


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            phone TEXT NOT NULL,
            guests INTEGER NOT NULL,
            booking_datetime TEXT NOT NULL,
            special_requests TEXT,
            created_at TEXT NOT NULL
        );
        """
    )
    conn.commit()
    conn.close()
    


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/menu')
def menu():
    # Static menu page (HTML/CSS only)
    return render_template('menu.html')


@app.route('/book', methods=['GET', 'POST'])
def book_table():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        phone = request.form.get('phone', '').strip()
        guests = request.form.get('guests', '').strip()
        date = request.form.get('date', '').strip()
        time = request.form.get('time', '').strip()
        special = request.form.get('special_requests', '').strip()

        errors = []
        if not name:
            errors.append('Name is required.')
        if not phone:
            errors.append('Phone is required.')
        try:
            guests_int = int(guests)
            if guests_int <= 0:
                errors.append('Guests must be a positive number.')
        except ValueError:
            errors.append('Guests must be a number.')
        if not date or not time:
            errors.append('Date and time are required.')

        if errors:
            for e in errors:
                flash(e, 'error')
            return render_template('book_table.html', form=request.form)

        # Use date & time exactly as provided by HTML
        booking_dt_str = f"{date}  {time}"

        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO bookings (customer_name, phone, guests, booking_datetime, special_requests, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (name, phone, guests_int, booking_dt_str, special, booking_dt_str),
        )
        conn.commit()
        conn.close()
        flash('Your table has been booked! See you soon at YUMM.', 'success')
        return redirect(url_for('index'))

    return render_template('book_table.html', form={})


@app.route('/bookings')
def bookings():
    # Simple admin view (no auth for demo). In production, protect this route.
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM bookings ORDER BY booking_datetime DESC")
    rows = cur.fetchall()
    conn.close()
    return render_template('bookings.html', bookings=rows)


if __name__ == '__main__':
    # Ensure DB exists on first run
    init_db()
    app.run(host='127.0.0.1', port=5000, debug=True)
