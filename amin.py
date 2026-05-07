from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SECRET_KEY'] = 'hotel_secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hotel.db'

db = SQLAlchemy(app)

# ================= MODELS =================

class Room(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    room_number = db.Column(
        db.String(50),
        nullable=False
    )

    room_type = db.Column(
        db.String(100),
        nullable=False
    )

    price = db.Column(
        db.Integer,
        nullable=False
    )

    available = db.Column(
        db.Boolean,
        default=True
    )

    bookings = db.relationship(
        'Booking',
        backref='room',
        lazy=True
    )

    def __repr__(self):
        return self.room_number

class Booking(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    customer_name = db.Column(
        db.String(200),
        nullable=False
    )

    days = db.Column(
        db.Integer,
        nullable=False
    )

    total_price = db.Column(
        db.Integer,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    room_id = db.Column(
        db.Integer,
        db.ForeignKey('room.id'),
        nullable=False
    )

# ================= ROUTES =================

@app.route('/')
def home():

    rooms = Room.query.all()

    return render_template(
        'rooms.html',
        rooms=rooms
    )

@app.route('/add-room', methods=['GET', 'POST'])
def add_room():

    if request.method == 'POST':

        room_number = request.form['room_number']
        room_type = request.form['room_type']
        price = request.form['price']

        room = Room(
            room_number=room_number,
            room_type=room_type,
            price=price
        )

        db.session.add(room)
        db.session.commit()

        return redirect('/')

    return render_template('add_room.html')

@app.route('/book/<int:id>', methods=['GET', 'POST'])
def book_room(id):

    room = Room.query.get_or_404(id)

    if request.method == 'POST':

        customer_name = request.form['customer_name']
        days = int(request.form['days'])

        total_price = days * room.price

        booking = Booking(
            customer_name=customer_name,
            days=days,
            total_price=total_price,
            room_id=room.id
        )

        room.available = False

        db.session.add(booking)
        db.session.commit()

        flash("Room Booked Successfully")

        return redirect('/')

    return render_template(
        'book_room.html',
        room=room
    )

@app.route('/delete-room/<int:id>')
def delete_room(id):

    room = Room.query.get_or_404(id)

    db.session.delete(room)
    db.session.commit()

    return redirect('/')

# ================= MAIN =================

if __name__ == '__main__':

    with app.app_context():
        db.create_all()

    app.run(debug=True)
