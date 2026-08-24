import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

df1 = pd.read_csv("./data/gym_track.csv")
print(df1.head())

# corr = df1.corr(numeric_only=True)
# sns.heatmap(corr,annot=True, cmap='coolwarm')
# plt.show()

df2 = pd.read_csv('./data/gym_renewal.csv')
print(df2.head())

# # corr = df2.corr(numeric_only=True)
# # sns.heatmap(corr,annot=True, cmap='coolwarm')
# # plt.show()

df2  = df2[:973]

df3 = pd.concat(
    [df1.reset_index(drop=True), df2.reset_index(drop=True)],
    axis=1
)

# # corr = df3.corr(numeric_only=True)
# # sns.heatmap(corr, annot=True, cmap='coolwarm')
# # plt.show()

# # sns.histplot(data=df2, x='age', hue='renewed_membership', bins=15)
# # plt.show()

# st.set_page_config(
#     page_title = 'Gym membership and Workout dashboard',
#     layout='wide'
# )


# st.title("🏋️ Gym Membership & Workout Dashboard")
# st.markdown(
#     "Overview of member activity, workout behavior and membership renewal."
# )

# df3 = df3.query('Age <= 25')
# youth = youth.groupby('renewed_membership').size()

def plot_bar(data, title, xlabel="", ylabel="Count", rotation=0, figsize=(8, 5), stacked=False):
    fig, ax = plt.subplots(figsize=figsize)
    data.plot(kind="bar", ax=ax, stacked=stacked)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.tick_params(axis="x", rotation=rotation)
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)


st.set_page_config(
    page_title="Gym Dashboard",
    page_icon="🏋️",
    layout="wide"
)

renewal_labels = {0: "Not Renewed", 1: "Renewed"}
# -----------------------------
# Title
# -----------------------------

st.title("Gym Membership & Workout Dashboard")

st.markdown(
    "Overview of member activity, workout behavior and membership renewal."
)


# -----------------------------
# Sidebar Filters
# -----------------------------

st.sidebar.header("🔍 Filters")

gender_filter = st.sidebar.multiselect(
    "Gender",
    options=df3["Gender"].unique(),
    default=df3["Gender"].unique()
)

workout_filter = st.sidebar.multiselect(
    "Workout Type",
    options=df3["Workout_Type"].unique(),
    default=df3["Workout_Type"].unique()
)

filtered_data = df3[
    (df3["Gender"].isin(gender_filter)) &
    (df3["Workout_Type"].isin(workout_filter))
]
print(filtered_data.info())

# -----------------------------
# KPI Calculations
# -----------------------------

total_members = len(filtered_data)

renewal_rate = (
    filtered_data["renewed_membership"].mean() * 100
)

avg_calories = filtered_data["Calories_Burned"].mean()

avg_frequency = filtered_data[
    "Workout_Frequency (days/week)"
].mean()


# -----------------------------
# KPI Cards
# -----------------------------

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Members",
    total_members
)

col2.metric(
    " Renewal Rate",
    f"{renewal_rate:.1f}%"
)

col3.metric(
    " Avg Calories Burned",
    f"{avg_calories:.0f}"
)

col4.metric(
    " Avg Workout Frequency",
    f"{avg_frequency:.1f} days/week"
)


st.divider()




st.subheader("Workout Performance")

col1, col2 = st.columns(2)

with col1:
    workout  = filtered_data['Workout_Type'].value_counts()
    ind = workout.index
    fig, ax = plt.subplots(figsize=(8,5))
    workout.plot(kind='pie', ax=ax, autopct='%1.1f%%')
    ax.set_title('Workout type')
    st.pyplot(fig, use_container_width=False)


with col2:
    gender_workout = pd.crosstab(
        filtered_data["Gender"],
        filtered_data["Workout_Type"]
    )
    
    plot_bar(
        gender_workout,
        "Workout Type Distribution by Gender",
        xlabel="Gender",
        ylabel="Number of Members"
    )

col1, col2 = st.columns(2)
with col1:
    gender_freq = filtered_data.groupby('Gender')['Workout_Frequency (days/week)'].mean()
    plot_bar(gender_freq, 'Avg workout frequenct of gender', xlabel='Gender',ylabel='No of days per week')

with col2:
    st.subheader(" Session Duration vs Calories Burned")

    fig, ax = plt.subplots(figsize=(10, 5))

    # Separate members based on renewal
    for status, label in [(0, "Not Renewed"), (1, "Renewed")]:

        temp = filtered_data[
            filtered_data["renewed_membership"] == status
        ]

        if not temp.empty:
            ax.scatter(
                temp["Session_Duration (hours)"],
                temp["Calories_Burned"],
                alpha=0.6,
                label=label
            )

    ax.set_title("Session Duration vs Calories Burned")
    ax.set_xlabel("Session Duration (hours)")
    ax.set_ylabel("Calories Burned")

    ax.legend()
    ax.grid(alpha=0.25)

    fig.tight_layout()

    st.pyplot(fig, use_container_width=True)

    plt.close(fig)

st.divider()

col1, col2 = st.columns(2)
with col1 :
    work_cal = filtered_data.pivot_table(index='Workout_Type', values='Calories_Burned', aggfunc='mean')
    

    plot_bar(work_cal, 'Workout_type vs Calories')
with col2:
    heart_rate = filtered_data[
    ["Resting_BPM", "Avg_BPM", "Max_BPM"]
    ]

    fig, ax = plt.subplots(figsize=(10, 5))

    heart_rate.boxplot(ax=ax)

    ax.set_title("Heart Rate Distribution")
    ax.set_xlabel("Heart Rate Type")
    ax.set_ylabel("BPM")

    ax.grid(axis="y", alpha=0.25)

    fig.tight_layout()

    st.pyplot(fig, use_container_width=True)

    plt.close(fig)


st.divider()
st.subheader("Member Profile")

col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(filtered_data["Age"], bins=10, edgecolor="black")
    ax.set_title("Age Distribution")
    ax.set_xlabel("Age")
    ax.set_ylabel("Number of Members")
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)


with col2:
    age_bins = list(range(15, 70, 10))

    if filtered_data["Age"].max() >= age_bins[-1]:
        age_bins.append(int(filtered_data["Age"].max()) + 1)

    age_groups = pd.cut(
        filtered_data["Age"],
        bins=age_bins,
        include_lowest=True
    )

    age_renewal = pd.crosstab(age_groups, filtered_data["renewed_membership"])
    age_renewal = age_renewal.rename(
        columns={0: "Not Renewed", 1: "Renewed"}
    )


    age_renewal = age_renewal[["Not Renewed", "Renewed"]]

    plot_bar(
        age_renewal,
        "Age Group vs Membership Renewal",
        xlabel="Age Group",
        ylabel="Number of Members",
        rotation=30
    )


col1, col2 = st.columns(2)

with col1:
    gender_renewal = (
        filtered_data.groupby("Gender")["renewed_membership"]
        .count()
    )

    plot_bar(
        gender_renewal,
        "Members by Gender",
        xlabel="Gender",
        ylabel="Number of Members"
    )

with col2:
    gender_frequency = (
        filtered_data.groupby("Gender")[
            "Workout_Frequency (days/week)"
        ]
        .mean()
    )

    plot_bar(
        gender_frequency,
        "Average Workout Frequency by Gender",
        xlabel="Gender",
        ylabel="Average Days per Week"
    )


col1, col2 = st.columns(2)

with col1:
    age_workout = pd.crosstab(age_groups, filtered_data["Workout_Type"])

    plot_bar(
        age_workout,
        "Workout Type Distribution by Age Group",
        xlabel="Age Group",
        ylabel="Number of Members",
        rotation=30,
        stacked=False
    )

with col2:
    gender_workout = pd.crosstab(
        filtered_data["Gender"],
        filtered_data["Workout_Type"]
    )

    plot_bar(
        gender_workout,
        "Workout Type Distribution by Gender",
        xlabel="Gender",
        ylabel="Number of Members"
    )
st.divider()
st.subheader('Membership Renewal')
col1, col2 = st.columns(2)
with col1 :
    st.subheader(" Workout Frequency vs Renewal Rate")

    frequency_renewal = (
        filtered_data.groupby("Workout_Frequency (days/week)")["renewed_membership"]
        .mean()
        .mul(100)
        .sort_index()
    )

    st.line_chart(frequency_renewal)

with col2:
    st.subheader(" Workout Type vs Renewal Rate")

    workout_renewal = (
        filtered_data.groupby("Workout_Type")["renewed_membership"]
        .mean()
        .mul(100)
        .sort_values(ascending=False)
    )

    plot_bar(workout_renewal, 'WorkoutType vs Reneal', xlabel='Type of workout', ylabel='Percentage of Renewal')


# st.subheader(" Login Frequency vs Membership Renewal")

# login_not_renewed = filtered_data.loc[
#     filtered_data["renewed_membership"] == 0,
#     "num_logins"
# ]

# login_renewed = filtered_data.loc[
#     filtered_data["renewed_membership"] == 1,
#     "num_logins"
# ]

# fig, ax = plt.subplots(figsize=(8, 4))

# ax.boxplot(
#     [login_not_renewed, login_renewed],
    
# )

# ax.set_title("Login Frequency vs Membership Renewal")
# ax.set_xlabel("Membership Status")
# ax.set_ylabel("Number of Logins")
# ax.grid(axis="y", alpha=0.25)

# fig.tight_layout()
# st.pyplot(fig, use_container_width=True)

# plt.close(fig)


st.subheader("Membership Type vs Membership Renewal")

membership_renewal = pd.crosstab(
    filtered_data["membership_type"],
    filtered_data["renewed_membership"]
)

membership_renewal = membership_renewal.rename(
    columns={0: "Not Renewed", 1: "Renewed"}
)

for col in ["Not Renewed", "Renewed"]:
    if col not in membership_renewal.columns:
        membership_renewal[col] = 0

membership_renewal = membership_renewal[["Not Renewed", "Renewed"]]

plot_bar(
    membership_renewal,
    "Membership Type vs Renewal",
    xlabel="Membership Type",
    ylabel="Number of Members")



st.subheader(" Classes Attended vs Membership Renewal")

max_classes = int(filtered_data["num_classes_attended"].max())

# Keep the 2-class interval idea from the notebook,
# but automatically cover the full range of the filtered data.
if max_classes < 2:
    class_bins = [0, 2]
else:
    class_bins = list(range(0, max_classes + 3, 2))

class_groups = pd.cut(
    filtered_data["num_classes_attended"],
    bins=class_bins,
    include_lowest=True
)

classes_renewal = pd.crosstab(
    class_groups,
    filtered_data["renewed_membership"]
)

classes_renewal = classes_renewal.rename(
    columns={0: "Not Renewed", 1: "Renewed"}
)

for col in ["Not Renewed", "Renewed"]:
    if col not in classes_renewal.columns:
        classes_renewal[col] = 0

classes_renewal = classes_renewal[["Not Renewed", "Renewed"]]

plot_bar(
    classes_renewal,
    "Classes Attended vs Membership Renewal",
    xlabel="Number of Classes Attended",
    ylabel="Number of Members",
    rotation=45,
    figsize=(10, 5)
)

col1, col2 = st.columns(2)

with col1:
    complaints = (
        filtered_data.groupby("renewed_membership")["num_complaints"]
        .sum()
    )
    complaints.index = [
        renewal_labels.get(x, str(x))
        for x in complaints.index
    ]

    plot_bar(
        complaints,
        "Total Complaints by Renewal Status",
        xlabel="Renewal Status",
        ylabel="Total Complaints"
    )

with col2:
    complaint_avg = (
        filtered_data.groupby("renewed_membership")["num_complaints"]
        .mean()
    )
    complaint_avg.index = [
        renewal_labels.get(x, str(x))
        for x in complaint_avg.index
    ]

    plot_bar(
        complaint_avg,
        "Average Complaints by Renewal Status",
        xlabel="Renewal Status",
        ylabel="Average Complaints"
    )