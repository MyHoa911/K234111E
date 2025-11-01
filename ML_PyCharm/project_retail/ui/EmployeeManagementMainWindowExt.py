from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QTableWidgetItem, QMessageBox

from project_retail.connector.employee_connector import EmployeeConnector
from project_retail.model.employee import Employee
from project_retail.ui.EmployeeManagementMainWindow import Ui_MainWindow


class EmployeeManagementMainWindowExt(Ui_MainWindow):
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow) #luu tru , khong thu hoi o nho o dong lenh so 8
        self.MainWindow=MainWindow  #dong setup phai de cuoi cung de no dua du lieu len thanh ram
        self.setupSignalAndSlot()
        self.is_Completed = False

        self.ec = EmployeeConnector()
        self.ec.connect()
        self.display_all_employees()

    def showWindow(self):
        self.MainWindow.show()
    def closeWindow(self):
        self.MainWindow.close()
    def setupSignalAndSlot(self):
        self.tableWidgetEmployee.itemSelectionChanged.connect(self.show_detail)
        self.pushButtonNew.clicked.connect(self.clear_data)
        self.pushButtonInsert.clicked.connect(self.insert_data)
        self.pushButtonUpdate.clicked.connect(self.update_data)
        self.pushButtonDelete.clicked.connect(self.delete_data)

    def display_all_employees(self):
        #empty existing data:
        self.tableWidgetEmployee.setRowCount(0)
        #loop all employee, then show up into table:
        employees = self.ec.get_list_employee()
        for emp in employees:
            #get lasted row:
            row=self.tableWidgetEmployee.rowCount()
            #insert new row at the end of table
            self.tableWidgetEmployee.insertRow(row)
            #assign (gán) value for columm:
            column_id=QTableWidgetItem(str(emp.ID))
            column_name=QTableWidgetItem(str(emp.Name))
            column_email=QTableWidgetItem(str(emp.Email))
            column_phone=QTableWidgetItem(str(emp.Phone))
            if emp.IsDeleted==1:
                column_id.setBackground(Qt.GlobalColor.yellow)
                column_name.setBackground(Qt.GlobalColor.yellow)
                column_email.setBackground(Qt.GlobalColor.yellow)
                column_phone.setBackground(Qt.GlobalColor.yellow)
            #push column(s) into row:
            self.tableWidgetEmployee.setItem(row,0,column_id)
            self.tableWidgetEmployee.setItem(row,1,column_name)
            self.tableWidgetEmployee.setItem(row,2,column_email)
            self.tableWidgetEmployee.setItem(row,3,column_phone)
        self.is_Completed = True

    def show_detail(self):
        if self.is_Completed==False:
            return
        row_number=self.tableWidgetEmployee.currentIndex().row()
        id=self.tableWidgetEmployee.item(row_number,0).text()
        emp=self.ec.get_detail(id)

        if emp!= None:
            self.lineEditID.setText(str(emp.ID))
            self.lineEditName.setText(emp.Name)
            self.lineEditPhone.setText(emp.Phone)
            self.lineEditEmail.setText(emp.Email)
            self.lineEditPassword.setText(emp.Password)

    def clear_data(self):
        self.lineEditID.setText("")
        self.lineEditName.clear()
        self.lineEditPhone.setText("")
        self.lineEditEmail.setText("")
        self.lineEditName.setFocus()

    def insert_data(self):
        self.is_Completed = False
        emp=Employee()
        emp.Name=self.lineEditName.text()
        emp.Email=self.lineEditEmail.text()
        emp.Phone=self.lineEditPhone.text()
        emp.Password=self.lineEditPassword.text()
        emp.IsDeleted=0
        result=self.ec.insert_employee(emp)
        if result > 0:
            self.display_all_employees()
        else:
            #use msgbox for warning
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setWindowTitle("Infor")
            msg.setText("Cannot insert a new employee!!!")
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()

    def update_data(self):
        self.is_Completed = False
        emp = Employee()
        emp.ID = int(self.lineEditID.text())
        emp.Name = self.lineEditName.text()
        emp.Email = self.lineEditEmail.text()
        emp.Phone = self.lineEditPhone.text()
        emp.Password = self.lineEditPassword.text()
        emp.IsDeleted = 0
        if self.checkBoxIsDeleted.isChecked():
            emp.IsDeleted=1
        result = self.ec.update_detail(emp)
        if result > 0:
            self.display_all_employees()
        else:
            # use msgbox for warning
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setWindowTitle("Infor")
            msg.setText("Cannot update employee!!!")
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()

    def delete_data(self):
        self.is_Completed = False
        emp = Employee()
        emp.ID = int(self.lineEditID.text())

        result = self.ec.delete_employee(emp)
        if result > 0:
            self.display_all_employees()
        else:
            # use msgbox for warning
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setWindowTitle("Infor")
            msg.setText("Cannot delete employee!!!")
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()
