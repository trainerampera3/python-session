import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
df=pd.read_excel("default.xlsx")
print(df)
print(df.head())
print(df.info())
print(df.describe())
df.drop(df.columns[0], axis=1, inplace=True)
print(df.head(10))
print(df.duplicated().sum())
print(df["default"].value_counts()) 
print(df["default"].value_counts(normalize=True)*100)
#  bar graph
# print(df["default"].value_counts().plot(kind="bar"))
# plt.xlabel("default status")
# plt.ylabel("no of custemors")
# plt.title("credit card default distribution")
# plt.xticks(rotation=0)
# plt.show()

# pie chart
# print(df["default"].value_counts().plot(kind="pie",autopct="%1.1f%%"))
# plt.ylabel("")
# plt.title("credit card default percentage")
# plt.show()

# this shows students have high default
print(df.groupby("student")["default"].value_counts())
print(df.groupby("student")["default"].value_counts(normalize=True)*100)
# this shows that people with default have high avg balance
print(df.groupby("default")["balance"].mean())
print(df.groupby("default")["income"].mean())

# histogram
df["balance"].hist(bins=30, edgecolor="black")
plt.xlabel("Balance")
plt.ylabel("no of customers")
plt.title("Balance Distribution")
plt.show()
# df["income"].hist(bins=30 )
# plt.xlabel("Balance")
# plt.ylabel("no of custmores")
# plt.title("income Distribution")
# plt.show()

#scater plots income vs balance
# df.ead(100).plot.scatter(x="income",y="balance")
# plt.xlabel("income")
# plt.ylabel("Balance")
# plt.title("income vs credit card bakance")
# plt.show()

# # box plot
# sns.boxplot(x="default", y="income", data=df)
# plt.xlabel("Default Status")
# plt.ylabel("Income")
# plt.title("Income by Default Status")
# plt.show()

# coorelation
# corr1=df[["balance","income"]].corr()
# print(corr1)
# sns.heatmap(corr1,annot=True)
# plt.title("correlation between numeric variables")
# plt.show()
df["default"]=df["default"].map({"Yes":1,"No":0})
corr2=df.corr(numeric_only=True)["default"].sort_values(ascending=False)
print(corr2)

