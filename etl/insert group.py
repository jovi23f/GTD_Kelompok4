import psycopg2
import pandas as pd

# Koneksi ke database PostgreSQL
conn = psycopg2.connect(
    host="localhost",#masukan host
    port="5432", #masukan port
    dbname="terrorism_data",#masukan dbname
    user="postgres",#masukan username
    password="vico123"#masukan password
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

# Fungsi untuk load data CSV ke tabel group
def load_csv_to_group(file):
    df = pd.read_csv(file)

    for index, row in df.iterrows():
        data = {
            'gname': truncate_string(row.get('gname'), 100),
            'gsubname': truncate_string(row.get('gsubname'), 100),
            'gname2': truncate_string(row.get('gname2'), 100),
            'gsubname2': truncate_string(row.get('gsubname2'), 100),
            'gname3': truncate_string(row.get('gname3'), 100),
            'gsubname3': truncate_string(row.get('gsubname3'), 100),
            'motive': truncate_string(row.get('motive'), 100),
            'guncertain1': safe_convert(row.get('guncertain1')),
            'guncertain2': safe_convert(row.get('guncertain2')),
            'guncertain3': safe_convert(row.get('guncertain3')),
            'individual': safe_convert(row.get('individual')),
            'nperps': safe_convert(row.get('nperps')),
            'nperpcap': safe_convert(row.get('nperpcap')),
            'claimed': safe_convert(row.get('claimed')),
            'claimmode': safe_convert(row.get('claimmode')),
            'claimmode_txt': truncate_string(row.get('claimmode_txt'), 100),
            'claim2': safe_convert(row.get('claim2')),
            'claimmode2': safe_convert(row.get('claimmode2')),
            'claimmode2_txt': truncate_string(row.get('claimmode2_txt'), 100),
            'claim3': safe_convert(row.get('claim3')),
            'claimmode3': safe_convert(row.get('claimmode3')),
            'claimmode3_txt': truncate_string(row.get('claimmode3_txt'), 100),
            'compclaim': truncate_string(row.get('compclaim'), 100)
        }

        try:
            cursor.execute("""
                INSERT INTO "group" (
                    gname, gsubname, gname2, gsubname2, gname3, gsubname3, motive,
                    guncertain1, guncertain2, guncertain3, individual, nperps,
                    nperpcap, claimed, claimmode, claimmode_txt, claim2, claimmode2,
                    claimmode2_txt, claim3, claimmode3, claimmode3_txt, compclaim
                ) VALUES (
                    %(gname)s, %(gsubname)s, %(gname2)s, %(gsubname2)s, %(gname3)s,
                    %(gsubname3)s, %(motive)s, %(guncertain1)s, %(guncertain2)s,
                    %(guncertain3)s, %(individual)s, %(nperps)s, %(nperpcap)s,
                    %(claimed)s, %(claimmode)s, %(claimmode_txt)s, %(claim2)s,
                    %(claimmode2)s, %(claimmode2_txt)s, %(claim3)s, %(claimmode3)s,
                    %(claimmode3_txt)s, %(compclaim)s
                )
            """, data)
        except Exception as e:
            print(f"Error inserting row: {e}")
            print(f"Problematic data: {data}")
            conn.rollback()

    conn.commit()
    print("✅ Data inserted into group")

file = 'terrorism_data.csv'
load_csv_to_group(file)

cursor.close()
conn.close()
