# Global Terrorism Database ETL Pipeline 🚀

## **Overview**
Proyek ini bertujuan untuk mengimplementasikan **ETL (Extract, Transform, Load)** menggunakan **Python** dengan **PostgreSQL**, berdasarkan data dari **Global Terrorism Database (GTD)**. Sebelumnya, model ini telah dikembangkan di **Google Cloud Platform**, tetapi dalam implementasi ini, database yang digunakan adalah **PostgreSQL**.

## **Alur Proyek**
### 🔹 **1. Extract (Ekstraksi Data)**  
Data sumber berupa **CSV** diekstrak dan dibersihkan sebelum dimasukkan ke database.

### 🔹 **2. Transform (Transformasi Data)**  
Data mengalami pembersihan dan normalisasi untuk memastikan akurasi dan konsistensi, termasuk format tanggal, pengisian nilai yang hilang, serta pemetaan atribut ke dalam struktur yang sesuai.

### 🔹 **3. Load (Pemuatan Data)**  
Setelah transformasi selesai, data dimasukkan ke PostgreSQL untuk digunakan dalam analisis lebih lanjut.

## **Struktur Database**  
Dataset ini telah dinormalisasi menjadi **7 tabel utama**:
- **Event**: Informasi lengkap tentang kejadian terorisme.
- **Attack**: Jenis serangan yang terjadi dalam suatu event.
- **Fatality**: Data mengenai korban tewas dan luka-luka.
- **Group**: Kelompok teroris yang bertanggung jawab atas serangan.
- **Target**: Sasaran serangan yang dilakukan oleh kelompok teroris.
- **Country**: Informasi lokasi serangan berdasarkan negara dan wilayah.
- **Weapon**: Jenis senjata yang digunakan dalam serangan.

## **File dalam Proyek**
| Nama File | Deskripsi |
|-----------|----------|
| `create_table.py` | Membuat tabel dalam PostgreSQL sesuai dengan skema database. |
| `insert_attack.py` | Memasukkan data ke tabel **attack**. |
| `insert_event.py` | Memasukkan data ke tabel **event**. |
| `insert_group.py` | Memasukkan data ke tabel **group**. |
| `insert_region_country.py` | Memasukkan data ke tabel **region** dan **country**. |
| `insert_target.py` | Memasukkan data ke tabel **target**. |
| `insert_weapon.py` | Memasukkan data ke tabel **weapon**. |
| `nginx.conf` | Konfigurasi untuk web service menggunakan Nginx. |
| `readme.md` | Dokumentasi proyek ini. |

## **Deployment & Eksekusi**
1. **Instal dependensi yang diperlukan** agar proyek berjalan dengan baik.  
2. **Buat tabel dalam PostgreSQL** menggunakan skrip yang telah disediakan.  
3. **Masukkan data ke dalam tabel PostgreSQL** secara bertahap sesuai kategori.  

## **Troubleshooting**
- Jika terjadi error dalam menghubungkan ke PostgreSQL, pastikan kredensial database sudah benar.  
- Jika `psycopg2` tidak dikenali oleh Python, gunakan `psycopg2-binary` sebagai alternatif.  
- Pastikan semua file CSV telah diproses dengan format yang sesuai sebelum dimasukkan ke dalam database.

---

Dokumentasi ini bisa diperluas sesuai kebutuhan. Jika ada informasi yang perlu ditambahkan atau diperbaiki, silakan sesuaikan! 🚀  
Semoga proyek ini berjalan lancar! 😊
