#!/usr/bin/python3
# coding: utf-8

import sys
import psycopg2
from clint.textui import puts, colored, prompt


def display_query():
    puts(str(colored.white("""
    The three questions which the tool answers are as follows:\n""") + colored.cyan("""
      1. In order, what are the three most popular articles of all time?\n
      2. In order, who are the most popular article authors of all time?\n
      3. In order, on which days did more than 1% of requests lead to errors?\n""") + colored.white("""
    Please type in the number corresponding to the question you'd like
    answered, and press ENTER.""")))
    command = prompt.query(str(colored.green("""
    Enter a command:""", bold=True)))
    handle_user_input(command)


def handle_user_input(command):
    command = int(command) - 1
    most_popular_articles = """
    select
      title,
      count(*)
    from
      articles,
      log
    where
      path like ('%' || slug || '%')
    group by
      title
    order by
      count desc
    limit
      3;"""
    most_popular_authors = """
    select
      authors.name,
      count(*)
    from
      articles,
      authors,
      log
    where
      articles.author = authors.id
      and path like ('%' || slug || '%')
    group by
      authors.name
    order by
      count desc;"""
    days_with_error_rate_above_one = """
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
    select
      *
    from
      (
        select
          all_requests_by_date.date,
          failed_requests_by_date.count as failed_requests,
          all_requests_by_date.count as total_requests,
          round(
            (
              ((failed_requests_by_date.count) * 1.0)
              / (all_requests_by_date.count)
            ) * 100,
            4
          ) as percent_of_failed_requests
        from
          all_requests_by_date,
          failed_requests_by_date
        where
          all_requests_by_date.date = failed_requests_by_date.date
        order by
          percent_of_failed_requests desc
      ) as innerTable
    where
      percent_of_failed_requests > 1;"""
    query = [
        most_popular_articles,
        most_popular_authors,
        days_with_error_rate_above_one]
    if (command >= 0 and command < len(query)):
        print_report(execute_query(query[command]), command)
    else:
        puts(str(colored.green("""
            Please enter an acceptable command.""", bold=True)))
        display_query()


def print_report(results, command):
    index = "\n"
    for result in results:
        index += ("\n      " + result[0] + "\n")
    outputs = {
        0: "The most popular articles are in order as follows:",
        1: "The most popular authors are in order as follows:",
        2: "The days with more than 1% of requests " +
        "leading to errors are in order as follows:"}
    puts(str(colored.cyan("""\n\n    """ + (outputs.get(command))) +
             colored.green(index) + "\n"))
    display_query()


def execute_query(query):
    db = psycopg2.connect("dbname=news")
    cursor = db.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    db.commit()
    db.close()
    return results


try:
    puts(str(colored.green("""
    Logs Analysis Project\n""", bold=True) + colored.white("""
    This is a Python reporting tool that prints out reports —
    based on data in the database —
    using the psycopg2 module.""", bold=True)))
    display_query()
except KeyboardInterrupt:
    puts(str(colored.cyan("""\n
    Goodbye!\n""")))
    sys.exit()
