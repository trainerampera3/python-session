import pandas as pd
import csv

def load_data_using_copy(conn, file_path):
    data = pd.read_csv(file_path)


    with conn.cursor() as cur:
        
        with cur.copy(f"""
            COPY hospital_patients
            FROM STDIN
        """) as copy:

            for row in data.itertuples(
                index=False,
                name=None
            ):
                copy.write_row(row)

        conn.commit()

def load_data_using_insertions(conn, file_path):
    with conn.cursor() as cursor:
        with open(file_path, "r") as file:
            reader = csv.reader(file)
            next(reader)

            res = []
            batch_size = 100

            for row in reader:
                res.append(row)

                if len(res) == batch_size:
                    cursor.executemany("""
                        CALL datainsertion(
                            %s, %s, %s, %s, %s,
                            %s, %s, %s, %s, %s,
                            %s, %s, %s, %s, %s
                        )
                    """, res)

                    conn.commit()
                    res = []

            if res:
                cursor.executemany("""
                    CALL datainsertion(
                        %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s
                    )
                """, res)

                conn.commit()