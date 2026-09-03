import psycopg
from psycopg import sql


class Filter:

    def __init__(self):
        self.conn = psycopg.connect(
            host="localhost",
            port="5433",
            dbname="Hospital_database",
            user="shahir",
            password="shahir"
        )


    def load_data(self, table_name):
        with self.conn.cursor() as cursor:
            query = sql.SQL("SELECT * FROM {}").format(
                sql.Identifier(table_name)
            )

            cursor.execute(query)
            all_data = cursor.fetchall()

        return all_data
    
    def give_min_max_dates(self):
        with self.conn.cursor() as cursor:
            cursor.execute("""
                select min(admission_date) from patient_admissions;
            """)
            min_date=cursor.fetchone()[0]
            cursor.execute("""
                select max(admission_date) from patient_admissions;
            """)
            max_date=cursor.fetchone()[0]
        return min_date,max_date
    def admission_type(self):
        with self.conn.cursor() as cursor:
            cursor.execute("""
                select DISTINCT(admission_type) from patient_admissions;
            """)
            res= cursor.fetchall()
            lis=[]
            for row in res:
                lis.append(row[0])
            return lis
    def get_departments(self):
        with self.conn.cursor() as cursor:
            cursor.execute("""
            select department_name from departments;
            """)
            res=[]
            for row in cursor.fetchall():
                res.append(row[0])
            return res
    def get_disease(self):
        with self.conn.cursor() as cursor:
            cursor.execute("""
                select disease_name from diseases;
            """)
            res=[]
            for row in cursor.fetchall():
                res.append(row[0])
            return res
    def filter(self, start_date, end_date, admission, department_types, disease_types):
        with self.conn.cursor() as cursor:
            cursor.execute("""
            CREATE TEMP TABLE filtered_data AS
            SELECT *
            FROM patient_admissions
            WHERE admission_date BETWEEN %s AND %s
            AND admission_type = ANY(%s)
            AND department_id IN (
                SELECT department_id
                FROM departments
                WHERE department_name = ANY(%s)
            )
            AND disease_id IN (
                SELECT disease_id
                FROM diseases
                WHERE disease_name = ANY(%s)
            )
        """, (
            start_date,
            end_date,
            admission,
            department_types,
            disease_types
        ))

            self.conn.commit()
    def display(self):
        with self.conn.cursor() as cursor:
            cursor.execute("""
                select * from filtered_data
            
            """)
            return cursor.fetchmany(10)

    def get_patient_count(self):
        with self.conn.cursor() as cursor:
            cursor.execute("""

            select count(distinct(patient_id)) from filtered_data;

            """)
            return cursor.fetchone()[0]
    def get_admission_count(self):
        with self.conn.cursor() as cursor:
            cursor.execute("""
        
                        select count(admission_id) from filtered_data;        

                    """)
            return cursor.fetchone()[0]

    def get_avg_discharge_rate(self):
        with self.conn.cursor() as cursor:
            cursor.execute("""
        
                        select round(avg(discharge_date-admission_date ),2) from filtered_data;     

                    """)
            return cursor.fetchone()[0]
    def get_bed_count(self):
        with self.conn.cursor() as cursor:
            cursor.execute("""
        
                        select count(bed_id) from filtered_data;     

                    """)
            return cursor.fetchone()[0]
    def get_gender_count(self):
        with self.conn.cursor() as cursor:
            cursor.execute("""
                
                    select gender,count(*) from filtered_data group by gender;
                            """)
            labels = []             
            values = []
            for row in  cursor.fetchall():
                labels.append(row[0])
                values.append(row[1])
            return labels,values

    def get_admissions_by_time(self, time):
        with self.conn.cursor() as cursor:

            if time == "Day":
                cursor.execute("""
                SELECT admission_date, COUNT(*)
                FROM filtered_data
                GROUP BY admission_date
                ORDER BY admission_date;
            """)

            elif time == "Month":
                cursor.execute("""
                SELECT
                    DATE_TRUNC('month', admission_date)::date,
                    COUNT(*)
                FROM filtered_data
                GROUP BY DATE_TRUNC('month', admission_date)
                ORDER BY DATE_TRUNC('month', admission_date);
            """)

            else:
                cursor.execute("""
                SELECT
                    EXTRACT(YEAR FROM admission_date)::int,
                    COUNT(*)
                FROM filtered_data
                GROUP BY EXTRACT(YEAR FROM admission_date)
                ORDER BY EXTRACT(YEAR FROM admission_date);
            """)

            labels = []             
            values = []
            for row in  cursor.fetchall():
                labels.append(row[0])
                values.append(row[1])
            return labels,values

    def get_disease_frequency(self):
        with self.conn.cursor() as cursor:
            cursor.execute("""
            SELECT
                d.disease_name,
                COUNT(*) AS frequency
            FROM filtered_data fd
            JOIN diseases d
                ON fd.disease_id = d.disease_id
            GROUP BY d.disease_id, d.disease_name
            ORDER BY frequency DESC
            LIMIT 5;
        """)

            labels = []             
            values = []
            for row in  cursor.fetchall():
                labels.append(row[0])
                values.append(row[1])
            return labels,values
    def get_department_frequency(self):
        with self.conn.cursor() as cursor:
            cursor.execute("""
            SELECT
                (
                    SELECT department_name
                    FROM departments
                    WHERE department_id = fd.department_id
                ) AS department_name,
                COUNT(*) AS frequency
            FROM filtered_data fd
            GROUP BY fd.department_id
            ORDER BY frequency DESC
            LIMIT 5;
        """)

            labels = []             
            values = []
            for row in  cursor.fetchall():
                labels.append(row[0])
                values.append(row[1])
            return labels,values
    def get_drug_frequency(self):
        with self.conn.cursor() as cursor:
            cursor.execute("""
            SELECT
                d.drug_name,
                COUNT(*) AS frequency
            FROM filtered_data fd
            JOIN prescriptions p
                ON fd.admission_id = p.admission_id
            JOIN drugs d
                ON p.drug_id = d.drug_id
            GROUP BY d.drug_id, d.drug_name
            ORDER BY frequency DESC
            LIMIT 5;
        """)

            labels = []             
            values = []
            for row in  cursor.fetchall():
                labels.append(row[0])
                values.append(row[1])
            return labels,values