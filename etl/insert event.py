import psycopg2
import pandas as pd

# Koneksi ke database PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    port="5432",
    dbname="terrorism_data",
    user="postgres",
    password="vico123"
)
cursor = conn.cursor()

# Fungsi bantu
def safe_convert(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return None

def truncate_string(value, length):
    if isinstance(value, str) and len(value) > length:
        return value[:length]
    return value

# Buat mapping dari attacktype1_txt ke attackid
cursor.execute("SELECT attackid, attacktype FROM attack")
attack_mapping = {row[1]: row[0] for row in cursor.fetchall()}

# Fungsi untuk load data ke event
def load_csv_to_event(file):
    df = pd.read_csv(file)

    for index, row in df.iterrows():
        row_number = index + 1

        # targetid, gid, weaponid semua diurutkan dari 1
        targetid = row_number
        gid = row_number
        weaponid = row_number

        # Ambil regionid dan countryid dari tabel target berdasarkan targetid (yang sekarang urut)
        regionid, countryid = None, None
        cursor.execute("SELECT regionid, countryid FROM target WHERE targetid = %s", (targetid,))
        result = cursor.fetchone()
        if result:
            regionid, countryid = result

        # Mapping attackid dari attacktype1_txt
        attacktype_txt = row.get('attacktype1_txt')
        attackid = attack_mapping.get(attacktype_txt)

        data = {
            # Event core
            'iyear': safe_convert(row.get('iyear')),
            'imonth': safe_convert(row.get('imonth')),
            'iday': safe_convert(row.get('iday')),
            'location': row.get('location'),
            'summary': row.get('summary'),
            'latitude': row.get('latitude'),
            'longitude': row.get('longitude'),
            'crit1': safe_convert(row.get('crit1')),
            'crit2': safe_convert(row.get('crit2')),
            'crit3': safe_convert(row.get('crit3')),
            'addnotes': row.get('addnotes'),
            'scite1': row.get('scite1'),
            'scite2': row.get('scite2'),
            'scite3': row.get('scite3'),
            'dbsource': row.get('dbsource'),

            # Foreign keys
            'targetid': targetid,
            'gid': gid,
            'weaponid': weaponid,
            'attackid': attackid,
            'regionid': regionid,
            'countryid': countryid,

            # Fatality fields
            'nkill': safe_convert(row.get('nkill')),
            'nkillus': safe_convert(row.get('nkillus')),
            'nkillter': safe_convert(row.get('nkillter')),
            'nwound': safe_convert(row.get('nwound')),
            'nwoundte': safe_convert(row.get('nwoundte')),
            'property': safe_convert(row.get('property')),
            'propextent': safe_convert(row.get('propextent')),
            'propextent_txt': truncate_string(row.get('propextent_txt'), 20),
            'propvalue': safe_convert(row.get('propvalue')),
            'propcomment': truncate_string(row.get('propcomment'), 15),
            'ishostkid': safe_convert(row.get('ishostkid')),
            'nhostkid': safe_convert(row.get('nhostkid')),
            'nhostkidus': safe_convert(row.get('nhostkidus')),
            'nhours': safe_convert(row.get('nhours')),
            'ndays': safe_convert(row.get('ndays')),
            'divert': truncate_string(row.get('divert'), 15),
            'kidihijcountry': truncate_string(row.get('kidihijcountry'), 20),
            'ransom': safe_convert(row.get('ransom')),
            'ransomamt': safe_convert(row.get('ransomamt')),
            'ransomamtus': truncate_string(row.get('ransomamtus'), 20),
            'ransompaid': safe_convert(row.get('ransompaid')),
            'ransompaidus': truncate_string(row.get('ransompaidus'), 20),
            'ransomnote': truncate_string(row.get('ransomnote'), 100),
            'hostkidoutcome': safe_convert(row.get('hostkidoutcome')),
            'hostkidoutcome_txt': truncate_string(row.get('hostkidoutcome_txt'), 20),
            'nreleased': safe_convert(row.get('nreleased')),
        }

        try:
            cursor.execute("""
                INSERT INTO event (
                    iyear, imonth, iday, location, summary, latitude, longitude,
                    crit1, crit2, crit3, addnotes, scite1, scite2, scite3, dbsource,
                    targetid, gid, weaponid, attackid,
                    regionid, countryid,
                    nkill, nkillus, nkillter, nwound, nwoundte,
                    property, propextent, propextent_txt, propvalue, propcomment,
                    ishostkid, nhostkid, nhostkidus, nhours, ndays, divert,
                    kidihijcountry, ransom, ransomamt, ransomamtus, ransompaid,
                    ransompaidus, ransomnote, hostkidoutcome, hostkidoutcome_txt, nreleased
                ) VALUES (
                    %(iyear)s, %(imonth)s, %(iday)s, %(location)s, %(summary)s, %(latitude)s, %(longitude)s,
                    %(crit1)s, %(crit2)s, %(crit3)s, %(addnotes)s, %(scite1)s, %(scite2)s, %(scite3)s, %(dbsource)s,
                    %(targetid)s, %(gid)s, %(weaponid)s, %(attackid)s,
                    %(regionid)s, %(countryid)s,
                    %(nkill)s, %(nkillus)s, %(nkillter)s, %(nwound)s, %(nwoundte)s,
                    %(property)s, %(propextent)s, %(propextent_txt)s, %(propvalue)s, %(propcomment)s,
                    %(ishostkid)s, %(nhostkid)s, %(nhostkidus)s, %(nhours)s, %(ndays)s, %(divert)s,
                    %(kidihijcountry)s, %(ransom)s, %(ransomamt)s, %(ransomamtus)s, %(ransompaid)s,
                    %(ransompaidus)s, %(ransomnote)s, %(hostkidoutcome)s, %(hostkidoutcome_txt)s, %(nreleased)s
                )
            """, data)
        except Exception as e:
            print(f"❌ Error inserting row: {e}")
            print(f"⚠️ Data bermasalah: {data}")
            conn.rollback()

    conn.commit()
    print("✅ Semua data berhasil dimasukkan ke tabel event.")

# Jalankan
file = 'terrorism_data.csv'
load_csv_to_event(file)

cursor.close()
conn.close()
