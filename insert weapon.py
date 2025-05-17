import psycopg2
import pandas as pd

# Koneksi ke database PostgreSQL
conn = psycopg2.connect(
    host="localhost",     
    port="port",
    dbname="data",
    user="user",
    password="password"
)
cursor = conn.cursor()

# Fungsi untuk memotong string jika terlalu panjang
def truncate_string(value, length):
    if isinstance(value, str) and len(value) > length:
        return value[:length]
    return value

# Fungsi untuk convert data ke integer atau None jika kosong
def safe_convert(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return None

# Fungsi untuk load data CSV ke tabel weapon
def load_csv_to_weapon(file):
    df = pd.read_csv(file)

    for index, row in df.iterrows():
        data = {
            'weaptype1': safe_convert(row.get('weaptype1')),
            'weaptype1_txt': truncate_string(row.get('weaptype1_txt'), 100),
            'weapsubtype1': safe_convert(row.get('weapsubtype1')),
            'weapsubtype1_txt': truncate_string(row.get('weapsubtype1_txt'), 100),
            'weaptype2': safe_convert(row.get('weaptype2')),
            'weaptype2_txt': truncate_string(row.get('weaptype2_txt'), 100),
            'weapsubtype2': safe_convert(row.get('weapsubtype2')),
            'weapsubtype2_txt': truncate_string(row.get('weapsubtype2_txt'), 100),
            'weaptype3': safe_convert(row.get('weaptype3')),
            'weaptype3_txt': truncate_string(row.get('weaptype3_txt'), 100),
            'weapsubtype3': safe_convert(row.get('weapsubtype3')),
            'weapsubtype3_txt': truncate_string(row.get('weapsubtype3_txt'), 100),
            'weaptype4': safe_convert(row.get('weaptype4')),
            'weaptype4_txt': truncate_string(row.get('weaptype4_txt'), 100),
            'weapsubtype4': safe_convert(row.get('weapsubtype4')),
            'weapsubtype4_txt': truncate_string(row.get('weapsubtype4_txt'), 100),
            'weapdetail': truncate_string(row.get('weapdetail'), 200)
        }

        try:
            cursor.execute("""
                INSERT INTO weapon (
                    weaptype1, weaptype1_txt, weapsubtype1, weapsubtype1_txt,
                    weaptype2, weaptype2_txt, weapsubtype2, weapsubtype2_txt,
                    weaptype3, weaptype3_txt, weapsubtype3, weapsubtype3_txt,
                    weaptype4, weaptype4_txt, weapsubtype4, weapsubtype4_txt, weapdetail
                ) VALUES (
                    %(weaptype1)s, %(weaptype1_txt)s, %(weapsubtype1)s, %(weapsubtype1_txt)s,
                    %(weaptype2)s, %(weaptype2_txt)s, %(weapsubtype2)s, %(weapsubtype2_txt)s,
                    %(weaptype3)s, %(weaptype3_txt)s, %(weapsubtype3)s, %(weapsubtype3_txt)s,
                    %(weaptype4)s, %(weaptype4_txt)s, %(weapsubtype4)s, %(weapsubtype4_txt)s, %(weapdetail)s
                )
            """, data)
        except Exception as e:
            print(f"Error inserting row: {e}")
            print(f"Problematic data: {data}")
            conn.rollback()

    conn.commit()
    print("✅ Data inserted into weapon")

file = 'terrorism_data.csv'  # Ganti dengan path file CSV yang sesuai
load_csv_to_weapon(file)

cursor.close()
conn.close()
