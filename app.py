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
    tables = db.execute("SELECT * FROM tables")
    
    students_by_grade = {}
    tables_by_student = {}
    for grade in grades:
        students = db.execute("SELECT * FROM students WHERE grade_id = :grade_id", grade_id=grade['id'])
        students_by_grade[grade['id']]= students
        for student in students:
            tables_by_student[student['id']] = db.execute("SELECT * FROM tables WHERE guests_of = :student_id ", student_id = student['id'])
        
        print(tables_by_student)
        
    
    
    return render_template('event_template.html', event = event, grades = grades, tables = tables, students_by_grade = students_by_grade, tables_by_student = tables_by_student )


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
        db.execute(f"INSERT INTO students (grade_id, name, guests, vegetarians,  celiac,  delivered, charged)"
                    f" VALUES ({grade_id}, '', 0, 0, 0, 0, 0)")

    
    return redirect(url_for('show_event', event_id=event_id))


def save_cell_data(): 
	"""
	Function to uplotad data from cell
	"""
	
	# Get cell data
	cell_data = request.get_json()
	row_id = cell_data['rowId']
	column_index = cell_data['columnIndex']
	new_data = cell_data['newData']
	
	# Get grade id from student
	result = db.execute('SELECT grade_id FROM students WHERE id= :row_id' , row_id=row_id)
	result = result['0']
	grade_id = result['id']
	
	# Get column name
	column_name = get_column_name(column_index)
	
	# Save cell data
	if column_name != "tables":
	    db.execute('INSERT students SET :column_name = :new_data WHERE id = :row_id',
		column_name=column_name, new_data=new_data, row_id=row_id)
	
	# Logic to manage tables
	else:  
        manage_tables(row_id, new_data)


def get_column_name(column_index):
    switcher = {
        0: "name",
        1: "guests",
        3: "vegetarians",
        4: "celiac",
        5: "delivered",
        6: "charged",
        7: "tables"
    }
    return switcher.get(column_index, "Invalid column id")


def manage_tables(student_id, new_data):
    """
    Function to create and manage tables
    """

    # Get student tables
    old_table_numbers = get_student_tables(student_id)
    
    # Given a string of tables, returns a list with every table
    new_table_numbers = [int(num.strip()) for num in new_data.split(',')]

    to_delete, to_create, to_analize = compare_tables(new_table_numbers, old_table_numbers, student_id)

    # Tables to delete
    for table_number in to_delete:
        table_id = get_table_id(student_id, table)
        delete_table(table_id)
    
    # Tables to analize
    for table_number in to_create:

        # Store table ID
        table_id =  get_table_id(student_id, table)

        # Calculate guests to place
        result_guests = db.execute('SELECT guests, placed FROM students WHERE id = ?', (table_id))
        result_guests = result_guests[0]
        guests, placed = result_guests

        cant_guests = guests - placed
        # Create a table
        # Place student guests
        # Add the placed guests to the variable placed
        # Add the placed guests to the cant_guest_off variable

    # Tables to create  
    for table_number in to_analize:

        # Store table ID
        table_id =  get_table_id(student_id, table)

        # Calculate guests to place
        result_guests = db.execute('SELECT guests, placed FROM students WHERE id = ?', (table_id))
        result_guests = result_guests[0]
        guests, placed = result_guests

        cant_guests = guests - placed

        # Get the current and max guests for the table
        result = db.execute('SELECT cant_guest, max_guest FROM tables WHERE id = ?', (table_id,))
        result = result[0]
        if result:
            current_guests, max_guests = result
            if current_guests < max_guests:
                # Place student guests

            else:
                print("ERROR: Table is full.")


def compare_tables(new_list, old_list):
    """
    Compare the tables from the old and new lists
    Returns three lists. One to create new tables, one to delete tables, and other to analize later.
    """

    # Convert lists to sets for easier comparison
    new_set = set(new_list)
    old_set = set(old_list)
    
    # Find tables to delete and tables to analize
    to_delete = list(old_set - new_set)
    to_analize = list(new_set - old_set)
    to_create = list()

    # Find tables to create
    for table_number in to_analize:

        # Check if the table exists in the db
        table_id = get_table_id(student_id, table_number)

        # If table is not in the db then add to the create list
        if not table_id:
            to_create.append(table_number

    return to_delete, to_create, to_create


def get_table_id(student_id, number):
    """
    Given the student_id and the table number return the table_id
    """

    result = db.execute('SELECT table_id FROM students_tables WHERE student_id = :student_id AND table_number = :number',
                student_id=student_id, number=number)
    if result:
        return result[0] 
    else:
        return None


def get_student_tables(student_id):
    pass

def delete_table(table_id):
    pass

def add_table(table_id):
    pass

    

        
    




    






    


    
    
    
if __name__ == '__main__':
    app.run()
