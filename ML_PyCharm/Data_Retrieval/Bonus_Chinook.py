import sqlite3
import pandas as pd

# (1) Viết hàm trả về TOP N danh sách các Invoice có tổng trị giá trị từ a->b, sắp xếp giảm dần
def top_invoices_by_amount_range(a, b, n):
    try:
        conn = sqlite3.connect('../databases/Chinook_Sqlite.sqlite')
        print("DB Init")

        query = f"""
            SELECT i.InvoiceId, SUM(il.UnitPrice * il.Quantity) AS Total
            FROM Invoice i
            JOIN InvoiceLine il ON i.InvoiceId = il.InvoiceId
            GROUP BY i.InvoiceId
            HAVING Total BETWEEN {a} AND {b}
            ORDER BY Total DESC
            LIMIT {n};
        """

        df = pd.read_sql_query(query, conn)
        print(df)

    except sqlite3.Error as error:
        print("Error occured - ", error)
    finally:
        if conn:
            conn.close()
            print("SQLite Connection closed")


# (2) Viết hàm lọc ra TOP N khách hàng có nhiều Invoice nhất
def top_customers_by_invoice_count(n):
    try:
        conn = sqlite3.connect('../databases/Chinook_Sqlite.sqlite')
        print("DB Init")

        query = f"""
            SELECT c.CustomerId, c.FirstName || ' ' || c.LastName AS CustomerName, 
                   COUNT(i.InvoiceId) AS InvoiceCount
            FROM Customer c
            JOIN Invoice i ON c.CustomerId = i.CustomerId
            GROUP BY c.CustomerId
            ORDER BY InvoiceCount DESC
            LIMIT {n};
        """

        df = pd.read_sql_query(query, conn)
        print(df)

    except sqlite3.Error as error:
        print("Error occured - ", error)
    finally:
        if conn:
            conn.close()
            print("SQLite Connection closed")


# (3) Viết hàm lọc ra TOP N khách hàng có tổng giá trị Invoice cao nhất
def top_customers_by_invoice_value(n):
    try:
        conn = sqlite3.connect('../databases/Chinook_Sqlite.sqlite')
        print("DB Init")

        query = f"""
            SELECT c.CustomerId, c.FirstName || ' ' || c.LastName AS CustomerName,
                   SUM(il.UnitPrice * il.Quantity) AS TotalValue
            FROM Customer c
            JOIN Invoice i ON c.CustomerId = i.CustomerId
            JOIN InvoiceLine il ON i.InvoiceId = il.InvoiceId
            GROUP BY c.CustomerId
            ORDER BY TotalValue DESC
            LIMIT {n};
        """

        df = pd.read_sql_query(query, conn)
        print(df)

    except sqlite3.Error as error:
        print("Error occured - ", error)
    finally:
        if conn:
            conn.close()
            print("SQLite Connection closed")


print("TOP 5 Invoice có giá trị từ 5 -> 25:")
top_invoices_by_amount_range(5, 25, 5)

print("\nTOP 5 khách hàng có nhiều Invoice nhất:")
top_customers_by_invoice_count(5)

print("\nTOP 5 khách hàng có tổng giá trị Invoice cao nhất:")
top_customers_by_invoice_value(5)
