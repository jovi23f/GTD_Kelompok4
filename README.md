# 🌍 Global Terrorism Async API

A scalable and asynchronous RESTful API for accessing Global Terrorism Data, built using **FastAPI**, **PostgreSQL**, and **asyncpg/databases**. This project is developed as part of a graduate-level assignment focused on building efficient data services using modern backend technologies. The modified databases can be downloaded in the database section.

---

## 📌 Features

- ✅ **Asynchronous** implementation using `asyncpg` + `databases`
- 📄 **Read-only RESTful API**
- 🔎 **Filtering** by year, country, region, group, weapon, etc.
- 🔁 **Sorting** (ascending/descending by any event column)
- 📦 **Pagination** for efficient data delivery
- 📚 **Swagger Documentation** at `/docs`
- 🔗 **JOIN** across 7 normalized tables

---

## 🚀 Tech Stack

| Layer          | Tools/Libraries              |
|----------------|------------------------------|
| API Framework  | FastAPI                      |
| Database       | PostgreSQL                   |
| Async Drivers  | asyncpg, databases           |
| ORM/SQL        | SQLAlchemy Core              |
| Load Testing   | Locust (suggested)           |
| Docs UI        | Swagger (OpenAPI 3.1)        |

---

## 🧑‍💻 Getting Started

### 1. Clone This Repository

```bash
git clone https://github.com/jovi23f/GTD_Kelompok4.git
cd GTD_Kelompok4
```

### 2. Install Dependencies

Create virtual env (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate (Windows)
pip install -r requirements.txt
```

### 3. Setup PostgreSQL Database

To load the dataset used in this project, restore the PostgreSQL database from the provided SQL dump:

```bash
createdb terrorism_db
psql -U postgres -d terrorism_db -f terrorism_db.sql
```

Ensure `database.py` or config matches:

```
DATABASE_URL=postgresql://ro_user:yourpassword@localhost:5432/terrorism_db
```

Ensure PostgreSQL is running and contains these tables:

- `event` — main terrorism incident data
- `country` — country reference table
- `region` — regional classification
- `group` — terrorist group info
- `target` — attack targets
- `weapon` — weapon types used
- `attack` — attack types

  
### 4. Setup PostgreSQL Read-Only User (Optional)

```sql
-- Login ke PostgreSQL
psql -U postgres

-- Buat user read-only
CREATE USER ro_user WITH PASSWORD 'yourpassword';

-- Beri hak akses hanya untuk baca
\c terrorism_db
GRANT CONNECT ON DATABASE terrorism_db TO ro_user;
GRANT USAGE ON SCHEMA public TO ro_user;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO ro_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO ro_user;
```

### 5. Run the API

```bash
uvicorn app.main:app --reload
```

Visit [http://localhost:8000/docs](http://localhost:8000/docs) to explore endpoints.

---


## 🔍 API Endpoints

### `GET /events`
Retrieve terrorism incident data with advanced filtering, sorting, and pagination.

**Filtering Parameters Supported:**

| Parameter       | Description                              |
|----------------|------------------------------------------|
| `iyear`         | Year of incident (int)                    |
| `imonth`        | Month (1–12)                              |
| `iday`          | Day (1–31)                                |
| `location`      | Location name                             |
| `crit1`, `crit2`, `crit3` | Attack criteria (boolean)        |
| `countryid`     | Country ID                                |
| `regionid`      | Region ID                                 |
| `group_name`    | Name of the terrorist group               |
| `targetid` / `target_name` | Target ID or name                |
| `weaponid` / `weapon_type`| Weapon ID or type                |
| `attackid` / `attacktype` | Attack ID or type                |
| `region_name`   | Region name (e.g., Southeast Asia)        |
| `country_name`  | Country name (e.g., Indonesia)            |

**Sorting**

| Parameter | Description                         |
|-----------|-------------------------------------|
| `sort_by` | Column name to sort (e.g. `iyear`)   |
| `order`   | `asc` for ascending, `desc` for descending |

**Example Query:**
```
/events?page=1&limit=10&region_name=South America&year=1995&group_name=FARC&sort_by=iyear&order=desc
```

### `GET /regions`
Returns list of all region IDs and names.

### `GET /countries`
Returns list of all countries (optionally filtered by `region_id`).

---

## 📂 Database Schema & Joins

Because the original database has a lot of data, we decided to modify it's structure a little bit by making several tables and some normalization in it's coloumn. You can access the Postgre backup file in the link below.

LINK: https://drive.google.com/file/d/1LWGHwfiORfwSKBmA6Ls43PxPIr1TzUAY/view?usp=sharing

This API joins data from 7 related tables:

| Table     | Description                        | Related Keys                                 |
|-----------|------------------------------------|----------------------------------------------|
| `event`   | Core terrorism incident data        | `countryid`, `regionid`, `gid`, `targetid`, `weaponid`, `attackid` |
| `country` | Country reference                   | `regionid` → `region.regionid`               |
| `region`  | World region names                  | —                                            |
| `group`   | Terrorist group information         | —                                            |
| `target`  | Target data of incidents            | —                                            |
| `weapon`  | Weapon types used                   | —                                            |
| `attack`  | Attack type categories              | —                                            |

---

## 📊 Sample Response

```json
[
{
  "status": "success",
  "message": "Events fetched successfully.",
  "page": 1,
  "total_pages": 243,
  "total_items": 1212,
  "data": [
    {
      "eventid": 79361,
      "iyear": 2006,
      "imonth": 1,
      "iday": 0,
      "location": "The rockets landed near Sederot in the Western Negev.",
      "hostkidoutcome_txt": "NaN",
      "nreleased": null,
      "regionid": 6,
      "countryid": 612
    }]
}
]
```

---

## 📊 Load Testing

Use tools like [Locust](https://locust.io/) to simulate concurrent access:

```bash
locust -f load_test.py
```

---

## 📒 License

This project is intended for academic purposes. For commercial use, please consult with the authors.

---

## 👩‍💼 Authors

-  NIKOLAUS VICO CRISTIANTO (5026211107)
-  I GUSTI MADE ARISUDANA (5026211188)
-  FIDELA JOVITA KANEDI (6026242016)

