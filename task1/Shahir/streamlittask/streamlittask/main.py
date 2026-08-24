import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


from utilities import gives_min_max_dates, department_changer,fillter,disease_type_changer,change_insurance_id
from count_data import get_patient_count,get_admission_count,get_bed_count,get_discharge_count,get_avg_discharge_rate


st.set_page_config(
    page_title="Hospital Dashboard",
    layout="wide"
)

st.title("Hospital Management Dashboard")


# Load data
patient_data = pd.read_csv(
    'data/patient_detials.csv'
)
patient_data=department_changer(patient_data)
patient_data=disease_type_changer(patient_data)


# Display data for testing
# Sidebar
st.sidebar.header("Filters")


# Date filter
min_date, max_date = gives_min_max_dates(patient_data)
end_date=min_date+pd.Timedelta(days=7)
start_date,end_date = st.sidebar.date_input(
    'Admission Date',
    (min_date, end_date),
    min_date,
    max_date,
    format='YYYY-MM-DD'
)


# Admission type
admission_type = st.sidebar.multiselect(
    'Admission Type',
    options=patient_data['admission_type'].unique(),
    default=patient_data['admission_type'].unique()
)


# Department
department_types = st.sidebar.multiselect(
    'Department Type',
    options=patient_data['department_id'].unique(),
    default=patient_data['department_id'].unique()
)


# Disease
disease_types = st.sidebar.multiselect(
    'Disease Type',
    options=patient_data['disease_id'].unique(),
    default=patient_data['disease_id'].unique()
)

time=st.sidebar.selectbox(
    'Timeline',
    options=['Day','Month','Year']
)
res=fillter(patient_data,start_date,end_date,admission_type,department_types,disease_types)


col1,col2,col3,col4=st.columns(4)
with col1:
    patient_count=get_patient_count(res)
    st.metric('Patient Count',patient_count)
with col2:
    admission_count=get_admission_count(res)
    st.metric('Admission Count',admission_count)

with col3:
    discharge_=get_avg_discharge_rate(res)
    st.metric('Avg Days to Discharge',discharge_)

with col4:
    bed_count=get_bed_count(res)
    st.metric('Bed Count',bed_count)
    
    
fig, ax = plt.subplots(1, 2, figsize=(12, 5))

count = res['gender'].value_counts()

ax[0].pie(
    count.values,
    labels=count.index,
    autopct='%1.1f%%'
)

ax[0].set_title("Gender Distribution")


if time == 'Day':
    data = res.groupby(
        res['admission_date'].dt.date
    ).size()

elif time == 'Month':
    data = res.groupby(
        res['admission_date'].dt.to_period('M')
    ).size()

else:
    data = res.groupby(
        res['admission_date'].dt.year
    ).size()

ax[1].plot(
    data.index.astype(str),
    data.values
)

ax[1].set_xlabel(time)
ax[1].set_ylabel('Admissions')
ax[1].set_title(f'Admissions by {time}')

plt.tight_layout()

st.pyplot(fig)

fig,ax=plt.subplots(1,2,figsize=(12,5))
ax[0].set_title('Most Diseases')
fre=res['disease_id'].value_counts()
ax[0].bar(fre.index,fre.values)
ax[0].set_xlabel('Diseases')
ax[0].set_ylabel('Frequncy')

ax[1].set_title('Departments')
fre=res['department_id'].value_counts()
ax[1].bar(fre.index,fre.values)
ax[1].set_xlabel('Department Name')
ax[1].set_ylabel('Frequncy')
st.pyplot(fig)


admission_ids=res['admission_id']
precription=pd.read_csv('data/prescription.csv')
drug=pd.read_csv('data/drug.csv')

result=pd.merge(precription,drug,on='drug_id',how='inner')

result=result[result['admission_id'].isin(admission_ids)]
drug_freq=result['drug_name'].value_counts().head(5)
fix,ax=plt.subplots()
fix.set_figheight(3)

ax.bar(drug_freq.index,drug_freq.values)
st.pyplot(fix)

patien_ids=res['patient_id']
insurance_=pd.read_csv('data/insurance.csv')
insurance_providers=pd.read_csv('data/insurance_provider.csv')
insurance=change_insurance_id(insurance_,insurance_providers)
result=insurance[insurance['patient_id'].isin(patien_ids)]
insurance_freq=result['insurance_provider_id'].value_counts().head(5)
fix,ax=plt.subplots()
fix.set_figheight(3)

ax.bar(insurance_freq.index,insurance_freq.values)
st.pyplot(fix)