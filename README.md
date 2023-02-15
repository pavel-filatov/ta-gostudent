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