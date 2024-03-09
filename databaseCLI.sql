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

    PRIMARY KEY("id" AUTOINCREMENT),
    FOREIGN KEY("grade_id") REFERENCES "grade" ("id")
);

CREATE TABLE tables (
    number INTEGER,
    id INTEGER,
    cant_guest INTEGER,
    guests_of INTEGER,
    PRIMARY KEY("id" AUTOINCREMENT),
    FOREIGN KEY("guests_of") REFERENCES "students" ("id")
   
);

