import sqlite3
import pandas as pd

CSV_PATH = "data/computrabajo.csv"
DB_PATH = "data/database.db"

def update_database():
    # GET DATA WE WANT TO STORE
    df = pd.read_csv(CSV_PATH)

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    # IF TABLE DOESNT EXIST
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS data_table (
            puesto TEXT,
            empresa TEXT,
            ubicacion TEXT,
            salario TEXT,
            contrato TEXT,
            jornada TEXT,
            modalidad TEXT,
            url TEXT
        )
    """)

    data_to_add = [tuple(row) for row in df.values.tolist()]

    # INSERT OR IGNORE -> if url already exists, do not add
    cursor.executemany("""
        INSERT OR IGNORE INTO data_table
        (puesto, empresa, ubicacion, salario, contrato, jornada, modalidad, url)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, data_to_add)

    conn.commit()

    conn.close()




def check_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Contar cuántos registros hay
    cursor.execute("SELECT COUNT(*) FROM data_table")
    total = cursor.fetchone()[0]
    print(f"Total de registros en la base: {total}")

    # Mostrar los primeros 5 registros
    cursor.execute("SELECT * FROM data_table LIMIT 5")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

    conn.close()
