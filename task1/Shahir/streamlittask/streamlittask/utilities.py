import pandas as pd


def gives_min_max_dates(data):

    data['admission_date'] = pd.to_datetime(
        data['admission_date'],
        format='%Y-%m-%d'
    )
    data['discharge_date']=pd.to_datetime(
        data['discharge_date'],
        format='%Y-%m-%d'
    )

    min_day = data['admission_date'].min().date()
    max_day = data['admission_date'].max().date()

    return min_day, max_day


def department_changer(dataframe):

    departments = {
        1: "Emergency",
        2: "Internal Medicine",
        3: "Surgery",
        4: "Pediatrics",
        5: "Orthopedics",
        6: "ICU",
        7: "Radiology",
        8: "Pathology",
        9: "Pharmacy",
        10: "Billing",
        11: "HR"
    }

    dataframe['department_id'] = dataframe['department_id'].map(departments)

    return dataframe
def fillter(
    dataframe,
    start_date,
    end_date,
    admission_type,
    department_types,
    disease_types
):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    res = dataframe.loc[
        (dataframe['admission_date'] >= start_date) &
        (dataframe['admission_date'] <= end_date) &
        (dataframe['admission_type'].isin(admission_type)) &
        (dataframe['department_id'].isin(department_types)) &
        (dataframe['disease_id'].isin(disease_types))
    ]
    return res
    
def disease_type_changer(dataframe):
    disease_dict = {
    1: "Acute Myocardial Infarction",
    2: "Stroke",
    3: "Road Traffic Accident",
    4: "Sepsis",
    5: "Acute Respiratory Distress",
    6: "Diabetes Mellitus",
    7: "Hypertension",
    8: "Chronic Kidney Disease",
    9: "Chronic Obstructive Pulmonary Disease",
    10: "Anemia",
    11: "Fracture Femur",
    12: "Appendicitis",
    13: "Gallstones",
    14: "Hernia",
    15: "Pneumonia",
    16: "Neonatal Jaundice",
    17: "Urinary Tract Infection",
    18: "Viral Fever",
    19: "COVID-19",
    20: "Tuberculosis"
}
    dataframe['disease_id']=dataframe['disease_id'].map(disease_dict)
    return dataframe

def change_insurance_id(insurance, insurance_provider):
    tracker = insurance_provider.set_index('insurance_provider_id')['provider_name']

    insurance['insurance_provider_id'] = (
        insurance['insurance_provider_id'].map(tracker)
    )

    return insurance