import psycopg
import pandas as pd

conn=psycopg.connect(
    host='localhost',
    port='5433',
    dbname='Hospital_database',
    user='shahir',
    password='shahir'
)


with conn.cursor() as cursor:

    cursor.execute("""
        select * from beds limit 10;
    """)
    rows=cursor.fetchall()
    cursor.execute("""
select * from beds where bed_status='Available' limit 5
    """)
    rows=cursor.fetchall()
    cursor.execute("""
        select * from patient_admissions where admission_type='Emergency' limit 20
    """)
    rows=cursor.fetchall()
    cursor.execute("""
        select count(*) from patient_admissions group by gender
    """)
    result=cursor.fetchall()
    cursor.execute("""
       select p.*,a.department_name as department_ from patient_admissions as p join departments as a on p.department_id=a.department_id limit 5
    """)
    result=cursor.fetchall()
