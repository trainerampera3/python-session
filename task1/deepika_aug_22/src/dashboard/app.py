import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path



st.set_page_config(
    page_title="Job Management Dashboard",
    page_icon="💼",
    layout="wide"
)



BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"



ai_jobs = pd.read_csv(
    DATA_DIR / "ai_jobs_market_2025_2026_cleaned.csv"
)

jobs = pd.read_csv(
    DATA_DIR / "job_dataset_cleaned.csv"
)

jobs["YearsOfExperience"] = pd.to_numeric(
    jobs["YearsOfExperience"],
    errors="coerce"
)

ds_salaries = pd.read_csv(
    DATA_DIR / "ds_salaries_cleaned.csv"
)

ds_salaries["salary_in_usd"] = pd.to_numeric(
    ds_salaries["salary_in_usd"],
    errors="coerce"
)


st.sidebar.title("💼 Job Filters")

page = st.sidebar.selectbox(
    "Select Dashboard",
    [
        "📊 Job Market Overview",
        "💼 Job Roles & Skills",
        "💰 Salary Analysis"
    ]
)


# DASHBOARD 1

if page == "📊 Job Market Overview":

    st.title("📊 Job Market Overview")

    st.write(
        "This dashboard provides an overview of the current AI job market "
        "using the AI Jobs dataset. It highlights job roles, experience "
        "levels, job categories, required skills, geographic distribution, "
        "and remote work trends."
    )

   

    st.sidebar.subheader("Job Market Filters")


    # EXPERIENCE FILTER

    experience_options = sorted(
        ai_jobs["experience_level"]
        .dropna()
        .unique()
    )

    selected_experience = st.sidebar.multiselect(
        "Experience Level",
        options=experience_options,
        default=experience_options
    )


    # CATEGORY FILTER

    category_options = sorted(
        ai_jobs["job_category"]
        .dropna()
        .unique()
    )

    selected_category = st.sidebar.multiselect(
        "Job Category",
        options=category_options,
        default=category_options
    )


    # COUNTRY FILTER

    country_options = sorted(
        ai_jobs["country"]
        .dropna()
        .unique()
    )

    selected_country = st.sidebar.multiselect(
        "Country",
        options=country_options,
        default=country_options
    )


    # CITY FILTER

    city_options = sorted(
        ai_jobs["city"]
        .dropna()
        .unique()
    )

    selected_city = st.sidebar.multiselect(
        "City",
        options=city_options,
        default=city_options
    )


    # FILTER DATA

    filtered_ai_jobs = ai_jobs[
        (
            ai_jobs["experience_level"].isin(
                selected_experience
            )
        )
        &
        (
            ai_jobs["job_category"].isin(
                selected_category
            )
        )
        &
        (
            ai_jobs["country"].isin(
                selected_country
            )
        )
        &
        (
            ai_jobs["city"].isin(
                selected_city
            )
        )
    ]



    total_jobs = filtered_ai_jobs["job_id"].nunique()

    total_roles = filtered_ai_jobs["job_title"].nunique()

    total_categories = filtered_ai_jobs["job_category"].nunique()

    total_experience_levels = (
        filtered_ai_jobs["experience_level"].nunique()
    )


   

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Jobs",
        total_jobs
    )

    col2.metric(
        "Job Roles",
        total_roles
    )

    col3.metric(
        "Job Categories",
        total_categories
    )

    col4.metric(
        "Experience Levels",
        total_experience_levels
    )


    st.divider()


    col1, col2 = st.columns(2)

    with col1:

        st.subheader("📊 Job Roles Distribution")

        job_roles = (
            filtered_ai_jobs["job_title"]
            .value_counts()
            .head(15)
            .reset_index()
        )

        job_roles.columns = [
            "Job Role",
            "Number of Jobs"
        ]

        fig = px.bar(
            job_roles,
            x="Job Role",
            y="Number of Jobs",
            title="Top 15 Job Roles"
        )

        fig.update_layout(
            xaxis_title="Job Role",
            yaxis_title="Number of Jobs"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

   

    with col2:

        st.subheader("📊 Experience Level Distribution")

        experience = (
            filtered_ai_jobs["experience_level"]
            .value_counts()
            .reset_index()
        )

        experience.columns = [
            "Experience Level",
            "Number of Jobs"
        ]

        fig = px.bar(
            experience,
            x="Experience Level",
            y="Number of Jobs",
            title="Jobs by Experience Level"
        )

        fig.update_layout(
            xaxis_title="Experience Level",
            yaxis_title="Number of Jobs"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )



    col1, col2 = st.columns(2)


    with col1:

        st.subheader("📂 Job Category Distribution")

        categories = (
            filtered_ai_jobs["job_category"]
            .dropna()
            .value_counts()
            .reset_index()
        )

        categories.columns = [
            "Job Category",
            "Number of Jobs"
        ]

        fig = px.bar(
            categories,
            x="Job Category",
            y="Number of Jobs",
            title="Jobs by Category"
        )

        fig.update_layout(
            xaxis_title="Job Category",
            yaxis_title="Number of Jobs"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )



    with col2:

        education_column = None

        for column in filtered_ai_jobs.columns:

            if column.lower().startswith("education"):

                education_column = column
                break


        if education_column:

            st.subheader("🎓 Education Level Distribution")

            education = (
                filtered_ai_jobs[education_column]
                .dropna()
                .value_counts()
                .reset_index()
            )

            education.columns = [
                "Education Level",
                "Number of Jobs"
            ]

            fig = px.bar(
                education,
                x="Education Level",
                y="Number of Jobs",
                title="Jobs by Education Level"
            )

            fig.update_layout(
                xaxis_title="Education Level",
                yaxis_title="Number of Jobs"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:

            st.info(
                "Education information is not available "
                "in this dataset."
            )



    # GEOGRAPHIC ANALYSIS

    st.divider()

    st.subheader("🌍 Geographic Analysis")

    col1, col2 = st.columns(2)



    with col1:

        st.subheader("🌍 Jobs by Country")

        jobs_by_country = (
            filtered_ai_jobs["country"]
            .dropna()
            .value_counts()
            .head(15)
            .reset_index()
        )

        jobs_by_country.columns = [
            "Country",
            "Number of Jobs"
        ]

        fig = px.bar(
            jobs_by_country,
            x="Country",
            y="Number of Jobs",
            title="Top 15 Countries by Jobs"
        )

        fig.update_layout(
            xaxis_title="Country",
            yaxis_title="Number of Jobs"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        st.subheader("🏙️ Jobs by City")

        jobs_by_city = (
            filtered_ai_jobs["city"]
            .dropna()
            .value_counts()
            .head(15)
            .reset_index()
        )

        jobs_by_city.columns = [
            "City",
            "Number of Jobs"
        ]

        fig = px.bar(
            jobs_by_city,
            x="City",
            y="Number of Jobs",
            title="Top 15 Cities by Jobs"
        )

        fig.update_layout(
            xaxis_title="City",
            yaxis_title="Number of Jobs"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )
  

    st.subheader("🏠 Remote Work Distribution")

    remote_work = (
        filtered_ai_jobs["remote_work"]
        .dropna()
        .value_counts()
        .reset_index()
    )

    remote_work.columns = [
        "Remote Work Type",
        "Number of Jobs"
    ]

    fig = px.pie(
        remote_work,
        names="Remote Work Type",
        values="Number of Jobs",
        title="Remote Work Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# DASHBOARD 2
# JOB ROLES & SKILLS


elif page == "💼 Job Roles & Skills":

    st.title("💼 Job Roles & Skills")

    st.write(
        "Detailed analysis of job roles, experience levels, "
        "skills, responsibilities, and keywords."
    )

    skill_data = (
        jobs["Skills"]
        .dropna()
        .astype(str)
        .str.split(",")
        .explode()
        .str.strip()
    )

    skill_data = skill_data[
        skill_data != ""
    ]


    responsibility_data = (
        jobs["Responsibilities"]
        .dropna()
        .astype(str)
        .str.split(",")
        .explode()
        .str.strip()
    )

    responsibility_data = responsibility_data[
        responsibility_data != ""
    ]



    keyword_data = (
        jobs["Keywords"]
        .dropna()
        .astype(str)
        .str.split(",")
        .explode()
        .str.strip()
    )

    keyword_data = keyword_data[
        keyword_data != ""
    ]

    total_job_records = jobs["JobID"].nunique()

    total_job_titles = jobs["Title"].nunique()

    total_experience = jobs["ExperienceLevel"].nunique()

    total_skills = skill_data.nunique()

  

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Job Postings",
        total_job_records
    )

    col2.metric(
        "Total Job Roles",
        total_job_titles
    )

    col3.metric(
        "Experience Levels",
        total_experience
    )

    col4.metric(
        "Total Skills",
        total_skills
    )


    st.divider()


    st.subheader("🔥 Top Job Roles by Demand")

    top_titles = (
        jobs["Title"]
        .value_counts()
        .head(15)
        .reset_index()
    )

    top_titles.columns = [
        "Job Role",
        "Number of Jobs"
    ]

    fig = px.bar(
        top_titles,
        x="Job Role",
        y="Number of Jobs",
        title="Top 15 Job Roles"
    )

    fig.update_layout(
        xaxis_title="Job Role",
        yaxis_title="Number of Jobs"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    col1, col2 = st.columns(2)


    with col1:

        st.subheader("📊 Jobs by Experience Level")

        experience_levels = (
            jobs["ExperienceLevel"]
            .value_counts()
            .reset_index()
        )

        experience_levels.columns = [
            "Experience Level",
            "Number of Jobs"
        ]

        fig = px.bar(
            experience_levels,
            x="Experience Level",
            y="Number of Jobs",
            title="Jobs by Experience Level"
        )

        fig.update_layout(
            xaxis_title="Experience Level",
            yaxis_title="Number of Jobs"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    with col2:

        st.subheader("📈 Jobs by Years of Experience")

        years_experience = (
            jobs["YearsOfExperience"]
            .dropna()
            .value_counts()
            .sort_index()
            .reset_index()
        )

        years_experience.columns = [
            "Years of Experience",
            "Number of Jobs"
        ]

        fig = px.bar(
            years_experience,
            x="Years of Experience",
            y="Number of Jobs",
            title="Jobs by Years of Experience"
        )

        fig.update_layout(
            xaxis_title="Years of Experience",
            yaxis_title="Number of Jobs"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    

    col1, col2 = st.columns(2)



    with col1:

        st.subheader("🔥 Most Required Skills")

        top_skills = (
            skill_data
            .value_counts()
            .head(15)
            .reset_index()
        )

        top_skills.columns = [
            "Skill",
            "Number of Jobs"
        ]

        fig = px.bar(
            top_skills,
            x="Skill",
            y="Number of Jobs",
            title="Top 15 Required Skills"
        )

        fig.update_layout(
            xaxis_title="Skill",
            yaxis_title="Number of Jobs"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    with col2:

        st.subheader("📋 Top Responsibilities")

        top_responsibilities = (
            responsibility_data
            .value_counts()
            .head(10)
            .reset_index()
        )

        top_responsibilities.columns = [
            "Responsibility",
            "Number of Jobs"
        ]

        fig = px.bar(
            top_responsibilities,
            x="Responsibility",
            y="Number of Jobs",
            title="Top 10 Responsibilities"
        )

        fig.update_layout(
            xaxis_title="Responsibility",
            yaxis_title="Number of Jobs"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )



    st.subheader("🔑 Most Common Job Keywords")

    top_keywords = (
        keyword_data
        .value_counts()
        .head(10)
        .reset_index()
    )

    top_keywords.columns = [
        "Keyword",
        "Number of Jobs"
    ]

    fig = px.bar(
        top_keywords,
        x="Keyword",
        y="Number of Jobs",
        title="Top 10 Job Keywords"
    )

    fig.update_layout(
        xaxis_title="Keyword",
        yaxis_title="Number of Jobs"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.divider()

    st.subheader("🔎 Job Role Analysis")

    selected_title = st.selectbox(
        "Select a Job Role",
        sorted(
            jobs["Title"]
            .dropna()
            .unique()
        )
    )


    filtered_jobs = jobs[
        jobs["Title"] == selected_title
    ]



    selected_job_count = len(filtered_jobs)

    selected_experience_levels = (
        filtered_jobs["ExperienceLevel"]
        .nunique()
    )

    selected_years = (
        pd.to_numeric(
            filtered_jobs["YearsOfExperience"],
            errors="coerce"
        )
        .mean()
    )


    if pd.isna(selected_years):

        selected_years = 0.0


    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Jobs for Selected Role",
        selected_job_count
    )

    col2.metric(
        "Experience Levels",
        selected_experience_levels
    )

    col3.metric(
        "Average Years of Experience",
        f"{selected_years:.1f}"
    )


    st.subheader(
        f"📋 Details for {selected_title}"
    )

    st.dataframe(
        filtered_jobs,
        use_container_width=True
    )


# DASHBOARD 3
# SALARY ANALYSIS

elif page == "💰 Salary Analysis":

    st.title("💰 Salary Analysis")

    st.write(
        "Analysis of salaries across data science "
        "and machine learning jobs."
    )


    salary_data = ds_salaries.dropna(
        subset=["salary_in_usd"]
    ).copy()

    salary_data["salary_in_usd"] = pd.to_numeric(
        salary_data["salary_in_usd"],
        errors="coerce"
    )

    salary_data = salary_data.dropna(
        subset=["salary_in_usd"]
    )


    average_salary = (
        salary_data["salary_in_usd"].mean()
    )

    maximum_salary = (
        salary_data["salary_in_usd"].max()
    )

    minimum_salary = (
        salary_data["salary_in_usd"].min()
    )

    total_salary_records = len(salary_data)



    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Average Salary",
        f"${average_salary:,.0f}"
    )

    col2.metric(
        "Maximum Salary",
        f"${maximum_salary:,.0f}"
    )

    col3.metric(
        "Minimum Salary",
        f"${minimum_salary:,.0f}"
    )

    col4.metric(
        "Salary Records",
        total_salary_records
    )


    st.divider()


    st.subheader("💰 Average Salary by Job Title")

    salary_by_job = (
        salary_data
        .groupby("job_title")["salary_in_usd"]
        .mean()
        .sort_values(ascending=False)
        .head(15)
        .reset_index()
    )

    salary_by_job.columns = [
        "Job Title",
        "Average Salary"
    ]

    fig = px.bar(
        salary_by_job,
        x="Job Title",
        y="Average Salary",
        title="Top 15 Job Titles by Average Salary"
    )

    fig.update_layout(
        xaxis_title="Job Title",
        yaxis_title="Average Salary (USD)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    col1, col2 = st.columns(2)



    with col1:

        st.subheader(
            "📊 Average Salary by Experience Level"
        )

        salary_by_experience = (
            salary_data
            .groupby("experience_level")["salary_in_usd"]
            .mean()
            .sort_values(ascending=False)
            .reset_index()
        )

        salary_by_experience.columns = [
            "Experience Level",
            "Average Salary"
        ]

        fig = px.bar(
            salary_by_experience,
            x="Experience Level",
            y="Average Salary",
            title="Average Salary by Experience"
        )

        fig.update_layout(
            xaxis_title="Experience Level",
            yaxis_title="Average Salary (USD)"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )



    with col2:

        st.subheader(
            "💼 Average Salary by Employment Type"
        )

        salary_by_employment = (
            salary_data
            .groupby("employment_type")["salary_in_usd"]
            .mean()
            .sort_values(ascending=False)
            .reset_index()
        )

        salary_by_employment.columns = [
            "Employment Type",
            "Average Salary"
        ]

        fig = px.bar(
            salary_by_employment,
            x="Employment Type",
            y="Average Salary",
            title="Average Salary by Employment Type"
        )

        fig.update_layout(
            xaxis_title="Employment Type",
            yaxis_title="Average Salary (USD)"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    if "work_year" in salary_data.columns:

        st.subheader("📈 Average Salary by Year")

        salary_by_year = (
            salary_data
            .groupby("work_year")["salary_in_usd"]
            .mean()
            .sort_index()
            .reset_index()
        )

        salary_by_year.columns = [
            "Year",
            "Average Salary"
        ]

        fig = px.line(
            salary_by_year,
            x="Year",
            y="Average Salary",
            markers=True,
            title="Average Salary by Year"
        )

        fig.update_layout(
            xaxis_title="Year",
            yaxis_title="Average Salary (USD)"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )



    st.divider()

    st.subheader("🔎 Salary by Selected Job")

    selected_job = st.selectbox(
        "Select Job Title",
        sorted(
            salary_data["job_title"]
            .dropna()
            .unique()
        )
    )


    selected_job_data = salary_data[
        salary_data["job_title"] == selected_job
    ]


    if len(selected_job_data) > 0:

        selected_average = (
            selected_job_data["salary_in_usd"].mean()
        )

        selected_maximum = (
            selected_job_data["salary_in_usd"].max()
        )

        selected_minimum = (
            selected_job_data["salary_in_usd"].min()
        )


        col1, col2, col3 = st.columns(3)


        col1.metric(
            "Average Salary",
            f"${selected_average:,.0f}"
        )

        col2.metric(
            "Maximum Salary",
            f"${selected_maximum:,.0f}"
        )

        col3.metric(
            "Minimum Salary",
            f"${selected_minimum:,.0f}"
        )


        st.dataframe(
            selected_job_data,
            use_container_width=True
        )