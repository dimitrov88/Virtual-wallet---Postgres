import sys
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import connection, cursor
from psycopg2 import Error


def _get_connection() -> connection:
    try:
        return psycopg2.connect(
            user="admin",
            password="CkPmGvGLslvxb5Z9MiKQ6JQsWMvKGY8k",
            host='dpg-cmgj8ngcmk4c73er9s6g-a.frankfurt-postgres.render.com',
            port=5432,
            database="walletdb_78c5"
        )
    except Error as e:
        print(f"Error connecting to PostgreSQL: {e}")
        sys.exit(1)


def read_query(sql: str, sql_params=()) -> list:
    with _get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, sql_params)
            return list(cursor.fetchall())


def delete_query(sql: str, sql_params=()) -> None:
    with _get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, sql_params)
        conn.commit()


def update_query(sql: str, sql_params=()) -> bool:
    with _get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, sql_params)
        conn.commit()
    return True


def insert_query(sql: str, sql_params=()) -> int:
    with _get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, sql_params)
            conn.commit()
            return cursor.lastrowid


def insert_query1(sql: str, sql_params=()) -> int:
    with _get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql + ' RETURNING id', sql_params)
            conn.commit()
            return cursor.fetchone()[0]


def first_row_query(sql: str, sql_params=()):
    with _get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, sql_params)
            return cursor.fetchone()
