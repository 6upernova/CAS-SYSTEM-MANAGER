CREATE TABLE events (
    id INTEGER,
    name TEXT,
    date TIMESTAMP,
    place TEXT,
    type TEXT,
    card_price FLOAT,
    PRIMARY KEY("id" AUTOINCREMENT)

);

CREATE TABLE grade (
    id INTEGER ,
    event_id INTEGER,
    name TEXT,
    size INTEGER,
    PRIMARY KEY("id" AUTOINCREMENT),
    FOREIGN KEY("event_id") REFERENCES "events"("id")
);

CREATE TABLE students (
    id INTEGER,
    grade_id INTEGER,
    name TEXT,
    guests INTEGER,
    vegetarians INTEGER,
    celiac INTEGER,
    delivered INTEGER,
    charged INTEGER,
<<<<<<< HEAD
    placed INTEGER
=======
    placed INTEGER,
>>>>>>> c11873b908a8c857335e37125582c8c37739c272

    PRIMARY KEY("id" AUTOINCREMENT),
    FOREIGN KEY("grade_id") REFERENCES "grade" ("id")
);

CREATE TABLE tables (
    number INTEGER,
    id INTEGER,
    cant_guest INTEGER,
    max_guest INTEGER,
    PRIMARY KEY("id" AUTOINCREMENT),
   
);

CREATE TABLE students_tables (
    id INTEGER,
    student_id INTEGER,
    table_id INTEGER,
    table_number INTEGER,
    cant_guest_of INTEGER,

    PRIMARY KEY("id" AUTOINCREMENT),
    FOREIGN KEY("student_id") REFERENCES "students" ("id"),
    FOREIGN KEY("table_id") REFERENCES "tables" ("id")
);

