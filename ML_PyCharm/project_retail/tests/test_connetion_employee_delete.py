from project_retail.connector.employee_connector import EmployeeConnector
from project_retail.model.employee import Employee

ec=EmployeeConnector()
ec.connect()
# emp=ec.get_detail("5")
emp=Employee()
emp.ID=10
result=ec.delete_employee(emp)
if result > 0:
    print("Delete Successful!!!")
else:
    print("Delete FAILED!!")
