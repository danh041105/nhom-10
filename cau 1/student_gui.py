import tkinter as tk
from tkinter import ttk, messagebox
from student_operations import add_student, get_all_students, update_student, delete_student, search_students
from db_config import create_database
import datetime

class StudentManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quản lý Sinh viên")
        self.root.geometry("800x600")
        
        # Tạo database và bảng
        create_database()
        
        # Biến để lưu trữ thông tin sinh viên đang được chỉnh sửa
        self.editing_student_id = None
        
        # Tạo các thành phần giao diện
        self.create_widgets()
        
        # Load dữ liệu ban đầu
        self.load_students()

    def create_widgets(self):
        # Frame cho form nhập liệu
        input_frame = ttk.LabelFrame(self.root, text="Thông tin sinh viên", padding="10")
        input_frame.pack(fill="x", padx=10, pady=5)

        # Các trường nhập liệu
        ttk.Label(input_frame, text="Họ và tên:").grid(row=0, column=0, sticky="w")
        self.full_name_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.full_name_var).grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(input_frame, text="Mã số sinh viên:").grid(row=1, column=0, sticky="w")
        self.student_id_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.student_id_var).grid(row=1, column=1, padx=5, pady=2)

        ttk.Label(input_frame, text="Ngày sinh:").grid(row=2, column=0, sticky="w")
        self.birth_date_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.birth_date_var).grid(row=2, column=1, padx=5, pady=2)

        ttk.Label(input_frame, text="Quê quán:").grid(row=3, column=0, sticky="w")
        self.hometown_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.hometown_var).grid(row=3, column=1, padx=5, pady=2)

        # Frame cho các nút
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=10)

        ttk.Button(button_frame, text="Thêm", command=self.add_student).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Cập nhật", command=self.update_student).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Hủy", command=self.cancel_edit).pack(side="left", padx=5)

        # Frame cho tìm kiếm
        search_frame = ttk.LabelFrame(self.root, text="Tìm kiếm", padding="10")
        search_frame.pack(fill="x", padx=10, pady=5)

        self.search_var = tk.StringVar()
        ttk.Entry(search_frame, textvariable=self.search_var).pack(side="left", padx=5)
        ttk.Button(search_frame, text="Tìm", command=self.search_students).pack(side="left", padx=5)

        # Treeview để hiển thị danh sách sinh viên
        self.tree = ttk.Treeview(self.root, columns=("ID", "Họ tên", "MSSV", "Ngày sinh", "Quê quán"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Họ tên", text="Họ tên")
        self.tree.heading("MSSV", text="MSSV")
        self.tree.heading("Ngày sinh", text="Ngày sinh")
        self.tree.heading("Quê quán", text="Quê quán")
        
        self.tree.column("ID", width=50)
        self.tree.column("Họ tên", width=200)
        self.tree.column("MSSV", width=100)
        self.tree.column("Ngày sinh", width=100)
        self.tree.column("Quê quán", width=200)
        
        self.tree.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Binding cho sự kiện chọn sinh viên
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        # Nút xóa
        ttk.Button(self.root, text="Xóa", command=self.delete_student).pack(pady=5)

    def load_students(self):
        # Xóa dữ liệu cũ trong treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Lấy danh sách sinh viên từ database
        success, message, students = get_all_students()
        if success:
            for student in students:
                self.tree.insert("", "end", values=(
                    student["id"],
                    student["fullName"],
                    student["studentId"],
                    student["birthDate"],
                    student["hometown"]
                ))
        else:
            messagebox.showerror("Lỗi", message)

    def add_student(self):
        # Lấy dữ liệu từ form
        full_name = self.full_name_var.get()
        student_id = self.student_id_var.get()
        birth_date = self.birth_date_var.get()
        hometown = self.hometown_var.get()

        # Kiểm tra dữ liệu
        if not all([full_name, student_id, birth_date, hometown]):
            messagebox.showerror("Lỗi", "Vui lòng điền đầy đủ thông tin!")
            return

        # Thêm sinh viên vào database
        success, message = add_student(full_name, student_id, birth_date, hometown)
        if success:
            messagebox.showinfo("Thành công", message)
            self.clear_form()
            self.load_students()
        else:
            messagebox.showerror("Lỗi", message)

    def update_student(self):
        if self.editing_student_id is None:
            messagebox.showerror("Lỗi", "Vui lòng chọn sinh viên cần cập nhật!")
            return

        # Lấy dữ liệu từ form
        full_name = self.full_name_var.get()
        student_id = self.student_id_var.get()
        birth_date = self.birth_date_var.get()
        hometown = self.hometown_var.get()

        # Kiểm tra dữ liệu
        if not all([full_name, student_id, birth_date, hometown]):
            messagebox.showerror("Lỗi", "Vui lòng điền đầy đủ thông tin!")
            return

        # Cập nhật thông tin sinh viên
        success, message = update_student(self.editing_student_id, full_name, student_id, birth_date, hometown)
        if success:
            messagebox.showinfo("Thành công", message)
            self.clear_form()
            self.load_students()
        else:
            messagebox.showerror("Lỗi", message)

    def delete_student(self):
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showerror("Lỗi", "Vui lòng chọn sinh viên cần xóa!")
            return

        if messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa sinh viên này?"):
            student_id = self.tree.item(selected_items[0])["values"][0]
            success, message = delete_student(student_id)
            if success:
                messagebox.showinfo("Thành công", message)
                self.clear_form()
                self.load_students()
            else:
                messagebox.showerror("Lỗi", message)

    def search_students(self):
        search_term = self.search_var.get()
        if not search_term:
            self.load_students()
            return

        # Xóa dữ liệu cũ trong treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Tìm kiếm sinh viên
        success, message, students = search_students(search_term)
        if success:
            for student in students:
                self.tree.insert("", "end", values=(
                    student["id"],
                    student["fullName"],
                    student["studentId"],
                    student["birthDate"],
                    student["hometown"]
                ))
        else:
            messagebox.showerror("Lỗi", message)

    def on_select(self, event):
        selected_items = self.tree.selection()
        if selected_items:
            values = self.tree.item(selected_items[0])["values"]
            self.editing_student_id = values[0]
            self.full_name_var.set(values[1])
            self.student_id_var.set(values[2])
            self.birth_date_var.set(values[3])
            self.hometown_var.set(values[4])

    def clear_form(self):
        self.editing_student_id = None
        self.full_name_var.set("")
        self.student_id_var.set("")
        self.birth_date_var.set("")
        self.hometown_var.set("")

    def cancel_edit(self):
        self.clear_form()
        self.tree.selection_remove(self.tree.selection())

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentManagementApp(root)
    root.mainloop() 