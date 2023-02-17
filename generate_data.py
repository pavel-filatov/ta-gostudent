import datetime
import random
import sqlite3
from pathlib import Path
from typing import List, Tuple

DATABASE = "gostudent.sqlite"
STARTUP_SCRIPT = Path("sql/00_setup_database.sql")


def main():
    """Generates data and fills a SQLite database with it."""
    run_sql_script(STARTUP_SCRIPT)
    subjects, students, tutors, lessons = generate_data()
    with sqlite3.connect(DATABASE) as con:
        con.executemany("INSERT INTO subjects(subject_name) VALUES (?)", subjects)
        con.executemany("INSERT INTO students(name, join_date, passport_details) VALUES (?, ?, ?)", students)
        con.executemany("INSERT INTO tutors(name, join_date, passport_details) VALUES (?, ?, ?)", tutors)
        con.executemany(
            "INSERT INTO lessons(start_dttm, end_dttm, subject_id, student_id, tutor_id) VALUES (?, ?, ?, ?, ?)",
            lessons,
        )


def run_sql_script(script_path: Path) -> None:
    """Executes SQL script against a SQLite database."""
    script = script_path.read_text()
    with sqlite3.connect(DATABASE) as con:
        con.executescript(script)


Subject = Tuple[str]
Person = Tuple[str, str, str]
Lesson = Tuple[str, str, int, int, int]


def generate_data() -> Tuple[List[Subject], List[Person], List[Person], List[Lesson]]:
    """Generates all 4 tables emulating the natural DB."""
    students_names = ["Peter", "Diana", "Alexandra", "Paul", "Josef", "Christine", "Matt", "Lucy"]
    tutors_names = ["Theofanis", "Ada", "Ailen", "Rosana", "Nicholas", "John", "Yasin", "Daniel", "Grant", "Ivan"]

    subjects = generate_subjects()
    students = generate_persons(students_names)
    tutors = generate_persons(tutors_names)
    lessons = generate_lessons(len(subjects), len(students), len(tutors))

    return subjects, students, tutors, lessons


def generate_subjects() -> List[Subject]:
    options = ["Chemistry", "Math", "Arts", "Biology", "History", "English", "German", "Computer Science"]

    num_options = random.randint(3, len(options))
    subjects = random.sample(options, k=num_options)

    return [(s,) for s in subjects]


def generate_persons(name_options: List[str]) -> List[Person]:
    num_records = random.randint(4, len(name_options))

    names = random.sample(name_options, k=num_records)
    join_dates = sorted([generate_datetime().date().isoformat() for _ in range(num_records)])
    passport_details = ["".join(random.sample("0123456789", k=7, counts=[10] * 10)) for _ in range(num_records)]

    return list(zip(names, join_dates, passport_details))


def generate_lessons(num_subjects: int, num_students: int, num_tutors: int) -> List[Lesson]:
    num_records = random.randint(100, 10000)
    start_times = sorted([generate_datetime() for _ in range(num_records)])
    time_deltas = [random.randint(10, 120) for _ in range(num_records)]

    return [
        (
            start_times[i].isoformat(),
            (start_times[i] + datetime.timedelta(minutes=time_deltas[i])).isoformat(),
            random.choice(range(1, num_subjects + 1)),
            random.choice(range(1, num_students + 1)),
            random.choice(range(1, num_tutors + 1)),
        )
        for i in range(num_records)
    ]


def generate_datetime() -> datetime.datetime:
    year = random.randint(2018, 2023)
    month = random.randint(1, 12)
    max_day = 28 if month == 2 else 30 if month in (4, 6, 9, 11) else 31
    day = random.randint(1, max_day)
    hour = random.randint(0, 23)
    minute = random.randint(0, 59)

    return datetime.datetime(year, month, day, hour, minute)


if __name__ == "__main__":
    main()
