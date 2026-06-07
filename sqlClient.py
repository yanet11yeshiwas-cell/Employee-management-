# sqlClient.py
import mysql.connector
from mysql.connector import Error

class mySqlClient:
    def __init__(self, username: str, password: str, host: str, database: str):
        self.host = host
        self.username = username
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None
        self.connect()
        self.create_database()
        self.use_database()
        self.init_table()

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.username,
                password=self.password
            )
            self.cursor = self.connection.cursor()
        except Error as e:
            raise Exception(f"Database connection failed: {e}")

    def create_database(self):
        try:
            self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
            self.connection.commit()
        except Error as e:
            raise Exception(f"Failed to create database: {e}")

    def use_database(self):
        try:
            self.cursor.execute(f"USE {self.database}")
        except Error as e:
            raise Exception(f"Failed to select database: {e}")

    def init_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS employeedetails (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            dateOfBirth DATE,
            joiningDate DATE,
            salary DECIMAL(10,2),
            department VARCHAR(255)
        )
        """
        try:
            self.cursor.execute(query)
            self.connection.commit()
        except Error as e:
            raise Exception(f"Failed to create table: {e}")

    def insert_employee(self, name: str, dob: str, joining: str, salary: float, department: str):
        query = """
        INSERT INTO employeedetails (name, dateOfBirth, joiningDate, salary, department)
        VALUES (%s, %s, %s, %s, %s)
        """
        try:
            self.cursor.execute(query, (name, dob, joining, salary, department))
            self.connection.commit()
            return self.cursor.lastrowid
        except Error as e:
            raise Exception(f"Insert failed: {e}")

    def find_employees(self, method: str, value: str):
        """method: 'Id', 'Name', 'Birth Date', 'Joining Date', 'Salary'"""
        col_map = {
            'Id': 'id',
            'Name': 'name',
            'Birth Date': 'dateOfBirth',
            'Joining Date': 'joiningDate',
            'Salary': 'salary'
        }
        if method not in col_map:
            raise ValueError("Invalid search method")
        column = col_map[method]
        # For text columns, use LIKE; for exact matches (ID, Salary) use =
        if column in ('id', 'salary'):
            query = f"SELECT * FROM employeedetails WHERE {column} = %s"
            params = (value,)
        else:
            query = f"SELECT * FROM employeedetails WHERE {column} LIKE %s"
            params = (f"%{value}%",)
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except Error as e:
            raise Exception(f"Search failed: {e}")

    def delete_employee(self, method: str, value: str):
        """Delete by Id or Name or other column (exact match)"""
        col_map = {
            'Id': 'id',
            'Name': 'name',
            'Birth Date': 'dateOfBirth',
            'Joining Date': 'joiningDate',
            'Salary': 'salary'
        }
        if method not in col_map:
            raise ValueError("Invalid delete method")
        query = f"DELETE FROM employeedetails WHERE {col_map[method]} = %s"
        try:
            self.cursor.execute(query, (value,))
            self.connection.commit()
            return self.cursor.rowcount
        except Error as e:
            raise Exception(f"Delete failed: {e}")

    def update_employee(self, emp_id: int, name: str, dob: str, joining: str, salary: float, department: str):
        query = """
        UPDATE employeedetails
        SET name = %s, dateOfBirth = %s, joiningDate = %s, salary = %s, department = %s
        WHERE id = %s
        """
        try:
            self.cursor.execute(query, (name, dob, joining, salary, department, emp_id))
            self.connection.commit()
            return self.cursor.rowcount
        except Error as e:
            raise Exception(f"Update failed: {e}")

    def get_all_employees(self):
        try:
            self.cursor.execute("SELECT * FROM employeedetails")
            return self.cursor.fetchall()
        except Error as e:
            raise Exception(f"Fetch all failed: {e}")

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
