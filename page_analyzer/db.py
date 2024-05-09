from psycopg2 import connect
from psycopg2.extras import NamedTupleCursor
import os
from dotenv import load_dotenv
from datetime import datetime



load_dotenv()


DATABASE_PASSWORD = os.getenv('PASSWORD')


class DatabaseConnection:
    def __enter__(self):
        self.connection = connect(
                              host='dpg-cougrrud3nmc73adm41g-a',
                              port=5432,
                              user='dbname_r03l_user',
                              password=DATABASE_PASSWORD,
                              dbname='dbname_r03l'
                          )
        self.cursor = self.connection.cursor(cursor_factory=NamedTupleCursor)
        return self.cursor

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            print(f"Возникло исключение типа: {exc_type}, "
                  f"со значением: {exc_value}")
        self.cursor.close()
        self.connection.commit()
        self.connection.close()

    def add_url_into_db(url):
        with DatabaseConnection() as cursor:
            query = (
                'INSERT INTO url '
                '(name, created_at) '
                'VALUES (%s, %s) '
                'RETURNING id'
            )
            values = (url, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            cursor.execute(query, values)
            return cursor.fetchone().id

    def get_url_by_name(url):
        with DatabaseConnection() as cursor:
            query = 'SELECT * FROM url WHERE name = (%s)'
            cursor.execute(query, (url,))
            data = cursor.fetchone()
            return data

    def get_url_by_id(id):
        with DatabaseConnection() as cursor:
            query = 'SELECT * FROM url WHERE id = (%s)'
            cursor.execute(query, (id,))
            data = cursor.fetchone()
            return data

    def add_url_check(check_data):
        with DatabaseConnection() as cursor:
            query = (
                'INSERT INTO url_checks '
                '(url_id, status_code, h1, title, description, created_at) '
                'VALUES (%s, %s, %s, %s, %s, %s)'
            )
            values = (
                check_data.get('url_id'),
                check_data.get('status_code'),
                check_data.get('h1', ''),
                check_data.get('title', ''),
                check_data.get('description', ''),
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            )
            cursor.execute(query, values)

    def get_checks_by_url_id(id):
        with DatabaseConnection() as cursor:
            query = (
                'SELECT * FROM url_checks WHERE url_id=(%s)'
                'ORDER BY id DESC'
            )
            cursor.execute(query, (id,))
            checks = cursor.fetchall()
            return checks

    def get_all_urls():
        with DatabaseConnection() as cursor:
            query = (
                'SELECT '
                'url.id AS id '
                'url.name AS name, '
                'url_checks.created_at AS las_check, '
                'status_code '
                'FROM url '
                'LEFT JOIN url_checks '
                'ON url.id = url_checks.url_id '
                'AND url_checks.id = ('
                'SELECT max(id) FROM url_checks'
                'WHERE url.id = url_checks.url_id '
                'ORDER BY url.id DESC;'
            )
            cursor.execute(query)
            urls = cursor.fetchall()
            return urls
