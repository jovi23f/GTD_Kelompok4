import psycopg2
import pandas as pd

# === CONFIGURASI KONEKSI POSTGRES ===
conn = psycopg2.connect(
    host="localhost",     # ganti sesuai host DB Anda
    port="5432",
    dbname="terrorism_data",
    user="postgres",
    password="vico123"
)
cursor = conn.cursor()


# === 2. LOAD DATA FROM CSV ===
file = 'terrorism_data.csv'

# Rename columns based on mapping and drop duplicates
def load_csv_to_table(file, table_name, column_mapping, subset_columns):
    df = pd.read_csv(file)
    df = df.rename(columns=column_mapping)
    df = df.drop_duplicates(subset=subset_columns)

    # Get mapped column names
    columns = list(column_mapping.values())
    tuples = [tuple(x) for x in df[columns].to_numpy()]

    # Prepare SQL query dynamically
    cols = ', '.join(columns)
    placeholders = ', '.join(['%s'] * len(columns))
    query = f"INSERT INTO {table_name} ({cols}) VALUES ({placeholders})"

    # Execute insert query
    cursor.executemany(query, tuples)
    conn.commit()

    print(f"✅ Data inserted into {table_name}")

# Attack data
column_mapping_attack = {
    'attacktype1': 'attackid',
    'attacktype1_txt': 'attacktype'
}
load_csv_to_table(file, 'attack', column_mapping_attack, ['attackid', 'attacktype'])



