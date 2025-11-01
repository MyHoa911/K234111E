import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
import plotly.express as px


from project_retail.connector.connector import Connector

conn=Connector(database="salesdatabase")
conn.connect()
sql="select * from customer"
df=conn.queryDataset(sql)
print(df)
sql2=("select distinct customer.CustomerId, Age, Annual_Income,Spending_Score from customer, customer_spend_score "
      "where customer.CustomerId=customer_spend_score.CustomerID")
df2=conn.queryDataset(sql2)
df2.columns = ['CustomerID', 'Age', 'Annual Income', 'Spending Score']
print(df2)
print(df2.head())
print(df2.describe())

def showHistogram(df,columns):
    plt.figure(1, figsize=(7,8))
    n = 0
    for column in columns:
        n +=1
        plt.subplot(3, 1, n)
        plt.subplots_adjust(hspace=0.5, wspace=0.5)
        sns.distplot(df[column], bins=32)
        plt.title(f'Histogram of {column}')
    plt.show()
showHistogram(df2,df2.columns[1:])

def elbowMethod(df, columnsForElbow):
    """
    Hàm vẽ Elbow Method để xác định số cụm tối ưu (k).
    df: DataFrame chứa dữ liệu
    columnsForElbow: danh sách tên cột dùng để phân cụm
    """

    # Lấy dữ liệu theo các cột cần dùng để phân cụm
    X = df.loc[:, columnsForElbow].values

    inertia = []

    # Thử lần lượt từ 1 đến 10 cụm
    for n in range(1, 11):
        model = KMeans(
            n_clusters=n,
            init='k-means++',   # phương pháp khởi tạo tốt giúp hội tụ nhanh
            max_iter=500,       # số vòng lặp tối đa
            random_state=42     # cố định kết quả ngẫu nhiên cho reproducibility
        )
        model.fit(X)
        inertia.append(model.inertia_)  # lưu lại tổng bình phương khoảng cách

    plt.figure(1, figsize=(15, 6))
    plt.plot(np.arange(1, 11), inertia, 'o')
    plt.plot(np.arange(1, 11), inertia, '--', alpha=0.5)
    plt.xlabel('Number of Clusters'), plt.ylabel('Cluster Sum of Squared Distances')
    plt.show()
# columns=['Age', 'Spending Score']
# elbowMethod(df2, columns)
# columns=['Annual Income', 'Spending Score']
# elbowMethod(df2, columns)
columns=['Age', 'Annual Income', 'Spending Score']
elbowMethod(df2, columns)
def runKMeans(X, cluster):
    model = KMeans(
        n_clusters=cluster,
        init='k-means++',
        max_iter=500,
        random_state=42
    )
    model.fit(X)
    labels = model.labels_
    centroids = model.cluster_centers_
    y_kmeans = model.fit_predict(X)
    return y_kmeans, centroids, labels

X = df2.loc[:, columns].values
cluster = 6
colors = ["red", "green", "blue", "purple", "black", "pink", "orange"]

y_kmeans, centroids, labels = runKMeans(X, cluster)
print(y_kmeans)
print(centroids)
print(labels)

df2["cluster"] = labels


# def visualizeKMeans(X, y_kmeans, cluster, title, xlabel, ylabel, colors):
#     plt.figure(figsize=(10, 10))  # tạo khung vẽ kích thước 10x10 inch
#
#     for i in range(cluster):  # lặp qua từng cụm
#         plt.scatter(
#             X[y_kmeans == i, 0],  # trục X của điểm thuộc cụm i
#             X[y_kmeans == i, 1],  # trục Y của điểm thuộc cụm i
#             s=100,  # kích thước điểm
#             c=colors[i],  # màu tương ứng trong danh sách colors
#             label='Cluster %i' % (i + 1)  # chú thích từng cụm
#         )
#
#     plt.title(title)
#     plt.xlabel(xlabel)
#     plt.ylabel(ylabel)
#     plt.legend()
#     plt.show()
# visualizeKMeans(X,
#                 y_kmeans,
#                 cluster,
#                 "Cluster of Customers - Age X Spending Score",
#                 "Age",
#                 "Spending Score",
#                 colors)
# visualizeKMeans(X,
#                 y_kmeans,
#                 cluster,
#                 "Cluster of Customers - Age X Spending Score",
#                 "Annual Income",
#                 "Spending Score",
#                 colors)
def visualize3DKmeans(df, columns, hover_data, cluster):
    fig = px.scatter_3d(df,
                        x=columns[0],
                        y=columns[1],
                        z=columns[2],
                        color='cluster',
                        hover_data=hover_data,
                        category_orders={"cluster":range(0,cluster)},
                        )
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0))
    fig.show()
hover_data = df2.columns
visualize3DKmeans(df2, columns, hover_data, cluster)
