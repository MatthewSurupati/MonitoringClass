# 🖥️ClassMonitoring Project Using YOLO
__Overview__

ClassMonitoring adalah aplikasi berbasis Streamlit yang digunakan untuk memonitor aktivitas dalam kelas. Aplikasi ini memungkinkan pengguna untuk:
- Melihat daftar mata kuliah dari database
- Mengedit dan menghapus data mata kuliah
- Mengunggah video atau menggunakan kamera untuk mendeteksi aktivitas dalam kelas menggunakan model YOLO
- Menyimpan hasil deteksi ke dalam database, mencatat mata kuliah, serta jumlah orang yang melakukan aktivitas tertentu seperti makan atau tidur.

__Technologies Used__

- __Python__ (Streamlit, OpenCV, SQLAlchemy, YOLO)
- __Database:__ MySQL/PostgreSQL
- __Machine Learning Model:__ YOLO untuk deteksi Aktivitas

__Project Structure__
```
MonitoringClass/
│── pages/
│   ├── dashboard.py
│   ├── mata_kuliah.py
│── models/
│   ├── yolo_model.py
│   ├── database.py
│── static/
│   ├── styles.css
│── main.py
│── requirements.txt
│── README.md
```

__Installation__
1. Clone repository:
   ```
   git clone https://github.com/yourusername/ClassMonitoring.git
   cd MonitoringClass
   ```
2. Buat virtual environment dan install dependensi:
   ```
   python -m venv env
   source env/bin/activate  # Untuk Mac/Linux
   env\Scripts\activate  # Untuk Windows
   pip install -r requirements.txt
   ```
3. Jalankan Apliaksi
   ```
   streamlit run main.py
   ```
__Database Setup__

- Pastikan database telah dibuat dan berisi tabel `class`, `activity`, `users` dan `activity_log`.
- Jika belum ada, maka buatlah terlebih dahulu.

__Feature__

1. __Mata Kuliah__
   - Menampilkan daftar mata kuliah dari tabel `class`.
   - Tersedia tombol __Add__, __Edit__ dan __Delete__ untuk menambahkan, mengubah atau menghapus data mata kuliah.
2. __Dashboard__
   - Menampilkan daftar mata kuliah yang diambil dari database.
   - Memungkinkan pengguna untuk mengunggah video atau menggunakan kamera.
   - Menggunakan model YOLO untuk mendeteksi aktivitas di dalam kelas.
   - Menampilkan hasil deteksi di bawah area upload/camera.
   - Menyimpan hasil deteksi ke dalam database.
3. __YOLO Activity Detection__
   - Menggunakan model YOLO untuk mendeteksi aktivitas seperti makan, tidur, dll.
   - Menyimpan aktivitas ke database dengan mencatat mata kuliah serta jumlah orang yang melakukan setiap aktivitas.

> [!IMPORTANT]
> Pastikan semua dependensi yang ada memiliki versi yang kompatible.
