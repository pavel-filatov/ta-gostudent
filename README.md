# ta-gostudent

Technical Assignment for GoStudent

Check the description [here](./docs/assignment.md).

## Prerequisites

- sqlite3 command-line app
- Python 3.8+
- Poetry

## SQL Task

SQL scripts for the task live in [`sql` directory](./sql).

### Preparations

To create a database and fill it with generated data, execute:

```shell
# Plain Python
python3 generate_data.py

# Or, alternatively, with Poetry
poetry run generate
```

This app will create a database named `gostudent.sqlite` in the project's root.

### How to run

To execute the SQL scripts, we need a help from `sqlite3` command-line app.

There are the example commands:

```shell
# 1. Compute the most popular subjects
sqlite3 sql/gostudent.sqlite < sql/01_most_popular_lessons.sql

# 2. Compute the total time spent on lessons this year per month 
sqlite3 sql/gostudent.sqlite < sql/02_lessons_time_per_month_this_year.sql
```

### How to check the outputs

The SQL scripts are outputting their results under the [`output` dirctory](./output).

To check the results of the scripts execution, please run them and check the folder.

## Python Task

### Preparations

Running the app is supposed to happen inside the virtual environment.

For this project, Poetry dependency manager is used.
To activate it and create a virtual env, execute:

```shell
poetry install
```

### How to run

To run the app, call the following command:

```shell
poetry run gostudent <options>
```

Currently, there is a single entrypoint that computes total earnings for all tutors.
The options available are:

- `-i` - base directory of input files
- `-o` - base directory where to write the output data
- `-of` - output file format, one of `parquet`, `csv`, `json`

Example usages:

```shell
# Parquet is used by default
poetry run gostudent -i data/input -o data/output/salaries.parquet
```

### How to check the outputs

As soon as Parquet is not a human-readable format, we need something else to check how the
outputs are created.

The solution is storing data in CSV format.

```shell
poetry run gostudent -i data/input -o data/output/salaries.csv -of csv
```

In this case, you can go to the output location and check them manually, e.g.:

```shell
head data/output/salaries.csv/2021-08/2021-08-16.csv
```

### Run test

To run the tests, execute:

```shell
poetry run pytest
```