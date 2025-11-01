import pandas as pd
import json
from project_retail.tests.test_salesdatabase import runKMeans, df2, conn


def exportClusterDetails(conn, df_clustered, file_name, multi_sheet=True):
    clusters = sorted(df_clustered["cluster"].unique())
    all_results = []

    if multi_sheet:
        with pd.ExcelWriter(file_name) as writer:
            for c in clusters:
                customer_ids = df_clustered.loc[df_clustered["cluster"] == c, "CustomerID"].tolist()
                sql = f"SELECT * FROM customer WHERE CustomerID IN ({','.join(map(str, customer_ids))})"
                df_cluster = conn.queryDataset(sql)
                df_cluster["cluster"] = c
                df_cluster.to_excel(writer, sheet_name=f"Cluster_{c}", index=False)
                print(f"✅ Đã ghi cụm {c} vào sheet 'Cluster_{c}'")
                all_results.append(df_cluster)

        print(f"\n🎯 Xuất thành công toàn bộ cụm vào file Excel: {file_name}")

    else:
        for c in clusters:
            customer_ids = tuple(df_clustered.loc[df_clustered["cluster"] == c, "CustomerID"])
            if len(customer_ids) == 1:
                customer_ids = f"({customer_ids[0]})"
            sql = f"SELECT * FROM customer WHERE CustomerID IN {customer_ids}"
            df_cluster = conn.queryDataset(sql)
            df_cluster["cluster"] = c
            all_results.append(df_cluster)
            print(f"=== CLUSTER {c} ===")
            print(df_cluster)

        df_all = pd.concat(all_results)
        df_all.to_csv(file_name, index=False)
        print(f"\n🎯 Xuất thành công toàn bộ cụm vào file CSV: {file_name}")

    return pd.concat(all_results, ignore_index=True)


def generateModernDashboard(df_cluster_details, df_clustered, k):
    """
    Tạo dashboard HTML hiện đại giống React component
    """
    # Màu sắc cho từng cluster
    colors = ['#3b82f6', '#ef4444', '#10b981', '#f59e0b', '#8b5cf6', '#ec4899']

    # Tính toán thống kê cho mỗi cluster
    cluster_stats = []
    for cluster_id in sorted(df_cluster_details['cluster'].unique()):
        cluster_data = df_cluster_details[df_cluster_details['cluster'] == cluster_id]
        stats = {
            'id': int(cluster_id),
            'name': f'Cluster {cluster_id}',
            'color': colors[cluster_id] if cluster_id < len(colors) else colors[0],
            'customerCount': len(cluster_data),
            'avgAge': round(cluster_data['Age'].mean(), 1) if 'Age' in cluster_data.columns else 0,
            'avgIncome': round(cluster_data['Annual Income'].mean(),
                               0) if 'Annual Income' in cluster_data.columns else 0,
            'avgSpending': round(cluster_data['Spending Score'].mean(),
                                 1) if 'Spending Score' in cluster_data.columns else 0,
        }
        cluster_stats.append(stats)

    # Prepare customer data
    customers_data = []
    for _, row in df_cluster_details.iterrows():
        customer = {
            'CustomerID': str(row.get('CustomerID', 'N/A')),
            'cluster': int(row['cluster']),
            'Age': int(row.get('Age', 0)) if pd.notna(row.get('Age')) else 0,
            'Gender': str(row.get('Gender', 'N/A')),
            'AnnualIncome': int(row.get('Annual Income', 0)) if pd.notna(row.get('Annual Income')) else 0,
            'SpendingScore': int(row.get('Spending Score', 0)) if pd.notna(row.get('Spending Score')) else 0,
        }
        customers_data.append(customer)

    # Generate HTML
    html_content = f"""
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Customer Segmentation Dashboard - K={k}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }}
        .cluster-card {{
            transition: all 0.3s ease;
        }}
        .cluster-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        }}
        .cluster-card.selected {{
            ring-width: 4px;
            ring-color: rgb(59, 130, 246);
        }}
        .fade-in {{
            animation: fadeIn 0.5s ease-in;
        }}
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
    </style>
</head>
<body class="bg-gradient-to-br from-slate-50 to-slate-100 min-h-screen">
    <div class="container mx-auto p-6 max-w-7xl">
        <!-- Header -->
        <div class="bg-white rounded-2xl shadow-lg p-8 mb-6 fade-in">
            <h1 class="text-4xl font-bold text-slate-800 mb-2">
                Customer Segmentation Analysis
            </h1>
            <p class="text-slate-600">K-Means Clustering Visualization (K = {k})</p>
            <div class="mt-4 text-sm text-slate-500">
                📊 Tổng số khách hàng: <span class="font-bold text-slate-700">{len(customers_data)}</span> |
                🎯 Số cụm: <span class="font-bold text-slate-700">{k}</span>
            </div>
        </div>

        <!-- Cluster Cards -->
        <div id="cluster-cards" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 mb-6">
            <!-- Cards will be generated by JavaScript -->
        </div>

        <!-- Charts -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
            <!-- Bar Chart -->
            <div class="bg-white rounded-2xl shadow-lg p-6 fade-in">
                <h2 class="text-xl font-bold text-slate-800 mb-4">📊 Phân bố khách hàng theo cụm</h2>
                <canvas id="barChart"></canvas>
            </div>

            <!-- Scatter Chart -->
            <div class="bg-white rounded-2xl shadow-lg p-6 fade-in">
                <h2 class="text-xl font-bold text-slate-800 mb-4">💰 Thu nhập vs Chi tiêu</h2>
                <canvas id="scatterChart"></canvas>
            </div>
        </div>

        <!-- Customer Table -->
        <div class="bg-white rounded-2xl shadow-lg p-6 fade-in">
            <div class="flex items-center justify-between mb-4">
                <h2 class="text-xl font-bold text-slate-800" id="table-title">
                    Tất cả khách hàng
                </h2>
                <button id="reset-filter" class="px-4 py-2 bg-slate-200 hover:bg-slate-300 rounded-lg text-sm font-semibold transition-all hidden">
                    Xem tất cả
                </button>
            </div>

            <div class="overflow-x-auto">
                <table class="w-full">
                    <thead>
                        <tr class="border-b-2 border-slate-200">
                            <th class="text-left py-3 px-4 text-slate-600 font-semibold">Customer ID</th>
                            <th class="text-left py-3 px-4 text-slate-600 font-semibold">Cluster</th>
                            <th class="text-left py-3 px-4 text-slate-600 font-semibold">Age</th>
                            <th class="text-left py-3 px-4 text-slate-600 font-semibold">Gender</th>
                            <th class="text-left py-3 px-4 text-slate-600 font-semibold">Annual Income</th>
                            <th class="text-left py-3 px-4 text-slate-600 font-semibold">Spending Score</th>
                        </tr>
                    </thead>
                    <tbody id="customer-table-body">
                        <!-- Rows will be generated by JavaScript -->
                    </tbody>
                </table>
                <div id="table-footer" class="text-center py-4 text-slate-500"></div>
            </div>
        </div>
    </div>

    <script>
        // Data
        const clusterStats = {json.dumps(cluster_stats)};
        const customersData = {json.dumps(customers_data)};

        let selectedCluster = null;
        let barChart, scatterChart;

        // Generate Cluster Cards
        function generateClusterCards() {{
            const container = document.getElementById('cluster-cards');
            container.innerHTML = '';

            clusterStats.forEach(cluster => {{
                const card = document.createElement('div');
                card.className = 'cluster-card bg-white rounded-xl shadow-lg p-6 cursor-pointer';
                card.style.borderTop = `4px solid ${{cluster.color}}`;
                card.onclick = () => toggleCluster(cluster.id);

                card.innerHTML = `
                    <div class="flex items-center justify-between mb-4">
                        <h3 class="text-lg font-bold text-slate-800">${{cluster.name}}</h3>
                        <div class="w-10 h-10 rounded-full flex items-center justify-center" 
                             style="background-color: ${{cluster.color}}20;">
                            <svg class="w-5 h-5" style="color: ${{cluster.color}}" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path>
                            </svg>
                        </div>
                    </div>

                    <div class="space-y-3">
                        <div class="flex items-center gap-2">
                            <span class="text-2xl font-bold" style="color: ${{cluster.color}}">
                                ${{cluster.customerCount}}
                            </span>
                            <span class="text-slate-600 text-sm">khách hàng</span>
                        </div>

                        <div class="border-t pt-3 space-y-2">
                            <div class="flex items-center justify-between text-sm">
                                <span class="text-slate-600">Tuổi TB:</span>
                                <span class="font-semibold text-slate-800">${{cluster.avgAge}}</span>
                            </div>
                            <div class="flex items-center justify-between text-sm">
                                <span class="text-slate-600">Thu nhập TB:</span>
                                <span class="font-semibold text-slate-800">$${{cluster.avgIncome.toLocaleString()}}</span>
                            </div>
                            <div class="flex items-center justify-between text-sm">
                                <span class="text-slate-600">Chi tiêu TB:</span>
                                <span class="font-semibold text-slate-800">${{cluster.avgSpending}}</span>
                            </div>
                        </div>
                    </div>
                `;

                container.appendChild(card);
            }});
        }}

        // Toggle Cluster Selection
        function toggleCluster(clusterId) {{
            selectedCluster = selectedCluster === clusterId ? null : clusterId;
            updateUI();
        }}

        // Update UI based on selection
        function updateUI() {{
            // Update cards selection
            const cards = document.querySelectorAll('.cluster-card');
            cards.forEach((card, index) => {{
                if (selectedCluster === index) {{
                    card.classList.add('selected', 'ring-4', 'ring-blue-500');
                }} else {{
                    card.classList.remove('selected', 'ring-4', 'ring-blue-500');
                }}
            }});

            // Update table
            updateTable();

            // Update charts
            updateCharts();

            // Update reset button
            const resetBtn = document.getElementById('reset-filter');
            const tableTitle = document.getElementById('table-title');
            if (selectedCluster !== null) {{
                resetBtn.classList.remove('hidden');
                tableTitle.textContent = `Chi tiết Cluster ${{selectedCluster}}`;
            }} else {{
                resetBtn.classList.add('hidden');
                tableTitle.textContent = 'Tất cả khách hàng';
            }}
        }}

        // Update Table
        function updateTable() {{
            const tbody = document.getElementById('customer-table-body');
            const footer = document.getElementById('table-footer');

            let displayData = selectedCluster !== null 
                ? customersData.filter(c => c.cluster === selectedCluster)
                : customersData;

            const displayLimit = 50;
            const displayCustomers = displayData.slice(0, displayLimit);

            tbody.innerHTML = '';
            displayCustomers.forEach(customer => {{
                const row = document.createElement('tr');
                row.className = 'border-b border-slate-100 hover:bg-slate-50 transition-colors';

                const clusterColor = clusterStats[customer.cluster].color;

                row.innerHTML = `
                    <td class="py-3 px-4 font-medium text-slate-700">${{customer.CustomerID}}</td>
                    <td class="py-3 px-4">
                        <span class="px-3 py-1 rounded-full text-white text-sm font-semibold"
                              style="background-color: ${{clusterColor}}">
                            ${{customer.cluster}}
                        </span>
                    </td>
                    <td class="py-3 px-4 text-slate-700">${{customer.Age}}</td>
                    <td class="py-3 px-4 text-slate-700">${{customer.Gender}}</td>
                    <td class="py-3 px-4 text-slate-700">$${{customer.AnnualIncome.toLocaleString()}}</td>
                    <td class="py-3 px-4 text-slate-700">${{customer.SpendingScore}}</td>
                `;

                tbody.appendChild(row);
            }});

            if (displayData.length > displayLimit) {{
                footer.textContent = `Hiển thị ${{displayLimit}}/${{displayData.length}} khách hàng`;
            }} else {{
                footer.textContent = '';
            }}
        }}

        // Create Bar Chart
        function createBarChart() {{
            const ctx = document.getElementById('barChart').getContext('2d');
            barChart = new Chart(ctx, {{
                type: 'bar',
                data: {{
                    labels: clusterStats.map(c => c.name),
                    datasets: [{{
                        label: 'Số lượng khách hàng',
                        data: clusterStats.map(c => c.customerCount),
                        backgroundColor: clusterStats.map(c => c.color),
                        borderRadius: 8,
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: true,
                    plugins: {{
                        legend: {{ display: false }}
                    }},
                    scales: {{
                        y: {{ beginAtZero: true }}
                    }}
                }}
            }});
        }}

        // Create Scatter Chart
        function createScatterChart() {{
            const ctx = document.getElementById('scatterChart').getContext('2d');

            const datasets = clusterStats.map(cluster => ({{
                label: cluster.name,
                data: customersData
                    .filter(c => c.cluster === cluster.id)
                    .map(c => ({{ x: c.AnnualIncome, y: c.SpendingScore }})),
                backgroundColor: cluster.color,
                borderColor: cluster.color,
            }}));

            scatterChart = new Chart(ctx, {{
                type: 'scatter',
                data: {{ datasets }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: true,
                    plugins: {{
                        legend: {{ position: 'top' }}
                    }},
                    scales: {{
                        x: {{ 
                            title: {{ display: true, text: 'Annual Income ($)' }}
                        }},
                        y: {{ 
                            title: {{ display: true, text: 'Spending Score' }}
                        }}
                    }}
                }}
            }});
        }}

        // Update Charts
        function updateCharts() {{
            if (selectedCluster !== null) {{
                const filteredData = customersData.filter(c => c.cluster === selectedCluster);
                scatterChart.data.datasets = [{{
                    label: `Cluster ${{selectedCluster}}`,
                    data: filteredData.map(c => ({{ x: c.AnnualIncome, y: c.SpendingScore }})),
                    backgroundColor: clusterStats[selectedCluster].color,
                    borderColor: clusterStats[selectedCluster].color,
                }}];
            }} else {{
                scatterChart.data.datasets = clusterStats.map(cluster => ({{
                    label: cluster.name,
                    data: customersData
                        .filter(c => c.cluster === cluster.id)
                        .map(c => ({{ x: c.AnnualIncome, y: c.SpendingScore }})),
                    backgroundColor: cluster.color,
                    borderColor: cluster.color,
                }}));
            }}
            scatterChart.update();
        }}

        // Reset Filter
        document.getElementById('reset-filter').onclick = () => {{
            selectedCluster = null;
            updateUI();
        }};

        // Initialize
        generateClusterCards();
        updateTable();
        createBarChart();
        createScatterChart();
    </script>
</body>
</html>
    """

    # Lưu file HTML
    html_file = f"cluster_dashboard_k{k}.html"
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"\n🌐 Đã tạo dashboard tại: {html_file}")

    # Tự động mở trên browser
    import webbrowser
    import os
    webbrowser.open('file://' + os.path.realpath(html_file))


# Main execution
for k in [4, 5, 6]:
    print(f"\n{'=' * 60}")
    print(f"🚀 RUNNING K-MEANS WITH K={k}")
    print(f"{'=' * 60}")

    # Copy dữ liệu để không ghi đè giữa các lần chạy
    df_temp = df2.copy()

    # Chọn cột đặc trưng
    X = df_temp.loc[:, ["Age", "Annual Income", "Spending Score"]].values

    # Chạy KMeans
    y_kmeans, centroids, labels = runKMeans(X, k)
    df_temp["cluster"] = labels

    # Xuất file Excel
    df_cluster_details = exportClusterDetails(conn, df_temp, f"cluster_details_k{k}.xlsx", multi_sheet=True)

    # Tạo dashboard HTML đẹp
    generateModernDashboard(df_cluster_details, df_temp, k)

    print(f"\n✅ Hoàn thành phân tích cho K={k}")

print(f"\n{'=' * 60}")
print("🎉 ĐÃ HOÀN THÀNH TẤT CẢ!")
print(f"{'=' * 60}")