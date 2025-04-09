// Mảng lưu trữ thông tin sinh viên
let students = [];
let isEditing = false;

// Lấy các phần tử DOM
const studentForm = document.getElementById('studentForm');
const studentList = document.getElementById('studentList');
const concatenatedString = document.getElementById('concatenatedString');
const separatedArrays = document.getElementById('separatedArrays');
const sortedNumbers = document.getElementById('sortedNumbers');
const submitBtn = document.getElementById('submitBtn');
const cancelBtn = document.getElementById('cancelBtn');

// Load dữ liệu khi trang web được tải
document.addEventListener('DOMContentLoaded', function() {
    loadStudents();
});

// Hàm load dữ liệu từ server
function loadStudents() {
    fetch('/api/students', {
        method: 'GET'
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            students = data.data;
            displayStudents();
            processArrays();
        } else {
            alert('Lỗi khi tải dữ liệu: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Có lỗi xảy ra khi tải dữ liệu');
    });
}

// Xử lý sự kiện submit form
studentForm.addEventListener('submit', function (e) {
    e.preventDefault();

    // Lấy giá trị từ form
    const fullName = document.getElementById('fullName').value;
    const studentCode = document.getElementById('studentCode').value;
    const birthDate = document.getElementById('birthDate').value;
    const hometown = document.getElementById('hometown').value;
    const studentId = document.getElementById('studentId').value;

    // Kiểm tra tính hợp lệ của dữ liệu
    if (!isValidName(fullName) || !isValidStudentId(studentCode)) {
        alert('Vui lòng kiểm tra lại thông tin nhập vào!');
        return;
    }

    const studentData = {
        fullName: fullName,
        studentId: studentCode,
        birthDate: birthDate,
        hometown: hometown
    };

    if (isEditing) {
        // Cập nhật sinh viên
        fetch(`/api/students/${studentId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(studentData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(data.message);
                loadStudents();
                resetForm();
            } else {
                alert('Lỗi: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Có lỗi xảy ra');
        });
    } else {
        // Thêm sinh viên mới
        fetch('/api/students', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(studentData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(data.message);
                loadStudents();
                resetForm();
            } else {
                alert('Lỗi: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Có lỗi xảy ra');
        });
    }
});

// Hàm sửa thông tin sinh viên
function editStudent(id) {
    const student = students.find(s => s.id === id);
    if (student) {
        document.getElementById('studentId').value = student.id;
        document.getElementById('fullName').value = student.fullName;
        document.getElementById('studentCode').value = student.studentId;
        document.getElementById('birthDate').value = student.birthDate;
        document.getElementById('hometown').value = student.hometown;
        
        isEditing = true;
        submitBtn.textContent = 'Cập nhật';
        cancelBtn.style.display = 'inline-block';
    }
}

// Hàm xóa sinh viên
function deleteStudent(id) {
    if (confirm('Bạn có chắc chắn muốn xóa sinh viên này?')) {
        fetch(`/api/students/${id}`, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(data.message);
                loadStudents();
            } else {
                alert('Lỗi: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Có lỗi xảy ra');
        });
    }
}

// Hàm reset form
function resetForm() {
    studentForm.reset();
    document.getElementById('studentId').value = '';
    isEditing = false;
    submitBtn.textContent = 'Thêm Sinh viên';
    cancelBtn.style.display = 'none';
}

// Xử lý sự kiện nút Hủy
cancelBtn.addEventListener('click', resetForm);

// Hàm kiểm tra tên hợp lệ (chỉ chứa chữ cái và khoảng trắng)
function isValidName(name) {
    return /^[A-Za-zÀ-ỹ\s]+$/.test(name);
}

// Hàm kiểm tra mã số sinh viên hợp lệ (chỉ chứa số và chữ)
function isValidStudentId(id) {
    return /^[A-Za-z0-9]+$/.test(id);
}

// Hàm hiển thị danh sách sinh viên
function displayStudents() {
    studentList.innerHTML = '';
    students.forEach((student, index) => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${student.fullName}</td>
            <td>${student.studentId}</td>
            <td>${formatDate(student.birthDate)}</td>
            <td>${student.hometown}</td>
            <td>
                <button onclick="editStudent(${student.id})" class="edit-btn">Sửa</button>
                <button onclick="deleteStudent(${student.id})" class="delete-btn">Xóa</button>
            </td>
        `;
        studentList.appendChild(row);
    });
}

// Hàm xử lý các yêu cầu về mảng
function processArrays() {
    if (students.length === 0) {
        concatenatedString.innerHTML = '<strong>Chuỗi ghép:</strong> ';
        separatedArrays.innerHTML = '<strong>Mảng ký tự:</strong> []<br><strong>Mảng số:</strong> []';
        sortedNumbers.innerHTML = '<strong>Mảng số đã sắp xếp:</strong> []';
        return;
    }

    // Ghép MSSV và ngày sinh của tất cả sinh viên
    let concatenated = students.reduce((acc, student) => {
        // Lấy ngày sinh và format lại
        const date = new Date(student.birthDate);
        const day = date.getDate().toString().padStart(2, '0');
        const month = (date.getMonth() + 1).toString().padStart(2, '0');
        const year = date.getFullYear();
        const formattedDate = `${day}${month}${year}`;
        
        return acc + student.studentId + formattedDate;
    }, '');

    // Tách thành mảng số và ký tự
    const numbers = [];
    const chars = [];
    
    // Xử lý từng ký tự trong chuỗi ghép
    for (let i = 0; i < concatenated.length; i++) {
        const char = concatenated[i];
        if (/[0-9]/.test(char)) {
            numbers.push(parseInt(char));
        } else if (/[A-Za-z]/.test(char)) {
            chars.push(char);
        }
    }

    // Sắp xếp mảng số theo thứ tự giảm dần
    const sortedNums = [...numbers].sort((a, b) => b - a);

    // Hiển thị kết quả
    concatenatedString.innerHTML = `<strong>Chuỗi ghép:</strong> ${concatenated}`;
    separatedArrays.innerHTML = `
        <strong>Mảng ký tự:</strong> [${chars.join(', ')}]<br>
        <strong>Mảng số:</strong> [${numbers.join(', ')}]
    `;
    sortedNumbers.innerHTML = `<strong>Mảng số đã sắp xếp:</strong> [${sortedNums.join(', ')}]`;
}

// Hàm tìm kiếm sinh viên
function searchStudents() {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    if (!searchTerm) {
        loadStudents();
        return;
    }

    fetch(`/api/students/search?term=${searchTerm}`, {
        method: 'GET'
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            students = data.data;
            displayStudents();
            processArrays();
        } else {
            alert('Lỗi: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Có lỗi xảy ra');
    });
}

// Hàm format ngày tháng
function formatDate(dateString) {
    const date = new Date(dateString);
    const day = date.getDate().toString().padStart(2, '0');
    const month = (date.getMonth() + 1).toString().padStart(2, '0');
    const year = date.getFullYear();
    return `${day}/${month}/${year}`;
} 