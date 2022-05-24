import pymysql

class Student:

    def __init__(self):
        # You may have to put code here.
        pass

    def get_by_id(self, ID):
        # Connect to DB.
        conn = pymysql.connect(host="localhost", user="root", password="dbuserdbuser",charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        # Form SQL
        sql = """
            select * from db_book.student where
                ID=%s
        """

        # Run query
        cur = conn.cursor()
        res = cur.execute(
            sql, args=(ID)
        )
        res = cur.fetchone()
        # return result
        return res

        # pass