from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from student_operations import add_student, get_all_students, update_student, delete_student, search_students
import os

app = Flask(__name__, static_folder='.')
CORS(app)  # Cho phép cross-origin requests

# Route mặc định để phục vụ file index.html
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

# Route để phục vụ các file tĩnh (CSS, JS, hình ảnh)
@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

@app.route('/api/students', methods=['GET'])
def get_students():
    success, message, students = get_all_students()
    return jsonify({'success': success, 'message': message, 'data': students})

@app.route('/api/students', methods=['POST'])
def create_student():
    data = request.json
    success, message = add_student(
        data['fullName'],
        data['studentId'],
        data['birthDate'],
        data['hometown']
    )
    return jsonify({'success': success, 'message': message})

@app.route('/api/students/<int:student_id>', methods=['PUT'])
def update_student_info(student_id):
    data = request.json
    success, message = update_student(
        student_id,
        data['fullName'],
        data['studentId'],
        data['birthDate'],
        data['hometown']
    )
    return jsonify({'success': success, 'message': message})

@app.route('/api/students/<int:student_id>', methods=['DELETE'])
def delete_student_info(student_id):
    success, message = delete_student(student_id)
    return jsonify({'success': success, 'message': message})

@app.route('/api/students/search', methods=['GET'])
def search_students_api():
    search_term = request.args.get('term', '')
    success, message, students = search_students(search_term)
    return jsonify({'success': success, 'message': message, 'data': students})

if __name__ == '__main__':
    app.run(debug=True) 