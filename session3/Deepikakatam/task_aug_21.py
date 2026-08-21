import numpy as np
import pandas as pd
import pathlib as path
import matplotlib.pyplot as plt
data = pd.read_csv(path.Path(__file__).parent / "swiggy_scrap_uncleaned.csv")

# print(data)
# print(data.columns)
# print(data.dtypes)
# print(data.iloc[0])
# print(data.iloc[0:5])
# print(data.iloc[0:5,0:3])
# print(data["hotel_name"])
# print(data[["food_type","location","offer"]])
# print(data.shape)
# print(data.isnull())
# print(data.isnull().sum())
# print((data["offer"] == " ").sum())
# print(data[data.isnull().any(axis=1)])
# print(data[data.duplicated()])
# print(data.duplicated().sum())
# data = data.dropna()
# print(data.drop_duplicates())
# print(data)
# print(data["rating_and_delivery_time"].head(20))
# filter_data=data[data["food_type"]=="Desserts"]
# print(filter_data)
# filter_data=data[data["location"]=="Thakur Village"]
# print(filter_data)
# filter = data[data["offer"] == " 15% OFF UPTO ₹45"]
# print(filter)
# filter= data[(data["location"] == "Malad West") &(data["food_type"] == "Pizzas")]
# print(filter)
# data["price"] = None
# print(data)
# print(data.sort_values("hotel_name"))
# print(data.sort_values("hotel_name",ascending=False))
# print(data.describe())
# print(data.describe(include="all"))



# data["price"] = np.random.randint(100, 1001, size=len(data))
# print(data)
# print(data.dtypes)
# print(data[data["price"]>500])
# print(data[data["price"]<500])
# print(data.sort_values("price"))
# print(data.sort_values("price",ascending=False))



# print(data["location"].value_counts())
# print(data["food_type"].value_counts())

# print(data.groupby("location").size())
# print(data.groupby("location")["hotel_name"].count())
# print(data.groupby("location")["price"].mean())
# print(data.groupby("location")["price"].sum())



# location_count = data["location"].value_counts().head(20)
# plt.plot(location_count.values, location_count.index,marker="o")
# plt.xlabel("Number Of Hotels")
# plt.ylabel("Location")
# plt.title("Number of Hotels by Location")
# plt.savefig(path.Path(__file__).parent / "../plots_task_21/swiggy_line.png")



# food_count = data["food_type"].value_counts().head(20)
# plt.bar(food_count.values, food_count.index)
# plt.xlabel("Number of Hotels")
# plt.ylabel("Food Type")
# plt.title("Hotels by Food Type")
# plt.savefig(path.Path(__file__).parent / "../plots_task_21/swiggy_bar.png")


# food_count = data["food_type"].value_counts().head(5)
# plt.pie(food_count.values,labels=food_count.index,autopct="%1.1f%%")
# plt.title("Top 5 Food Types")
# plt.savefig(path.Path(__file__).parent / "../plots_task_21/swiggy_pie.png")


# data["rating"] = data["rating_and_delivery_time"].str.extract(r"(\d+\.\d+)").astype(float)
# plt.hist(data["rating"].dropna())
# plt.xlabel("Rating")
# plt.ylabel("Number of Hotels")
# plt.title("Distribution of Hotel Ratings")
# plt.savefig(path.Path(__file__).parent / "../plots_task_21/swiggy_hist.png")



# data["delivery_time"] = data["rating_and_delivery_time"].str.extract(r"(\d+)\s*mins?").astype(float)
# plt.scatter(data["rating"], data["delivery_time"])


x=data["rating_and_delivery_time"].head(5)
y=data["location"].head(5)
plt.xlabel("Delivery Time")
plt.ylabel("Rating")
plt.title("Rating vs Delivery Time")
plt.scatter(x,y)
plt.savefig(path.Path(__file__).parent / "../plots_task_21/swiggy_scatter.png")