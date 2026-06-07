# main.py
import json
from tkinter import *
from tkinter import messagebox, ttk
from sqlClient import mySqlClient
from datetime import datetime

# ---------- Load config ----------
with open('config.json', 'r') as f:
    config = json.load(f)

db = mySqlClient(
    username=config['user'],
    password=config['pass'],
    host=config['host'],
    database=config['database']
)

# ---------- Window setup ----------
window = Tk()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
win_width = int(screen_width * 0.7)
win_height = int(screen_height * 0.7)
window.geometry(f"{win_width}x{win_height}")
window.title("Employee Management System")
window.protocol("WM_DELETE_WINDOW", lambda: (db.close(), window.destroy()))

# ---------- Helper: validate date ----------
def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

# ---------- Home screen ----------
def home_screen():
    for w in window.winfo_children():
        w.destroy()
    frame = Frame(window)
    frame.place(relx=0.5, rely=0.5, anchor=CENTER)
    opts = LabelFrame(frame, text="Options")
    opts.pack(padx=20, pady=10)
    Button(opts, text="Add New Employee", command=add_screen, width=20, height=2).pack(pady=5)
    Button(opts, text="Delete An Employee", command=delete_screen, width=20, height=2).pack(pady=5)
    Button(opts, text="Update An Employee", command=update_screen, width=20, height=2).pack(pady=5)
    Button(opts, text="View All Employees", command=all_employees_screen, width=20, height=2).pack(pady=5)

# ---------- Add employee ----------
def add_screen():
    for w in window.winfo_children():
        w.destroy()
    frame = Frame(window)
    frame.place(relx=0.5, rely=0.5, anchor=CENTER)

    entry_frame = LabelFrame(frame, text="Add New Employee")
    entry_frame.grid(row=0, column=0, padx=20, pady=10)

    labels = ["First Name", "Last Name", "Birth Date (YYYY-MM-DD)",
              "Joining Date (YYYY-MM-DD)", "Salary", "Department"]
    entries = []
    for i, txt in enumerate(labels):
        Label(entry_frame, text=txt).grid(row=i*2, column=0, sticky="w", padx=5, pady=2)
        e = Entry(entry_frame, width=30)
        e.grid(row=i*2+1, column=0, padx=5, pady=5)
        entries.append(e)

    def save():
        fname = entries[0].get().strip()
        lname = entries[1].get().strip()
        dob = entries[2].get().strip()
        doj = entries[3].get().strip()
        salary = entries[4].get().strip()
        dept = entries[5].get().strip()

        if not (fname and lname and dob and doj and salary and dept):
            messagebox.showerror("Error", "All fields are required")
            return
        if not is_valid_date(dob):
            messagebox.showerror("Error", "Invalid Birth Date (YYYY-MM-DD)")
            return
        if not is_valid_date(doj):
            messagebox.showerror("Error", "Invalid Joining Date (YYYY-MM-DD)")
            return
        try:
            salary_val = float(salary)
            if salary_val < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Salary must be a positive number")
            return

        full_name = f"{fname.capitalize()} {lname.capitalize()}"
        try:
            db.insert_employee(full_name, dob, doj, salary_val, dept)
            messagebox.showinfo("Success", "Employee added successfully")
            home_screen()
        except Exception as e:
            messagebox.showerror("DB Error", str(e))

    Button(frame, text="Save Employee", command=save, width=20).grid(row=1, column=0, pady=10)
    Button(frame, text="Cancel", command=home_screen, width=20).grid(row=2, column=0)

# ---------- Delete employee (simplified: search then select) ----------
def delete_screen():
    for w in window.winfo_children():
        w.destroy()
    frame = Frame(window)
    frame.place(relx=0.5, rely=0.5, anchor=CENTER)

    search_frame = LabelFrame(frame, text="Delete Employee")
    search_frame.pack(padx=20, pady=10)

    Label(search_frame, text="Search by:").grid(row=0, column=0, padx=5)
    search_by = StringVar(value="Id")
    opts = ["Id", "Name", "Birth Date", "Joining Date", "Salary"]
    OptionMenu(search_frame, search_by, *opts).grid(row=0, column=1, padx=5)
    Label(search_frame, text="Value:").grid(row=1, column=0, padx=5)
    value_entry = Entry(search_frame, width=30)
    value_entry.grid(row=1, column=1, padx=5, pady=5)

    def do_search():
        method = search_by.get()
        val = value_entry.get().strip()
        if not val:
            messagebox.showerror("Error", "Please enter a search value")
            return
        try:
            results = db.find_employees(method, val)
            if not results:
                messagebox.showinfo("No results", "No employee found")
                return
            # Show results in a new window
            show_select_window(results, delete_mode=True)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    Button(search_frame, text="Search", command=do_search).grid(row=2, column=0, columnspan=2, pady=10)
    Button(frame, text="Back", command=home_screen).pack(pady=5)

def show_select_window(employees, delete_mode=False, update_mode=False):
    # employees: list of tuples (id, name, dob, joining, salary, dept)
    sel_win = Toplevel(window)
    sel_win.title("Select Employee")
    sel_win.geometry("700x400")
    tree = ttk.Treeview(sel_win, columns=("ID","Name","DOB","Joining","Salary","Dept"), show="headings")
    for col in ("ID","Name","DOB","Joining","Salary","Dept"):
        tree.heading(col, text=col)
        tree.column(col, width=100)
    scroll = ttk.Scrollbar(sel_win, orient=VERTICAL, command=tree.yview)
    tree.configure(yscrollcommand=scroll.set)
    tree.pack(side=LEFT, fill=BOTH, expand=True)
    scroll.pack(side=RIGHT, fill=Y)

    for emp in employees:
        tree.insert("", END, values=emp)

    def on_select():
        selected = tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select an employee")
            return
        emp_data = tree.item(selected[0])['values']
        emp_id = emp_data[0]
        if delete_mode:
            if messagebox.askyesno("Confirm Delete", f"Delete employee {emp_data[1]} (ID {emp_id})?"):
                try:
                    db.delete_employee("Id", str(emp_id))
                    messagebox.showinfo("Success", "Employee deleted")
                    sel_win.destroy()
                    home_screen()
                except Exception as e:
                    messagebox.showerror("Error", str(e))
        elif update_mode:
            sel_win.destroy()
            update_form(emp_id, emp_data)

    Button(sel_win, text="Select", command=on_select).pack(pady=10)

# ---------- Update employee ----------
def update_screen():
    for w in window.winfo_children():
        w.destroy()
    frame = Frame(window)
    frame.place(relx=0.5, rely=0.5, anchor=CENTER)

    search_frame = LabelFrame(frame, text="Update Employee")
    search_frame.pack(padx=20, pady=10)

    Label(search_frame, text="Search by:").grid(row=0, column=0, padx=5)
    search_by = StringVar(value="Id")
    opts = ["Id", "Name", "Birth Date", "Joining Date", "Salary"]
    OptionMenu(search_frame, search_by, *opts).grid(row=0, column=1, padx=5)
    Label(search_frame, text="Value:").grid(row=1, column=0, padx=5)
    value_entry = Entry(search_frame, width=30)
    value_entry.grid(row=1, column=1, padx=5, pady=5)

    def do_search():
        method = search_by.get()
        val = value_entry.get().strip()
        if not val:
            messagebox.showerror("Error", "Enter search value")
            return
        try:
            results = db.find_employees(method, val)
            if not results:
                messagebox.showinfo("No results", "No employee found")
                return
            show_select_window(results, delete_mode=False, update_mode=True)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    Button(search_frame, text="Search", command=do_search).grid(row=2, column=0, columnspan=2, pady=10)
    Button(frame, text="Back", command=home_screen).pack(pady=5)

def update_form(emp_id, emp_data):
    # emp_data: (id, name, dob, joining, salary, department)
    for w in window.winfo_children():
        w.destroy()
    frame = Frame(window)
    frame.place(relx=0.5, rely=0.5, anchor=CENTER)

    edit_frame = LabelFrame(frame, text="Edit Employee Details")
    edit_frame.grid(row=0, column=0, padx=20, pady=10)

    labels = ["First Name", "Last Name", "Birth Date (YYYY-MM-DD)",
              "Joining Date (YYYY-MM-DD)", "Salary", "Department"]
    entries = []
    # split full name into first/last
    name_parts = emp_data[1].split()
    first_name = name_parts[0] if len(name_parts) > 0 else ""
    last_name = name_parts[1] if len(name_parts) > 1 else ""

    default_vals = [first_name, last_name, emp_data[2], emp_data[3], emp_data[4], emp_data[5]]
    for i, txt in enumerate(labels):
        Label(edit_frame, text=txt).grid(row=i*2, column=0, sticky="w", padx=5, pady=2)
        e = Entry(edit_frame, width=30)
        e.grid(row=i*2+1, column=0, padx=5, pady=5)
        e.insert(0, str(default_vals[i]))
        entries.append(e)

    def save_update():
        fname = entries[0].get().strip()
        lname = entries[1].get().strip()
        dob = entries[2].get().strip()
        doj = entries[3].get().strip()
        salary = entries[4].get().strip()
        dept = entries[5].get().strip()
        if not (fname and lname and dob and doj and salary and dept):
            messagebox.showerror("Error", "All fields required")
            return
        if not is_valid_date(dob) or not is_valid_date(doj):
            messagebox.showerror("Error", "Invalid date format (YYYY-MM-DD)")
            return
        try:
            salary_val = float(salary)
        except ValueError:
            messagebox.showerror("Error", "Invalid salary")
            return
        full_name = f"{fname.capitalize()} {lname.capitalize()}"
        try:
            db.update_employee(emp_id, full_name, dob, doj, salary_val, dept)
            messagebox.showinfo("Success", "Employee updated")
            home_screen()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    Button(frame, text="Update", command=save_update, width=20).grid(row=1, column=0, pady=10)
    Button(frame, text="Cancel", command=home_screen, width=20).grid(row=2, column=0)

# ---------- View all employees ----------
def all_employees_screen():
    try:
        employees = db.get_all_employees()
        if not employees:
            messagebox.showinfo("Info", "No employees found")
            home_screen()
            return
        for w in window.winfo_children():
            w.destroy()
        frame = Frame(window)
        frame.pack(fill=BOTH, expand=True, padx=20, pady=20)

        tree_frame = Frame(frame)
        tree_frame.pack(fill=BOTH, expand=True)
        tree = ttk.Treeview(tree_frame, columns=("ID","Name","DOB","Joining","Salary","Dept"), show="headings")
        scroll_y = ttk.Scrollbar(tree_frame, orient=VERTICAL, command=tree.yview)
        scroll_x = ttk.Scrollbar(tree_frame, orient=HORIZONTAL, command=tree.xview)
        tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        for col in ("ID","Name","DOB","Joining","Salary","Dept"):
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor="center")

        for emp in employees:
            tree.insert("", END, values=emp)

        tree.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        Button(frame, text="Back", command=home_screen, width=15).pack(pady=10)
    except Exception as e:
        messagebox.showerror("Error", str(e))
        home_screen()

# ---------- Start ----------
home_screen()
window.mainloop()
