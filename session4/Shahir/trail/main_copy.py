import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import timedelta

from utilities import Filter
from count_data import get_patient_count,get_admission_count,get_bed_count,get_discharge_count,get_avg_discharge_rate

database=Filter()

st.set_page_config(
    page_title="Hospital Dashboard",
    layout="wide"
)

st.title("Hospital Management Dashboard")


# Load data
patien_data=database.load_data('patient_admissions')





# Display data for testing
# Sidebar
st.sidebar.header("Filters")


# Date filter
min_date, max_date = database.give_min_max_dates()
end_date=min_date+timedelta(days=7)
start_date,end_date = st.sidebar.date_input(
    'Admission Date',
    (min_date, end_date),
    min_date,
    max_date,
    format='YYYY-MM-DD'
)
admission_types=database.admission_type()


# Admission type
admission_type = st.sidebar.multiselect(
    'Admission Type',
    options=admission_types,
    default=admission_types
)
departments=database.get_departments()


# Department
department_types = st.sidebar.multiselect(
    'Department Type',
    options=departments,
    default=departments
)

d=database.get_disease()
# Disease
disease_types = st.sidebar.multiselect(
    'Disease Type',
    options=d,
    default=d
)


time=st.sidebar.selectbox(
    'Timeline',
    options=['Day','Month','Year']
)


res=database.filter(start_date,end_date,admission_type,department_types,disease_types)
patient_count=database.get_patient_count()

col1,col2,col3,col4=st.columns(4)
with col1:
    patient_count=database.get_patient_count()
    st.metric('Patient Count',patient_count)
with col2:
    admission_count=database.get_admission_count()
    st.metric('Admission Count',admission_count)

with col3:
    discharge_=database.get_avg_discharge_rate()
    st.metric('Avg Days to Discharge',discharge_)

with col4:
    bed_count=database.get_bed_count()
    st.metric('Bed Count',bed_count)

labels,values=database.get_gender_count()
fig, ax = plt.subplots(1, 2, figsize=(12, 5))


ax[0].pie(
    values,
    labels=labels,
    autopct='%1.1f%%'
)

ax[0].set_title("Gender Distribution")



labels,values=database.get_admissions_by_time(time=time)

ax[1].plot(
    labels,
    values
)

ax[1].set_xlabel(time)
ax[1].set_ylabel('Admissions')
ax[1].set_title(f'Admissions by {time}')

plt.tight_layout()

st.pyplot(fig)


fig,ax=plt.subplots(1,2,figsize=(12,5))
ax[0].set_title('Most Diseases')
labels,values=database.get_disease_frequency()
ax[0].bar(labels,values)
ax[0].set_xlabel('Diseases')
ax[0].set_ylabel('Frequncy')

ax[1].set_title('Departments')
labels,values=database.get_department_frequency()
ax[1].bar(labels,values)
ax[1].set_xlabel('Department Name')
ax[1].set_ylabel('Frequncy')
st.pyplot(fig)

labels,values=database.get_drug_frequency()

fix,ax=plt.subplots()
fix.set_figheight(3)

ax.bar(labels,values)
st.pyplot(fix)

