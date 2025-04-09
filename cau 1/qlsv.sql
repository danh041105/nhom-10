CREATE DATABASE student_management;
CREATE TABLE IF NOT EXISTS student_management.students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fullName VARCHAR(255) NOT NULL,
    studentId VARCHAR(20) NOT NULL UNIQUE,
    birthDate DATE NOT NULL,
    hometown VARCHAR(255) NOT NULL
)

SELECT * FROM student_management.students;