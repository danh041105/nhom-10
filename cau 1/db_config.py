import mysql.connector
from mysql.connector import Error

def create_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="chip0411",
            database="student_management"
        )
        return connection
    except Error as e:
        print(f"Lỗi kết nối MySQL: {e}")
        return None

def create_database():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="chip0411"
        )
        cursor = connection.cursor()
        
        # Tạo database nếu chưa tồn tại
        cursor.execute("CREATE DATABASE IF NOT EXISTS student_management")
        cursor.execute("USE student_management")
        
        # Tạo bảng students nếu chưa tồn tại
        create_table_query = """
        CREATE TABLE IF NOT EXISTS students (
            id INT AUTO_INCREMENT PRIMARY KEY,
            fullName VARCHAR(255) NOT NULL,
            studentId VARCHAR(20) NOT NULL UNIQUE,
            birthDate DATE NOT NULL,
            hometown VARCHAR(255) NOT NULL
        )
        """
        cursor.execute(create_table_query)
        connection.commit()
        print("Database và bảng đã được tạo thành công!")
        
    except Error as e:
        print(f"Lỗi: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close() 