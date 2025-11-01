import mysql.connector

server="localhost"
port=3306
database="k23_retail"
username="root"
password="Mhoasql@911"

conn = mysql.connector.connect(
                host=server,
                port=port,
                database=database,
                user=username,
                password=password)
print("Connected!!!!")