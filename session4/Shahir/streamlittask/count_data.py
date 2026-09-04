import pandas as pd
def get_patient_count(cleaned_dataframe):
    return cleaned_dataframe['patient_id'].nunique()

def get_admission_count(cleaned_dataframe):
    return cleaned_dataframe['admission_id'].nunique()

def get_bed_count(cleaned_dataframe):
    return cleaned_dataframe['bed_id'].nunique()


def get_discharge_count(cleaned_dataframe):
    discharge_data=cleaned_dataframe[cleaned_dataframe['admission_status']=='Discharged']
    return discharge_data['patient_id'].nunique()
def get_avg_discharge_rate(cleaned_dataframe):

    difference = (
        cleaned_dataframe['discharge_date']
        - cleaned_dataframe['admission_date']
    )

    return round(difference.dt.days.mean(),2)