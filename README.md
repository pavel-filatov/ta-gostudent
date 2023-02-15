# ta-gostudent

Technical Assignment for GoStudent

Check the description [here](./docs/assignment.md).

## How to run

Running the app is supposed to happen inside the virtual environment.

For this project, Poetry dependency manager is used.
To activate it and create a virtual env, execute:

```shell
poetry install
```

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

# Store as csv to look at the data
poetry run gostudent -i data/input -o data/output/salaries.csv
```
