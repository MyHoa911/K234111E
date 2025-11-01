from PyQt6.QtWidgets import QMessageBox, QMainWindow

from project_retail.connector.employee_connector import EmployeeConnector
from project_retail.ui.EmployeeManagementMainWindowExt import EmployeeManagementMainWindowExt
from project_retail.ui.LoginMainWindow import Ui_MainWindow


class LoginMainWindowExt(Ui_MainWindow):
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow=MainWindow
        self.setupSignalAndSlot()
    def showWindow(self):
        self.MainWindow.show()
    def closeWindow(self):
        self.MainWindow.close()
    def setupSignalAndSlot(self):
        self.pushButtonLogin.clicked.connect(self.process_login)
    def process_login(self):
        uid=self.lineEditUsername.text()
        pwd=self.lineEditPassword.text()
        ec = EmployeeConnector()
        ec.connect()
        em = ec.login(uid, pwd)
        if em == None:
            msg=QMessageBox()
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setWindowTitle("Infor")
            msg.setText("Login Failed, please contact ADMIN!!!")
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()
        else:
            self.closeWindow()
            self.gui_emp=EmployeeManagementMainWindowExt() #phải có self để hiểu là biến local
            self.gui_emp.setupUi(QMainWindow())
            self.gui_emp.showWindow()

