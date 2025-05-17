import psycopg2

# === CONFIGURE POSTGRESQL CONNECTION ===
conn = psycopg2.connect(
    host="localhost",#masukan host
    port="port", #masukan port
    dbname="data",#masukan dbname
    user="user",#masukan username
    password="password"#masukan password
)
cursor = conn.cursor()

# === CREATE TABLES ===
create_tables_sql = '''

-- Table: public.region
CREATE TABLE IF NOT EXISTS public.region (
    regionid SERIAL PRIMARY KEY,
    region VARCHAR(200) COLLATE pg_catalog."default"
);

-- Table: public.country
CREATE TABLE IF NOT EXISTS public.country (
    countryid SERIAL PRIMARY KEY,
    countrycode INTEGER,
    country VARCHAR(100) COLLATE pg_catalog."default",
    provstate VARCHAR(100) COLLATE pg_catalog."default",
    city VARCHAR(100) COLLATE pg_catalog."default",
    regionid INTEGER REFERENCES public.region(regionid)
);

CREATE TABLE IF NOT EXISTS public.attack
(
    attackid integer NOT NULL,
    attacktype character varying(50) COLLATE pg_catalog."default",
    CONSTRAINT attack_pkey PRIMARY KEY (attackid)
);

-- Table: public.target
CREATE TABLE IF NOT EXISTS public.target (
    targetid SERIAL PRIMARY KEY,
    targtype1 INTEGER,
    targtype1_txt TEXT COLLATE pg_catalog."default",
    targsubtype1 INTEGER,
    targsubtype1_txt TEXT COLLATE pg_catalog."default",
    corp1 TEXT COLLATE pg_catalog."default",
    target1 TEXT COLLATE pg_catalog."default",
    natlty1 INTEGER,
    natlty1_txt TEXT COLLATE pg_catalog."default",
    targtype2 INTEGER,
    targtype2_txt TEXT COLLATE pg_catalog."default",
    targsubtype2 INTEGER,
    targsubtype2_txt TEXT COLLATE pg_catalog."default",
    corp2 TEXT COLLATE pg_catalog."default",
    target2 TEXT COLLATE pg_catalog."default",
    natlty2 INTEGER,
    natlty2_txt TEXT COLLATE pg_catalog."default",
    targtype3 INTEGER,
    targtype3_txt TEXT COLLATE pg_catalog."default",
    targsubtype3 INTEGER,
    targsubtype3_txt TEXT COLLATE pg_catalog."default",
    corp3 TEXT COLLATE pg_catalog."default",
    target3 TEXT COLLATE pg_catalog."default",
    natlty3 INTEGER,
    natlty3_txt TEXT COLLATE pg_catalog."default",
    countryid INTEGER REFERENCES public.country(countryid),
    regionid INTEGER REFERENCES public.region(regionid)
);


-- Table: public."group"
CREATE TABLE IF NOT EXISTS public."group" (
    gid SERIAL PRIMARY KEY,
    gname VARCHAR(100) COLLATE pg_catalog."default",
    gsubname VARCHAR(100) COLLATE pg_catalog."default",
    gname2 VARCHAR(100) COLLATE pg_catalog."default",
    gsubname2 VARCHAR(100) COLLATE pg_catalog."default",
    gname3 VARCHAR(100) COLLATE pg_catalog."default",
    gsubname3 VARCHAR(100) COLLATE pg_catalog."default",
    motive TEXT COLLATE pg_catalog."default",
    guncertain1 INTEGER,
    guncertain2 INTEGER,
    guncertain3 INTEGER,
    individual INTEGER,
    nperps INTEGER,
    nperpcap INTEGER,
    claimed INTEGER,
    claimmode INTEGER,
    claimmode_txt VARCHAR(100) COLLATE pg_catalog."default",
    claim2 INTEGER,
    claimmode2 INTEGER,
    claimmode2_txt VARCHAR(100) COLLATE pg_catalog."default",
    claim3 INTEGER,
    claimmode3 INTEGER,
    claimmode3_txt VARCHAR(100) COLLATE pg_catalog."default",
    compclaim TEXT COLLATE pg_catalog."default"
);

-- Table: public.weapon
CREATE TABLE IF NOT EXISTS public.weapon (
    weaponid SERIAL PRIMARY KEY,
    weaptype1 INTEGER,
    weaptype1_txt VARCHAR(100) COLLATE pg_catalog."default",
    weapsubtype1 INTEGER,
    weapsubtype1_txt VARCHAR(100) COLLATE pg_catalog."default",
    weaptype2 INTEGER,
    weaptype2_txt VARCHAR(100) COLLATE pg_catalog."default",
    weapsubtype2 INTEGER,
    weapsubtype2_txt VARCHAR(100) COLLATE pg_catalog."default",
    weaptype3 INTEGER,
    weaptype3_txt VARCHAR(100) COLLATE pg_catalog."default",
    weapsubtype3 INTEGER,
    weapsubtype3_txt VARCHAR(100) COLLATE pg_catalog."default",
    weaptype4 INTEGER,
    weaptype4_txt VARCHAR(100) COLLATE pg_catalog."default",
    weapsubtype4 INTEGER,
    weapsubtype4_txt VARCHAR(100) COLLATE pg_catalog."default",
    weapdetail TEXT COLLATE pg_catalog."default"
);


-- Table: public.event
CREATE TABLE IF NOT EXISTS public.event (
    eventid SERIAL PRIMARY KEY,
    iyear integer,
    imonth integer,
    iday integer,
    location text COLLATE pg_catalog."default",
    summary text COLLATE pg_catalog."default",
    latitude real,
    longitude real,
    crit1 integer,
    crit2 integer,
    crit3 integer,
    addnotes text COLLATE pg_catalog."default",
    scite1 text COLLATE pg_catalog."default",
    scite2 text COLLATE pg_catalog."default",
    scite3 text COLLATE pg_catalog."default",
    dbsource text COLLATE pg_catalog."default",
    targetid integer,
    gid integer,
    weaponid integer,
    attackid integer,
    nkill BIGINT,
    nkillus INTEGER,
    nkillter INTEGER,
    nwound BIGINT,
    nwoundte INTEGER,
    property INTEGER,
    propextent INTEGER,
    propextent_txt VARCHAR(20) COLLATE pg_catalog."default",
    propvalue BIGINT,
    propcomment VARCHAR(15) COLLATE pg_catalog."default",
    ishostkid INTEGER,
    nhostkid INTEGER,
    nhostkidus INTEGER,
    nhours INTEGER,
    ndays INTEGER,
    divert VARCHAR(15) COLLATE pg_catalog."default",
    kidihijcountry VARCHAR(20) COLLATE pg_catalog."default",
    ransom INTEGER,
    ransomamt BIGINT,
    ransomamtus VARCHAR(20) COLLATE pg_catalog."default",
    ransompaid INTEGER,
    ransompaidus VARCHAR(20) COLLATE pg_catalog."default",
    ransomnote VARCHAR(100) COLLATE pg_catalog."default",
    hostkidoutcome INTEGER,
    hostkidoutcome_txt VARCHAR(20) COLLATE pg_catalog."default",
    nreleased INTEGER,
    regionid integer,  -- Add regionid column
    countryid integer,  -- Add countryid column
    CONSTRAINT event_attackid_fkey FOREIGN KEY (attackid)
        REFERENCES public.attack (attackid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT event_gid_fkey FOREIGN KEY (gid)
        REFERENCES public."group" (gid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT event_targetid_fkey FOREIGN KEY (targetid)
        REFERENCES public.target (targetid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT event_weaponid_fkey FOREIGN KEY (weaponid)
        REFERENCES public.weapon (weaponid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
);

-- Add constraints for regionid and countryid
ALTER TABLE public.event
ADD CONSTRAINT event_regionid_fkey FOREIGN KEY (regionid)
    REFERENCES public.region (regionid) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;

ALTER TABLE public.event
ADD CONSTRAINT event_countryid_fkey FOREIGN KEY (countryid)
    REFERENCES public.country (countryid) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


'''

# Execute the table creation
cursor.execute(create_tables_sql)
conn.commit()

print("✅ Tables have been successfully created!")

# Close connection
cursor.close()
conn.close()
