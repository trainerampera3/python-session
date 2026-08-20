import pandas as pd
import pathlib as path
import matplotlib.pyplot as plt
data = pd.read_csv(
    path.Path(__file__).parent / "ecommerce_sales_analytics_5000.csv"
)

# print(data.describe())
# print(data.shape)
# print(data.info())
# print(data[["order_id","order_date"]])
# print(data["revenue"]>1000)
# print(data.sort_values("revenue"))
# print(data.sort_values("revenue", ascending=False))
# print(data.columns)
# print(data.columns.tolist())
# print(data[(data["revenue"] > 1000) & (data["quantity"] > 5)])
# print(data[(data["region"]=="South") | (data["region"]=="West")])
# data[(data["region"]=="South") | (data["region"]== "West")]


# plt.plot(data["order_id"],data["revenue"])
# plt.xlabel("oder_id")
# plt.ylabel("revenue")
# plt.title("Revenue order")
# plt.savefig(path.Path(__file__).parent / "../plots/revenue_order.png")


# plt.xlabel("product")
# plt.ylabel("revenue")
# plt.title("Revenue product")
# plt.bar(data["product_category"],data["revenue"])
# plt.savefig(path.Path(__file__).parent / "../plots/revenue_product.png")


# plt.xlabel("Product")
# plt.ylabel("Revenue")
# plt.title("Revenue by Product")
# plt.grid()

# plt.savefig(path.Path(__file__).parent / "../plots/revenue_product grid.png")

# x=data["order_id"]
# y=data["revenue"]
# plt.xlabel("Product")
# plt.ylabel("Revenue")
# plt.title("Revenue by Product")
# plt.scatter(x,y)

# plt.savefig(path.Path(__file__).parent / "../plots/revenue_product scatter.png")

# plt.hist(data["revenue"])
# plt.xlabel("Product")
# plt.ylabel("Revenue")
# plt.title("Revenue by Product")
# plt.savefig(path.Path(__file__).parent / "../plots/revenue_product hist.png")


payment_counts = data["payment_method"].value_counts()
plt.pie(payment_counts.values,labels=payment_counts.index,autopct="%1.1f%%")
plt.title("Payment Method Distribution")
plt.savefig(path.Path(__file__).parent / "../plots/payment_method_pie.png")