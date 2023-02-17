DROP TABLE IF EXISTS students;
DROP TABLE IF EXISTS tutors;
DROP TABLE IF EXISTS subjects;
DROP TABLE IF EXISTS lessons;

CREATE TABLE subjects(subject_id INTEGER PRIMARY KEY, subject_name TEXT);
CREATE TABLE students(id INTEGER PRIMARY KEY, name TEXT, join_date DATE, passport_details TEXT);
CREATE TABLE tutors(id INTEGER PRIMARY KEY, name TEXT, join_date DATE, passport_details TEXT);
CREATE TABLE lessons(
  id INTEGER PRIMARY KEY, start_dttm TIMESTAMP, end_dttm TIMESTAMP, subject_id INTEGER, student_id INTEGER, tutor_id INTEGER
);
