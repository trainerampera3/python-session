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


df["Year"] = df["Year"].ffill()


df = df.dropna(subset=["Year"])


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




# print("\nShape:")
# print(df.shape)

# print("\nColumns:")
# print(df.columns.tolist())

# print("\nData Types:")
# print(df.dtypes)




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




# print(
#     f"Year: {highest_year['Year']}"
# )

# print(
#     f"Billings: ${highest_year['Billions_USD']:.2f} Billion"
# )


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

# plt.savefig(
#     Path("output") / "worldwide_semiconductor_billings.png"
# )


regional = df[
    df["Region"] != "Worldwide"
]

highest_region = regional.loc[
    regional["Total Year"].idxmax()
]

print(
    f"Highest Region: {highest_region['Region']}"
)

print(
    f"Year: {highest_region['Year']}"
)

print(
    f"Billings: {highest_region['Total Year']}"
)



period_2020_2022 = recent_trend[
    recent_trend["Year"].between(2020, 2022)
]



print(
    period_2020_2022[
        [
            "Year",
            "Billions_USD",
            "YoY_Growth_%"
        ]
    ].to_string(index=False)
)


# Visualization
plt.figure(figsize=(10, 6))

plt.plot(
    period_2020_2022["Year"],
    period_2020_2022["Billions_USD"],
    marker="o"
)

plt.xlabel("Year")
plt.ylabel("Billings (Billion USD)")

plt.title(
    "Worldwide Semiconductor Billings: 2020–2022"
)

plt.xticks(
    period_2020_2022["Year"]
)

plt.grid(True)

plt.tight_layout()

plt.savefig(
    Path("output") / "semiconductor_billings_2020_2022.png"
)



recovery_period = recent_trend[
    recent_trend["Year"] >= 2022
]



print(
    recovery_period[
        [
            "Year",
            "Billions_USD",
            "YoY_Growth_%"
        ]
    ].to_string(index=False)
)



plt.figure(figsize=(10, 6))

plt.plot(
    recovery_period["Year"],
    recovery_period["Billions_USD"],
    marker="o"
)

plt.xlabel("Year")

plt.ylabel(
    "Billings (Billion USD)"
)

plt.title(
    "Semiconductor Market Recovery: 2022–2026"
)

plt.xticks(
    recovery_period["Year"]
)

plt.grid(True)

plt.tight_layout()

plt.savefig(
    Path("output") / "semiconductor_market_recovery_2022_2026.png"
)




year_2026 = recent_trend[
    recent_trend["Year"] == 2026
]


print(
    year_2026[
        [
            "Year",
            "Billions_USD",
            "YoY_Growth_%"
        ]
    ].to_string(index=False)
)


highest_year = recent_trend.loc[
    recent_trend["Billions_USD"].idxmax()
]

print("\nHighest Year in 2020–2026:")

print(
    f"Year: {highest_year['Year']}"
)

print(
    f"Billings: "
    f"${highest_year['Billions_USD']:.2f} Billion"
)


plt.figure(figsize=(10, 6))

plt.bar(
    recent_trend["Year"].astype(str),
    recent_trend["Billions_USD"]
)

plt.xlabel("Year")

plt.ylabel(
    "Billings (Billion USD)"
)

plt.title(
    "Worldwide Semiconductor Billings: 2020–2026"
)

plt.grid(
    axis="y"
)

plt.tight_layout()

plt.savefig(
    Path("output") / "semiconductor_billings_2020_2026.png"
)