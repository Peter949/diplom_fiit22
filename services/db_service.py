from database.connection import get_connection, release_connection
import json

class DBService:
    def get_all_faqs(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("select * from faq")
        rows = cursor.fetchall()
        cursor.close()
        release_connection(conn)
        return rows



db_service = DBService()