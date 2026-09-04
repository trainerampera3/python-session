import psycopg
import pandas as pd
import time
import csv
from load_data import load_data_using_copy,load_data_using_insertions
conn = psycopg.connect(
    host="localhost",
    port="5433",
    dbname="Practice",
    user="shahir",
    password="shahir"
)


with conn.cursor() as cursor:
    cursor.execute("""
    
    CREATE TABLE if not exists hospital_patients (
    name VARCHAR(100),
    age INTEGER,
    gender VARCHAR(20),
    blood_type VARCHAR(5),
    medical_condition VARCHAR(100),
    date_of_admission DATE,
    doctor VARCHAR(150),
    hospital VARCHAR(200),
    insurance_provider VARCHAR(100),
    billing_amount NUMERIC(12, 2),
    room_number INTEGER,
    admission_type VARCHAR(50),
    discharge_date DATE,
    medication VARCHAR(100),
    test_results VARCHAR(50)
);
    
    """)
    conn.commit()

with conn.cursor() as cursor:
    cursor.execute("""
        CREATE OR REPLACE PROCEDURE datainsertion(
            p_name VARCHAR(100),
            p_age INTEGER,
            p_gender VARCHAR(20),
            p_blood_type VARCHAR(5),
            p_medical_condition VARCHAR(100),
            p_date_of_admission DATE,
            p_doctor VARCHAR(150),
            p_hospital VARCHAR(200),
            p_insurance_provider VARCHAR(100),
            p_billing_amount NUMERIC(12, 2),
            p_room_number INTEGER,
            p_admission_type VARCHAR(50),
            p_discharge_date DATE,
            p_medication VARCHAR(100),
            p_test_results VARCHAR(50)
        )
        LANGUAGE plpgsql
        AS $$
        BEGIN
            INSERT INTO hospital_patients (
                name,
                age,
                gender,
                blood_type,
                medical_condition,
                date_of_admission,
                doctor,
                hospital,
                insurance_provider,
                billing_amount,
                room_number,
                admission_type,
                discharge_date,
                medication,
                test_results
            )
            VALUES (
                p_name,
                p_age,
                p_gender,
                p_blood_type,
                p_medical_condition,
                p_date_of_admission,
                p_doctor,
                p_hospital,
                p_insurance_provider,
                p_billing_amount,
                p_room_number,
                p_admission_type,
                p_discharge_date,
                p_medication,
                p_test_results
            );
        END;
        $$;
    """)

    conn.commit()

start = time.perf_counter()
load_data_using_copy(conn,'cleaned_data.csv')
end = time.perf_counter()

print("COPY time:", end - start)

'''
start = time.perf_counter()
load_data_using_insertions(conn,'cleaned_data.csv')
end = time.perf_counter()

print("COPY time:", end - start)

'''
