from project_retail.connector.employee_connector import EmployeeConnector


ec=EmployeeConnector()
ec.connect()
emp=ec.get_detail("4")
emp.Name="Tâm Như"
emp.Email="nhu@gmail.com"
result=ec.update_detail(emp)
if result > 0:
    print("Update Successful!!!")
else:
    print("Update FAILED!!")
