from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt



file_path = (
    Path("data")
    / "WSTS-Historical-Billings-Report-Jun_2026 (1).xlsx"
)


df = pd.read_excel(
    file_path,
    sheet_name="Monthly Data",
    header=None
)



df["Year"] = pd.to_numeric(
    df[0],
    errors="coerce"
)

# Fill year values downward
df["Year"] = df["Year"].ffill()

# Remove rows where Year is still missing
df = df.dropna(subset=["Year"])

# Convert Year to integer
df["Year"] = df["Year"].astype(int)



df["Region"] = df[0]



df = df[
    ~pd.to_numeric(
        df["Region"],
        errors="coerce"
    ).notna()
]


columns = [
    "Original",
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
    "Total Year",
    "Q1",
    "Q2",
    "Q3",
    "Q4",
    "Year",
    "Region"
]

df.columns = columns




print("\n========== DATA INFORMATION ==========")

print("\nShape:")
print(df.shape)

print("\nColumns:")
print(df.columns.tolist())

print("\nData Types:")
print(df.dtypes)




worldwide = df[
    df["Region"] == "Worldwide"
]




worldwide_trend = worldwide[
    ["Year", "Total Year"]
].copy()




worldwide_trend["Billions_USD"] = (
    worldwide_trend["Total Year"]
    / 1_000_000
)




worldwide_trend["YoY_Growth_%"] = (
    worldwide_trend["Billions_USD"]
    .pct_change()
    * 100
)




recent_trend = worldwide_trend[
    worldwide_trend["Year"] >= 2020
]


print("\n========== WORLDWIDE SEMICONDUCTOR BILLINGS ==========")

print(
    recent_trend[
        [
            "Year",
            "Billions_USD",
            "YoY_Growth_%"
        ]
    ].to_string(index=False)
)




highest_year = worldwide_trend.loc[
    worldwide_trend["Billions_USD"].idxmax()
]


print("\n========== HIGHEST BILLING YEAR ==========")

print(
    f"Year: {highest_year['Year']}"
)

print(
    f"Billings: ${highest_year['Billions_USD']:.2f} Billion"
)


plt.figure(figsize=(10, 6))

plt.plot(
    recent_trend["Year"],
    recent_trend["Billions_USD"],
    marker="o"
)

plt.xlabel("Year")

plt.ylabel(
    "Semiconductor Billings (Billion USD)"
)

plt.title(
    "Worldwide Semiconductor Billings: 2020–2026"
)

plt.xticks(
    recent_trend["Year"]
)

plt.grid(True)

plt.tight_layout()

plt.savefig(
    Path("output") / "worldwide_semiconductor_billings.png"
)