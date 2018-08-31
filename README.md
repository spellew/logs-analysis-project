# Logs Analysis Project

The task is to create a reporting tool that prints out reports (in plain text) based on the data in the database. This reporting tool is a Python program using the psycopg2 module to connect to the database.

## The Program's Design

The program is designed to loop. First, we introduce the user to the project, giving them an overview, before we ask them to select a report. This is inside of a `try` statement so if the user exits we can send them a `Goodbye!` message. After the user selects a query using the questions we displayed, we store their input and use it to call the `handle_user_input` function. Depending on the user's input we either use the corresponding query, or if there's no corresponding query, we ask them to enter an acceptable input. The corresponding query is then sent to our `execute_query` function, and is executed by `psycopg2`, which returns results. These results, from our database, are then formatted with the `print_report` function, and outputted to the user. The `display_query` function is then called, and we're back at square one.

## Running The Project

  0. Ensure that you have the latest version of Python installed. If not, please visit [python.org](https://python.org/) or refer to the `Installing Python` section of the [Hitchhiker’s Guide to Python](https://docs.python-guide.org/).

  1. Please install the following pip packages: `clint`, `psycopg2`, `psycopg2-binary`, using the `pip install` command.

  2. Run the project with `python catalog.py`.

## Created Views

  The following view gets the `log` table and selects the `time` column, and all of the data in the rows of this column are truncated and then converted to a new format — one where only the date of the request matters. These dates are then used to group the results, and we count up the amount of requests belonging to each grouping.
  ```
  create or replace view all_requests_by_date as
    select
      to_char(
        date_trunc('day', time),
        'Month DD, YYYY'
      ) as date,
      count(*)
    from
      log
    group by
      date;
  ```

  The following view gets the `log` table and selects the `time` column, and all of the data in the rows of this column are truncated and then converted to a new format — one where only the date of the request matters. These dates are then used to group the results, and we count up the amount of requests belonging to each grouping. Only the requests which fail, with a `status` not equal to `200 OK`, are counted.
  ```
    create or replace view failed_requests_by_date as
    select
      to_char(
        date_trunc('day', time),
        'Month DD, YYYY'
      ) as date,
      count(*)
    from
      log
    where
      status != '200 OK'
    group by
      date;
  ```