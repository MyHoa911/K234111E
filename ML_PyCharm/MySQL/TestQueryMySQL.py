import mysql.connector

server = "localhost"
port = 3306
database = "studentmanagement"
username = "root"
password = "Mhoasql@911"

conn = mysql.connector.connect(
                host=server,
                port=port,
                database=database,
                user=username,
                password=password)

cursor = conn.cursor()

sql="select * from student"
cursor.execute(sql)
#truy vấn toàn bộ sinh viên
dataset=cursor.fetchall()
align='{0:<3} {1:<6} {2:<15} {3:<10}'
print(align.format('ID', 'Code','Name',"Age"))
for item in dataset:
    id=item[0]
    code=item[1]
    name=item[2]
    age=item[3]
    avatar=item[4]
    intro=item[5]
    print(align.format(id,code,name,age))

cursor.close()
print("="*30)

#truy vấn các sinh viên có độ tuổi từ 22 tới 26
cursor = conn.cursor()
sql="SELECT * FROM student where Age>=22 and Age<=26"
cursor.execute(sql)

dataset=cursor.fetchall()
align='{0:<3} {1:<6} {2:<15} {3:<10}'
print(align.format('ID', 'Code','Name',"Age"))
for item in dataset:
    id=item[0]
    code=item[1]
    name=item[2]
    age=item[3]
    avatar=item[4]
    intro=item[5]
    print(align.format(id,code,name,age))

cursor.close()
print("="*30)

#truy vấn toàn bộ sinh viên và sp xếp theo tuổi tăng dần
cursor = conn.cursor()
sql="SELECT * FROM student order by Age asc"
cursor.execute(sql)

dataset=cursor.fetchall()
align='{0:<3} {1:<6} {2:<15} {3:<10}'
print(align.format('ID', 'Code','Name',"Age"))
for item in dataset:
    id=item[0]
    code=item[1]
    name=item[2]
    age=item[3]
    avatar=item[4]
    intro=item[5]
    print(align.format(id,code,name,age))

cursor.close()
print("="*30)

#truy vấn các sinh viên có độ tuổi từ 22 tới 26 và sắp xếp theo tuổi giảm dần
cursor = conn.cursor()
sql="SELECT * FROM student " \
    "where Age>=22 and Age<=26 " \
    "order by Age desc "
cursor.execute(sql)

dataset=cursor.fetchall()
align='{0:<3} {1:<6} {2:<15} {3:<10}'
print(align.format('ID', 'Code','Name',"Age"))
for item in dataset:
    id=item[0]
    code=item[1]
    name=item[2]
    age=item[3]
    avatar=item[4]
    intro=item[5]
    print(align.format(id,code,name,age))

cursor.close()
print("="*30)

#truy vấn chi tiết thông tin Sinh viên khi biết ID
cursor = conn.cursor()
sql="SELECT * FROM student " \
    "where ID=1 "

cursor.execute(sql)

dataset=cursor.fetchone()
if dataset!=None:
    id,code,name,age,avatar,intro=dataset
    print("Id =",id)
    print("Code =",code)
    print("Name =",name)
    print("Age =",age)

cursor.close()
print("="*30)

#truy vấn dạng phân trang Student
cursor = conn.cursor()
sql="SELECT * FROM student LIMIT 3 OFFSET 0"
cursor.execute(sql)
dataset=cursor.fetchall()
align='{0:<3} {1:<6} {2:<15} {3:<10}'
print(align.format('ID', 'Code','Name',"Age"))
for item in dataset:
    id=item[0]
    code=item[1]
    name=item[2]
    age=item[3]
    avatar=item[4]
    intro=item[5]
    print(align.format(id,code,name,age))
cursor.close()
print("="*15)

cursor = conn.cursor()
sql="SELECT * FROM student LIMIT 3 OFFSET 3" #limit là số phần tử, offset là vị trí bđ
cursor.execute(sql)
dataset=cursor.fetchall()
align='{0:<3} {1:<6} {2:<15} {3:<10}'
print(align.format('ID', 'Code','Name',"Age"))
for item in dataset:
    id=item[0]
    code=item[1]
    name=item[2]
    age=item[3]
    avatar=item[4]
    intro=item[5]
    print(align.format(id,code,name,age))
cursor.close()
print("="*15)

print("PAGING!!!!!")
cursor = conn.cursor()
sql="SELECT count(*) FROM student"
cursor.execute(sql)
dataset=cursor.fetchone()
rowcount=dataset[0]
limit=3
step=3
for offset in range(0,rowcount,step):
    sql=f"SELECT * FROM student LIMIT {limit} OFFSET {offset}"
    cursor.execute(sql)
    dataset=cursor.fetchall()
    align='{0:<3} {1:<6} {2:<15} {3:<10}'
    print(align.format('ID', 'Code','Name',"Age"))
    for item in dataset:
        id=item[0]
        code=item[1]
        name=item[2]
        age=item[3]
        avatar=item[4]
        intro=item[5]
        print(align.format(id,code,name,age))
cursor.close()
print("="*50)

#thêm mới 1 student
cursor = conn.cursor()
sql="insert into student (code,name,age) values (%s,%s,%s)"
val=("SV07","Trần Duy Thanh",45)
cursor.execute(sql,val)
conn.commit()
print(cursor.rowcount," record inserted")
cursor.close()
print("="*30)

#thêm mới nhiều Student
cursor = conn.cursor()
sql="insert into student (code,name,age) values (%s,%s,%s)"
val=[
    ("SV08","Trần Quyết Chiến",19),
    ("SV09","Hồ Thắng",22),
    ("SV10","Hoàng Hà",25),
     ]
cursor.executemany(sql,val)
conn.commit()
print(cursor.rowcount," record inserted")
cursor.close()
print("="*50)

#cập nhật tên Sinh viên có Code=’sv09′ thành tên mới “Trúc Nhân”
cursor = conn.cursor()
sql="update student set name='Trúc Nhân' where Code='SV07'"
cursor.execute(sql)
conn.commit()
print(cursor.rowcount," record(s) affected")

#cập nhật tên sinh viên có Code=’sv09′ thành tên mới “Hoàng Lão Tà” như viết dạng SQL Injection
cursor = conn.cursor()
sql="update student set name=%s where Code=%s"
val=('Hoàng Lão Tà','SV09')
cursor.execute(sql,val)
conn.commit()
print(cursor.rowcount," record(s) affected")

print("="*50)
#xóa Student có ID=14
conn = mysql.connector.connect(
                host=server,
                port=port,
                database=database,
                user=username,
                password=password)
cursor = conn.cursor()
sql="DELETE from student where ID=9"
cursor.execute(sql)
conn.commit()
print(cursor.rowcount," record(s) affected")

#xóa Student có ID=13 với SQL Injection
conn = mysql.connector.connect(
                host=server,
                port=port,
                database=database,
                user=username,
                password=password)
cursor = conn.cursor()
sql = "DELETE from student where ID=%s"
val = (11,)
cursor.execute(sql, val)
conn.commit()
print(cursor.rowcount," record(s) affected")