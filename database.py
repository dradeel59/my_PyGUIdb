import sqlite3
from PySide6.QtWidgets import *

class Widget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sqlite Database")
        self.setGeometry(100, 100, 500, 100)

        # Create QLabels - properties of each employee

        name_label = QLabel("Name")
        profession_label = QLabel("Profession")
        address_label = QLabel("Address")
        age_label = QLabel("Age")


        # Adding buttons to update/add
        button_add_data = QPushButton("Add New row")
        button_add_data.clicked.connect(self.add_data) # when the button is clicked it calls the add data function

        button_update_data = QPushButton("Update selected row")
        button_update_data.clicked.connect(self.update_data)




        # Create QLine Edits (where users can actually input the data into the labels)
        self.name_line_edit = QLineEdit()
        self.profession_line_edit = QLineEdit()
        self.address_line_edit = QLineEdit()
        self.age_line_edit = QLineEdit()

        # Name Lining up the QLine Edits and the QLabels - Form horizontal layout
        h_layout1 = QHBoxLayout()
        h_layout1.addWidget(name_label)
        h_layout1.addWidget(self.name_line_edit)

        # Profession Lining up the QLine Edits and the QLabels - Form horizontal layout
        h_layout2 = QHBoxLayout()
        h_layout2.addWidget(profession_label)
        h_layout2.addWidget(self.profession_line_edit)

        # Address Lining up the QLine Edits and the QLabels - Form horizontal layout
        h_layout3 = QHBoxLayout()
        h_layout3.addWidget(address_label)
        h_layout3.addWidget(self.address_line_edit)

        # Age Lining up the QLine Edits and the QLabels - Form horizontal layout
        h_layout4 = QHBoxLayout()
        h_layout4.addWidget(age_label)
        h_layout4.addWidget(self.age_line_edit)

        # button horizontal layout
        h_layout5 = QHBoxLayout()
        h_layout5.addWidget(button_add_data)
        h_layout5.addWidget(button_update_data)

        #grouping labls, buttons, and textboxes
        add_form = QGroupBox("Add New Employee")
    
        # displaying all items vertically in the group
        form_layout = QVBoxLayout()
        form_layout.addLayout(h_layout1)
        form_layout.addLayout(h_layout2)
        form_layout.addLayout(h_layout3)
        form_layout.addLayout(h_layout4)
        form_layout.addLayout(h_layout5)
        add_form.setLayout(form_layout)

        # create table
        self.table = QTableWidget(self)
        self.table.setMaximumWidth(800)

        self.table.setColumnCount(4)
        self.table.setColumnWidth(0, 150)
        self.table.setColumnWidth(1, 150)
        self.table.setColumnWidth(2, 150)
        self.table.setColumnWidth(3, 50)

        self.table.setHorizontalHeaderLabels(["Name", "Profession", "Address", "Age"])

        #creating more buttons
        button_insert_data = QPushButton("Insert Demo Data")
        button_insert_data.clicked.connect(self.insert_data)

        button_load_data = QPushButton("Load Data")
        button_load_data.clicked.connect(self.load_data)

        button_call_data = QPushButton("Extract Data")
        button_call_data.clicked.connect(self.call_data)

        button_delete_data = QPushButton("Delete Data")
        button_delete_data.clicked.connect(self.delete_data)

        #displaying all elements vertically
        layout = QVBoxLayout()
        layout.addWidget(add_form)
        layout.addWidget(self.table)
        layout.addWidget(button_insert_data)
        layout.addWidget(button_load_data)
        layout.addWidget(button_call_data)
        layout.addWidget(button_delete_data)
        self.setLayout(layout)

    def create_connection(self):
        # Create Sqlite database connection
        self.connection = sqlite3.connect("employees.db")

        return self.connection
    
    def insert_data(self):
        self.cursor = self.create_connection().cursor()

        self.cursor.execute("create table employees_list (Name text, Profession text, Address text, Age integer)")

        #listing employee data in tuples
        self.List_of_employees = [
            ("Faheem Ahmed", "Ice Cream Server", "Ashburn", 17),
            ("Tanzeela Ahmed", "Curie Learning", "Leesburg", 12),
            ("Durresameen Prapulla", "Chef", "Maryland", 20),
            ("Kaleem Ahmed", "Software Engineer", "new Jersey", 25)
        ]

        #inserting multiple rows
        self.cursor.executemany("Insert into employees_list values (?,?,?,?)", self.List_of_employees)
        
        self.connection.commit()
        self.connection.close()


    def add_data(self):
        self.cursor = self.create_connection().cursor()

        # get informaotin from text box
        self.new_employee = [
            self.name_line_edit.text(),
            self.profession_line_edit.text(),
            self.address_line_edit.text(),
            self.age_line_edit.text(),
        ]
    
        print("Name added:", self.name_line_edit.text())

        #adding info to table

        self.cursor.execute("Insert into employees_list values (?,?,?,?)", self.new_employee)

        # clear text box afterwarsd
        self.name_line_edit.clear()
        self.profession_line_edit.clear()
        self.address_line_edit.clear()
        self.age_line_edit.clear()

        self.connection.commit()
        self.connection.close()


    def load_data(self):

        print("execute")
        self.cursor = self.create_connection().cursor()
        rowCount_sqlquery = "SELECT COUNT (*) FROM employees_list"
        employees_sqlquery = "SELECT * FROM employees_list"

        # getting row count
        self.cursor.execute(rowCount_sqlquery)
        results = self.cursor.fetchone()

        print("Rows", results[0])
        self.table.setRowCount(results[0])

        # putting data into gui

        table_row = 0

        for i in self.cursor.execute(employees_sqlquery):
            self.table.setItem(table_row, 0, QTableWidgetItem(i[0]))
            self.table.setItem(table_row, 1, QTableWidgetItem(i[1]))
            self.table.setItem(table_row, 2, QTableWidgetItem(i[2]))
            self.table.setItem(table_row, 3, QTableWidgetItem(str(i[3])))
            table_row = table_row + 1


    def call_data(self):
        current_row_index = self.table.currentRow()

        # making each employee detail a variable

        self.name_edit = str(self.table.item(current_row_index, 0).text())
        self.profession_edit = str(self.table.item(current_row_index, 1).text())
        self.address_edit = str(self.table.item(current_row_index, 2).text())
        self.age_edit = str(self.table.item(current_row_index, 3).text())

        # changing the text box so that it shows the variables

        self.name_line_edit.setText(self.name_edit)
        self.profession_line_edit.setText(self.profession_edit)
        self.address_line_edit.setText(self.address_edit)
        self.age_line_edit.setText(self.age_edit)

    def update_data(self):
        self.cursor = self.create_connection().cursor()

        # get current data in the text boxes
        params = [
            self.name_line_edit.text(),
            self.profession_line_edit.text(),
            self.address_line_edit.text(),
            self.age_line_edit.text(),
            self.name_edit
        ]

        #updating list

        self.cursor.execute("UPDATE employees_list SET Name=?, Profession=?, Address=?, Age=? WHERE Name=?", params)

        print("The old name was:", self.name_edit)
        print("Thew new name is:", self.name_line_edit.text())

        # clear text boxes
        self.name_line_edit.clear()
        self.profession_line_edit.clear()
        self.address_line_edit.clear()
        self.age_line_edit.clear()

        self.connection.commit()
        self.connection.close()


    def delete_data(self):
        self.cursor = self.create_connection().cursor()
        current_row_index = self.table.currentRow()

        # making name a variable
        name_item = str(self.table.item(current_row_index, 0).text())

        # putting a warning so that if nothing is selected
        if current_row_index < 0:
            Warning = QMessageBox.warning(self, "Warning", "Please select a box")
        else:
            Message = QMessageBox.question(self, "Confirmation", "Are you sure you want to delete this row?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if Message == QMessageBox.StandardButton.Yes:
            sqlquery = "DELETE FROM employees_list WHERE Name=?"
            self.cursor.execute(sqlquery, (name_item,))

            print("You deleted:", name_item)

        self.connection.commit()
        self.connection.close()
