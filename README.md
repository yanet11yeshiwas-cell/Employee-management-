# Employee-management-
Employee Management System
Developed by Yanet Yeshiwas
Overview

The Employee Management System is a desktop application developed using Python, Tkinter, and MySQL. The system provides an easy-to-use graphical interface for managing employee records efficiently. It allows organizations to store, update, view, and delete employee information through a centralized database system.

The application is designed to simplify employee data management while demonstrating the integration of Python GUI development with relational database management.

Technologies Used
Frontend
Python Tkinter
Backend
MySQL Database
Libraries
mysql-connector-python
Tkinter
Features
Add Employee

Add new employees to the database by entering their information through a user-friendly form.

Update Employee

Modify existing employee records and save changes directly to the database.

Delete Employee

Remove employee records securely from the database.

View Employees

Display all employee records in a structured format with a single click.

Database Integration

All employee data is stored and managed using MySQL, ensuring efficient data handling and persistence.

System Modules
Employee Registration
Employee ID
Full Name
Department
Position
Contact Information
Salary Details
Employee Management
Add records
Update records
Delete records
Search records
Database Operations
Create
Read
Update
Delete (CRUD)
Project Structure
Employee-Management-System/
│
├── main.py
├── config.json
├── requirements.txt
├── database/
│   └── employees.sql
├── assets/
└── README.md
Installation
Step 1: Clone the Repository
git clone https://github.com/OnkarSagare27/employee-management-mysql.git
Step 2: Navigate to the Project Directory
cd employee-management-mysql
Step 3: Install Required Dependencies
pip install -r requirements.txt
Database Configuration

Create or update the config.json file with your MySQL credentials.

{
    "pass": "DATABASE_PASSWORD",
    "user": "root",
    "host": "localhost",
    "database": "employees"
}

Ensure that:

MySQL Server is installed.
The database named employees exists.
The required tables have been created.
Running the Application

Execute the following command:

python main.py

The Employee Management System window will launch automatically.

Screenshots

Add screenshots of the application interface in this section.

Dashboard

Employee Records

Add Employee

Learning Outcomes

This project demonstrates practical experience in:

Python Programming
Tkinter GUI Development
MySQL Database Management
CRUD Operations
Database Connectivity
Desktop Application Development
Future Enhancements
Employee Search Functionality
Attendance Management
Payroll Management
Role-Based Authentication
Report Generation
Export Data to Excel/PDF
License

This project is intended for educational and learning purposes.

Author

Yanet Yeshiwas

Interested in Software Development, Database Systems, and Information Management Solutions.
