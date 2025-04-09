from db_config import create_connection
from mysql.connector import Error

def add_student(full_name, student_id, birth_date, hometown):
    connection = create_connection()
    if connection is None:
        return False, "Không thể kết nối đến database"
    
    try:
        cursor = connection.cursor()
        sql = """INSERT INTO students (fullName, studentId, birthDate, hometown) 
                 VALUES (%s, %s, %s, %s)"""
        values = (full_name, student_id, birth_date, hometown)
        cursor.execute(sql, values)
        connection.commit()
        return True, "Thêm sinh viên thành công"
    except Error as e:
        return False, f"Lỗi: {str(e)}"
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def get_all_students():
    connection = create_connection()
    if connection is None:
        return False, "Không thể kết nối đến database", []
    
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM students")
        students = cursor.fetchall()
        return True, "Lấy danh sách sinh viên thành công", students
    except Error as e:
        return False, f"Lỗi: {str(e)}", []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def update_student(student_id, full_name, student_code, birth_date, hometown):
    connection = create_connection()
    if connection is None:
        return False, "Không thể kết nối đến database"
    
    try:
        cursor = connection.cursor()
        sql = """UPDATE students 
                 SET fullName = %s, studentId = %s, birthDate = %s, hometown = %s 
                 WHERE id = %s"""
        values = (full_name, student_code, birth_date, hometown, student_id)
        cursor.execute(sql, values)
        connection.commit()
        return True, "Cập nhật thông tin sinh viên thành công"
    except Error as e:
        return False, f"Lỗi: {str(e)}"
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def delete_student(student_id):
    connection = create_connection()
    if connection is None:
        return False, "Không thể kết nối đến database"
    
    try:
        cursor = connection.cursor()
        sql = "DELETE FROM students WHERE id = %s"
        cursor.execute(sql, (student_id,))
        
        cursor.execute("ALTER TABLE students AUTO_INCREMENT = 1")
        
        connection.commit()
        return True, "Xóa sinh viên thành công"
    except Error as e:
        return False, f"Lỗi: {str(e)}"
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def search_students(search_term):
    connection = create_connection()
    if connection is None:
        return False, "Không thể kết nối đến database", []
    
    try:
        cursor = connection.cursor(dictionary=True)
        sql = """SELECT * FROM students 
                 WHERE fullName LIKE %s OR hometown LIKE %s"""
        search_pattern = f"%{search_term}%"
        cursor.execute(sql, (search_pattern, search_pattern))
        students = cursor.fetchall()
        return True, "Tìm kiếm thành công", students
    except Error as e:
        return False, f"Lỗi: {str(e)}", []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close() 