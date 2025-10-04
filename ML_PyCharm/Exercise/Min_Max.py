import pandas as pd
class MyStatistic:
    def find_orders_within_range(self, df, minValue, maxValue, sortType=True):
        # Tính tổng giá trị từng đơn hàng (OrderID)
        order_totals = df.groupby('OrderID').apply(
            lambda x: (x['UnitPrice'] * x['Quantity'] * (1 - x['Discount'])).sum()
        ).reset_index(name="TotalValue")
        # Lọc đơn hàng trong khoảng [minValue, maxValue]
        filtered_orders = order_totals[
            (order_totals['TotalValue'] >= minValue) & (order_totals['TotalValue'] <= maxValue)
        ]
        # Sắp xếp theo TotalValue
        sorted_orders = filtered_orders.sort_values(by="TotalValue", ascending=sortType)

        return sorted_orders[["OrderID", "TotalValue"]]

if __name__ == "__main__":
    df = pd.read_csv('../dataset/SalesTransactions.csv')
    minValue = float(input("Input min: "))
    maxValue = float(input("Input max: "))
    sortType = input("Sort according ? (t/f): ").lower() == "t"
    stat = MyStatistic()
    result = stat.find_orders_within_range(df, minValue, maxValue, sortType)
    print("Danh sách hóa đơn trong phạm vi giá trị:")
    print(result)