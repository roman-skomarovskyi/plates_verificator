import sqlite3
import datetime


class DateBaseHandler:
    # TODO: error handling
    def __init__(self):
        self.db_name = 'plates.db'
        self.conn = None
        self.cursor = None

    def create_connection(self):
        self.conn = sqlite3.connect("plates.db")
        self.cursor = self.conn.cursor()

    def close_connection(self):
        self.conn.close()

    def store_plate_info(self, plate, status):
        query = """INSERT INTO 'plates'
                    (plate_number, status, date)
                    VALUES (?, ?, ?);
                """

        data_tuple = (plate, status, datetime.datetime.now())
        self.cursor.execute(query, data_tuple)
        self.conn.commit()

    def select_all_results(self):
        """
        For testing purpose
        """
        self.cursor.execute("""SELECT * FROM plates""")
        rows = self.cursor.fetchall()
        self.conn.commit()
        return rows

    def clear_table(self):
        """
        For testing purpose
        """
        self.cursor.execute("""DELETE FROM plates""")
        self.conn.commit()
