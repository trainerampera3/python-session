import pandas as pd
import pathlib as path
import matplotlib.pyplot as plt

def main():
    data = pd.read_csv(path.Path(__file__).parent / "../data/ecommerce-dataset.csv")
    # print(data.head())
    # print(data.describe())
    # print(data.info())
    # print(data.columns)
    # print(data.head(50))
    # print(data.loc[0].value_counts())
    # print(data[['order_id', 'order_date']])
    # print(data['revenue']>1000)
    # print(data.describe(include='object'))
    # print(data.columns.tolist())
    # print(data.dtypes)
    # plt.plot(data["order_id"], data["revenue"])
    # plt.xlabel("Order ID")
    # plt.ylabel("Revenue")
    # plt.title("Revenue by Order")

    # plt.savefig(path.Path(__file__).parent / "../plots/revenue_by_order.png")
    # plt.savefig(path.Path(__file__).parent / "")
    
    category_revenue = data.groupby("product_category")["revenue"].sum()

    # plt.bar(category_revenue.index, category_revenue.values)

    # plt.xlabel("Product Category")
    # plt.ylabel("Revenue")
    # plt.title("Revenue by Product Category")

    # plt.savefig(path.Path(__file__).parent / "../plots/revenue_by_product_category.png")
    # plt.hist(data["revenue"])

    # plt.xlabel("Revenue")
    # plt.ylabel("Number of Orders")
    # plt.title("Revenue Distribution")

    # plt.savefig(path.Path(__file__).parent / "../plots/revenue_distribution.png")
    # plt.scatter(data["quantity"], data["revenue"])

    # plt.xlabel("Quantity")
    # plt.ylabel("Revenue")
    # plt.title("Quantity vs Revenue")

    # plt.savefig(path.Path(__file__).parent / "../plots/quantity_vs_revenue.png")
    
#     payment_counts = data["payment_method"].value_counts()

#     plt.pie(
#         payment_counts.values,
#         labels=payment_counts.index,
#         autopct="%1.1f%%"
#     )

#     plt.title("Payment Method Distribution")

#     plt.savefig(path.Path(__file__).parent / "../plots/payment_method_distribution.png")

    
    # fig, ax = plt.subplots()

    # ax.plot(data["order_id"], data["revenue"])

    # ax.set_xlabel("Order ID")
    # ax.set_ylabel("Revenue")
    # ax.set_title("Revenue by Order")

    plt.savefig(path.Path(__file__).parent / "../plots/revenue_by_order.png")
if __name__ == "__main__":
    main()
    