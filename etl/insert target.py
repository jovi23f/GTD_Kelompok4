import psycopg2
import pandas as pd

# Database connection
conn = psycopg2.connect(
    host="localhost",
    port="5432",
    dbname="terrorism_data",
    user="postgres",
    password="vico123"
)
cursor = conn.cursor()

def safe_convert(val):
    try:
        return int(val)
    except (ValueError, TypeError):
        return None

def get_region_cache():
    """Preload region data into dictionary."""
    cursor.execute("SELECT regionid, region FROM region")
    return {region: regionid for regionid, region in cursor.fetchall()}

def get_country_cache():
    """Preload country data into dictionary."""
    cursor.execute("SELECT countryid, country, provstate, city, regionid FROM country")
    return {
        (country, provstate, city, regionid): countryid
        for countryid, country, provstate, city, regionid in cursor.fetchall()
    }

def insert_new_country(rows):
    """Insert new countries individually and return updated cache."""
    query = """
        INSERT INTO country (countrycode, country, provstate, city, regionid)
        VALUES (NULL, %s, %s, %s, %s)
        RETURNING countryid, country, provstate, city, regionid
    """
    new_entries = {}
    for row in rows:
        try:
            cursor.execute(query, row)
            res = cursor.fetchone()
            if res:
                countryid, country, provstate, city, regionid = res
                new_entries[(country, provstate, city, regionid)] = countryid
        except Exception as e:
            print(f"❌ Failed to insert country {row}: {e}")
            conn.rollback()
    conn.commit()
    return new_entries

def load_csv_to_target(file):
    try:
        df = pd.read_csv(file, low_memory=False).drop_duplicates()
        region_map = get_region_cache()
        country_map = get_country_cache()

        new_country_rows = set()
        data_to_insert = []

        for _, row in df.iterrows():
            region = row.get('region_txt')
            regionid = region_map.get(region)
            if regionid is None:
                continue  # Skip if region not found

            country_key = (row.get('country_txt'), row.get('provstate'), row.get('city'), regionid)
            countryid = country_map.get(country_key)

            if countryid is None:
                new_country_rows.add(country_key)
                continue  # Delay insertion

            data = (
                safe_convert(row.get('targtype1')),
                row.get('targtype1_txt'),
                safe_convert(row.get('targsubtype1')),
                row.get('targsubtype1_txt'),
                row.get('corp1'),
                row.get('target1'),
                safe_convert(row.get('natlty1')),
                row.get('natlty1_txt'),
                safe_convert(row.get('targtype2')),
                row.get('targtype2_txt'),
                safe_convert(row.get('targsubtype2')),
                row.get('targsubtype2_txt'),
                row.get('corp2'),
                row.get('target2'),
                safe_convert(row.get('natlty2')),
                row.get('natlty2_txt'),
                safe_convert(row.get('targtype3')),
                row.get('targtype3_txt'),
                safe_convert(row.get('targsubtype3')),
                row.get('targsubtype3_txt'),
                row.get('corp3'),
                row.get('target3'),
                safe_convert(row.get('natlty3')),
                row.get('natlty3_txt'),
                countryid,
                regionid
            )
            data_to_insert.append(data)

        # Insert new countries
        if new_country_rows:
            new_country_map = insert_new_country(list(new_country_rows))
            country_map.update(new_country_map)

        # Second pass for delayed rows
        for _, row in df.iterrows():
            region = row.get('region_txt')
            regionid = region_map.get(region)
            if regionid is None:
                continue

            country_key = (row.get('country_txt'), row.get('provstate'), row.get('city'), regionid)
            countryid = country_map.get(country_key)
            if countryid is None:
                continue

            data = (
                safe_convert(row.get('targtype1')),
                row.get('targtype1_txt'),
                safe_convert(row.get('targsubtype1')),
                row.get('targsubtype1_txt'),
                row.get('corp1'),
                row.get('target1'),
                safe_convert(row.get('natlty1')),
                row.get('natlty1_txt'),
                safe_convert(row.get('targtype2')),
                row.get('targtype2_txt'),
                safe_convert(row.get('targsubtype2')),
                row.get('targsubtype2_txt'),
                row.get('corp2'),
                row.get('target2'),
                safe_convert(row.get('natlty2')),
                row.get('natlty2_txt'),
                safe_convert(row.get('targtype3')),
                row.get('targtype3_txt'),
                safe_convert(row.get('targsubtype3')),
                row.get('targsubtype3_txt'),
                row.get('corp3'),
                row.get('target3'),
                safe_convert(row.get('natlty3')),
                row.get('natlty3_txt'),
                countryid,
                regionid
            )
            data_to_insert.append(data)

        # Final insert
        insert_query = """
            INSERT INTO target (
                targtype1, targtype1_txt, targsubtype1, targsubtype1_txt,
                corp1, target1, natlty1, natlty1_txt,
                targtype2, targtype2_txt, targsubtype2, targsubtype2_txt,
                corp2, target2, natlty2, natlty2_txt,
                targtype3, targtype3_txt, targsubtype3, targsubtype3_txt,
                corp3, target3, natlty3, natlty3_txt,
                countryid, regionid
            ) VALUES (
                %s, %s, %s, %s,
                %s, %s, %s, %s,
                %s, %s, %s, %s,
                %s, %s, %s, %s,
                %s, %s, %s, %s,
                %s, %s, %s, %s,
                %s, %s
            )
        """
        cursor.executemany(insert_query, data_to_insert)
        conn.commit()
        print("✅ Data successfully inserted into 'target' table.")

    except Exception as e:
        print(f"❌ Error during processing: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

# Run
file = 'terrorism_data.csv'
load_csv_to_target(file)
