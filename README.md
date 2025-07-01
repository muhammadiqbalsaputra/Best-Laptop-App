# 💻 SPK Laptop – Flask + Weighted Product Decision Support System

Sistem Pendukung Keputusan (SPK) berbasis web untuk membantu mahasiswa memilih **laptop terbaik** menggunakan metode **Weighted Product (WP)**.  
Aplikasi dikembangkan dengan **Python Flask**, **MySQL/MariaDB**, dan **Tailwind CSS**.

---

## 🚀 Fitur

- **CRUD Kriteria** & pembobotan skala 1‑5  
- **CRUD Alternatif** (laptop) + skor tiap kriteria (input serentak)  
- Tabel skor lengkap, hapus skor individu, hapus alternatif  
- **Perhitungan Weighted Product** otomatis (benefit & cost)  
- Halaman rangking: nilai V, highlight juara, animasi pulse  
- Responsive UI dengan Tailwind – dark‑mode‑friendly

---

## 🗂 Struktur Direktori (ringkas)

```
spk_laptop/
│
├─ main.py # Flask routes & WP logic
├─ DBConnection.py # helper koneksi PyMySQL
├─ requirements.txt
├─ spk_laptop_full.sql # schema & contoh data
│
├─ templates/
│ ├─ layout.html
│ ├─ _header.html
│ ├─ _footer.html
│ ├─ dashboard.html
│ ├─ kriteria.html # list + modal add
│ ├─ kriteria_add.html # halaman add
│ ├─ kriteria_edit.html
│ ├─ alternatif.html
│ ├─ alternatif_add.html
│ ├─ skor.html
│ └─ rangking.html
│
└─ static/ # (opsional) hasil build Tailwind / JS custom
```

---

## ⚙️ Instalasi Cepat

```
# 1. klon / salin repo
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt  # Flask, PyMySQL

# 2. buat database
mysql -u root -p -e "CREATE DATABASE spk_laptop"

# 3. import schema
mysql -u root -p spk_laptop < spk_laptop_full.sql

# 4. jalankan aplikasi
python main.py
# buka http://localhost:5000
```

Gunakan variabel lingkungan untuk koneksi jika perlu:
```
export DB_USER=root
export DB_PASS=yourpassword
```

##🧮 Daftar Kriteria & Konversi Nilai

```
|  ID | Kriteria               | Unit Asli / Skala | **Skor disimpan**            | Konversi & Catatan                      |
| :-: | ---------------------- | ----------------- | ---------------------------- | --------------------------------------- |
|  1  | **Processor**          | Subjektif         | 1 – 10                       | Semakin tinggi semakin baik *(benefit)* |
|  2  | **Penyimpanan**        | GB                | 128 – 2048+                  | Nilai langsung GB *(benefit)*           |
|  3  | **Jenis Penyimpanan**  | HDD/Hybrid/SSD    | 1 = HDD, 2 = Hybrid, 3 = SSD | Mapping *(benefit)*                     |
|  4  | **Tahun Rilis**        | Tahun             | 2020+                        | Semakin baru semakin baik *(benefit)*   |
|  5  | **Harga**              | Skala 1‑10        | 1 = Murah … 10 = Mahal       | **Cost** → pangkat negatif              |
|  6  | **Daya Tahan Baterai** | Jam               | 3 – 15                       | Nilai langsung *(benefit)*              |
|  7  | **Ukuran Layar**       | Inch              | 13 – 17                      | Nilai langsung *(benefit)*              |
|  8  | **Berat**              | kg                | 0.9 – 3.0                    | **Cost** *(lebih ringan lebih baik)*    |
|  9  | **Fitur Tambahan**     | Subjektif         | 1 = Minim … 3 = Lengkap      | Mapping *(benefit)*                     |
```

## 🔢 Rumus Weighted Product
```
S_i = ∏ (x_ij) ^ w_j        (benefit)
      ∏ (x_ij) ^ -w_j       (cost)

V_i = S_i / ΣS_k
```
x_ij → skor alternatif i pada kriteria j

w_j → bobot (dinormalisasi Σw = 1)

Peringkat ditentukan oleh V_i (makin besar makin baik).

## 🖥️ Alur Penggunaan
Tambah kriteria (nama + bobot 1‑5).

Tambah alternatif & (opsional) skor per kriteria.

Isi/Edit skor untuk alternatif tertentu di halaman “Edit Skor”.

Buka /rangking → lihat juara dan nilai V.


## 👤 Dev
Muhammad Iqbal Saputra – D4 Teknik Informatika
© 2025 – bebas digunakan untuk riset & pembelajaran.





