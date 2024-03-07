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

@app.route('/event/<event_id>')
def show_event(event_id):
    # fetch data
    result = db.execute("SELECT * FROM events WHERE id = :event_id", event_id =event_id)
    event = result[0]
    grades = db.execute("SELECT * FROM grade WHERE event_id = :event_id ", event_id = event_id )
    
    students_by_grade = {}
    tables_by_student = {}
    for grade in grades:
        students = db.execute("SELECT * FROM students WHERE grade_id = :grade_id", grade_id=grade['id'])
        students_by_grade[grade['id']]= students
        for student in students:
            tables_by_student[student['id']] = db.execute("SELECT * FROM tables WHERE guests_of = :student_id ", student_id = student['id'])
        
        
    
    
    return render_template('event_template.html', event = event, grades = grades, students_by_grade = students_by_grade, tables_by_student = tables_by_student )

@app.route('/create_new_grade/<event_id>', methods=['POST'])
def create_new_grade(event_id):
    name = request.form['gradeName']
    size = int(request.form['gradeSize'])

    db.execute("INSERT INTO grade(event_id, name, size)"
                "VALUES (:event_id, :name, :size )",
                event_id = event_id, name = name, size = size)
    
    result = db.execute("SELECT last_insert_rowid() as id")
    result = result[0]
    grade_id = result['id']

    for i in range(size):
        db.execute("INSERT INTO students (grade_id) VALUES (:grade_id)",
                    grade_id=grade_id )
    
    return redirect(url_for('show_event', event_id=event_id))




    






    


    
    
    
if __name__ == '__main__':
    app.run()
