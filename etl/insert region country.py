import psycopg2
import pandas as pd

# === CONFIGURASI KONEKSI POSTGRES ===
conn = psycopg2.connect(
    host="localhost",#masukan host
    port="5432", #masukan port
    dbname="terrorism_data",#masukan dbname
    user="postgres",#masukan username
    password="vico123"#masukan password
)
cursor = conn.cursor()


# === 2. LOAD DATA FROM CSVs ===
# Asumsikan Anda punya file: country.csv, region.csv, attack.csv, target.csv, weapon.csv, group.csv, event.csv

def load_csv_to_table(file, table_name, column_mapping, drop_duplicates_col=None):
    df = pd.read_csv(file)

    # Rename columns based on mapping
    df = df.rename(columns=column_mapping)

    # Drop duplicates based on specified column
    if drop_duplicates_col:
        df = df.drop_duplicates(subset=[drop_duplicates_col])

    # Get mapped column names
    columns = list(column_mapping.values())

    tuples = [tuple(x.item() if hasattr(x, "item") else x for x in row) for row in df[columns].to_numpy()]

    # Prepare SQL query dynamically
    cols = ', '.join(columns)
    placeholders = ', '.join(['%s'] * len(columns))
    query = f"INSERT INTO {table_name} ({cols}) VALUES ({placeholders})"

    # Execute insert query
    cursor.executemany(query, tuples)
    conn.commit()

    print(f"✅ Data inserted into {table_name}")

# Region
file = "regions.csv"
column_mapping_region = {"region_name": "region"}
load_csv_to_table(file, "region", column_mapping_region)

# Country
file = "terrorism_data.csv"
column_mapping_country = {"country":"countrycode","country_txt": "country", "provstate": "provstate", "city": "city", "region": "regionid"}

# Load data to country
df_country = pd.read_csv(file)
df_country = df_country.rename(columns=column_mapping_country)
df_country = df_country.drop_duplicates(subset=["city"])

# Insert data to country table
for index, row in df_country.iterrows():
    cursor.execute("INSERT INTO public.country (countrycode, country, provstate, city, regionid) VALUES (%s, %s, %s, %s, %s)",
                   (row["countrycode"], row["country"], row["provstate"], row["city"], row["regionid"]))

conn.commit()
print("✅ Data inserted into country with regionid from CSV")


