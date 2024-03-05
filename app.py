import os

from cs50 import SQL
from datetime import datetime
from sqlalchemy import text
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, flash, redirect, json, jsonify, render_template, request, session, url_for, make_response
from flask_session import Session
from datetime import datetime, timedelta
from werkzeug.security import check_password_hash, generate_password_hash
from collections import namedtuple
from werkzeug.utils import secure_filename
from flask_mail import Mail, Message

import time


app = Flask(__name__)
app.secret_key = 'a1b2c3d4e5f6g7h8i9j0'


# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///manager.db")





@app.route('/')
def home():
    return redirect(url_for('events'))
    




@app.route("/events")
def events():
    """Show events"""

    # Check if there is a search query parameter in the URL
    query = request.args.get('query', '')

    # Fetch members data based on the search query or fetch all members if no query is provided
    if query:
        events = db.execute(
            "SELECT * FROM events WHERE name LIKE :query",
            query=f"%{query}%"
        )
    else:
        events = db.execute("SELECT * FROM events ")
    

    return render_template("events.html", events=events,  query=query)


@app.route("/create_new_event", methods=['POST'])
def create_new_event():
    # Get form data
    event_name = request.form['eventName']
    event_card_price = int(request.form['eventPrice'])
    event_date = request.form['datepicker']
    event_place = request.form['eventPlace']
    event_type = request.form['eventType']

    # Insertar datos del nuevo event en la base de datos
    db.execute("INSERT INTO events (name, date, place, type, card_price) "
               "VALUES (:event_name, :event_date, :event_place,  :event_type, :event_card_price)",
                event_name=event_name, event_date=event_date, event_place=event_place,
                event_type=event_type, event_card_price= event_card_price)

    # Redirigir al usuario a la página de índice
    return redirect(url_for('events'))





    


    
    
    
if __name__ == '__main__':
    app.run()
