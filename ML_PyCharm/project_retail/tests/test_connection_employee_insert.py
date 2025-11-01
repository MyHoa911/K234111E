from project_retail.connector.employee_connector import EmployeeConnector
from project_retail.model.employee import Employee

ec=EmployeeConnector()
ec.connect()

emp=Employee()
emp.Name="Lê Thị Mỹ Hòa"
emp.Email="piggy@gmail.com"
emp.Phone="072761853"
emp.Password="911"
emp.IsDeleted=0
result=ec.insert_employee(emp)
if result>0:
    print("Insert Ok")
else:
    print("Insert Failed!!!")