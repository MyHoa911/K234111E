from project_retail.connector.employee_connector import EmployeeConnector

ec=EmployeeConnector()
ec.connect()
em=ec.login("hoa@gmail.com", 4678)
if em==None:
    print("Login Failed!!!")
else:
    print(em)

print("Test - All Employess:")
employees=ec.get_list_employee()
for emp in employees:
    print(emp)

print("-------ID=4---------")
id=4
emp=ec.get_detail(id)
if emp != None:
    print("FOUND ID=",id)
    print(emp)
else:
    print("NOT FOUND ID = ", id)