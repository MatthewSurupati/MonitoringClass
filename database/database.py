import mysql.connector
import pandas as pd
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

def connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='Tangkabiringan@1',
        database='classmonitoring'
    )

def login(username, password):
    conn = connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    if user and check_password_hash(user["password_hash"], password):
        return user  # Login berhasil
    return None  # Login gagal

def get_all_mata_kuliah():
    """Mengambil semua data mata kuliah dari database"""
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM class")
    data = cursor.fetchall()
    conn.close()
    return [{"class_code": row[0], "class_name": row[1]} for row in data]

def get_mata_kuliah():
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM class")
    data = cursor.fetchall()
    conn.close()
    return {row[0]: row[1] for row in data}

def add_mata_kuliah(class_code, class_name):
    conn = connection()
    cursor = conn.cursor()
    query = "INSERT INTO class (class_code, class_name) VALUES (%s, %s)"
    cursor.execute(query, (class_code, class_name))
    conn.commit()
    cursor.close()
    conn.close()

def delete_mata_kuliah(class_code):
    """Menghapus mata kuliah berdasarkan ID"""
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM class WHERE class_code = %s", (class_code,))
    conn.commit()
    conn.close()

def update_mata_kuliah(class_code, new_name):
    """Mengupdate nama mata kuliah berdasarkan ID"""
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE class SET class_name = %s WHERE class_code = %s", (new_name, class_code))
    conn.commit()
    conn.close()

def get_activity_list():
    """Mengambil data aktivitas yang di lakukan"""
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("Select activity, category from activity")
    activities = cursor.fetchall()

    categories = {
        'terlibat': [],
        'tidak_terlibat': []
    }

    for activity in activities:
        if activity[1] == 'Terlibat':
            categories['terlibat'].append(activity[0])
        else:
            categories['tidak_terlibat'].append(activity[0])

    conn.close()
    return categories

def save_analysis_result(id_monitoring, class_code, engaged, not_engaged, analysis_result):
    """Menyimpan Hasil Analysis"""
    conn = connection()
    cursor = conn.cursor()
    cursor.execute('''insert into monitoring (date, class_code, id_monitoring, count_engage, count_not_engage, analysis) VALUES(%s, %s, %s, %s, %s, %s)''', (datetime.datetime.now(), class_code, id_monitoring, engaged, not_engaged, analysis_result))
    conn.commit()
    conn.close()

def save_detail_analysis(id_monitoring, activity_count):
    """Menyimpan detail deteksi"""
    conn = connection()
    cursor = conn.cursor()
    try:
        query = """
                INSERT INTO detail_monitoring (id_monitoring, activity, activity_count)
                VALUES (%s, %s, %s)
                """

        # Persiapkan data untuk dimasukkan
        data_to_insert = [(id_monitoring, activity, count) for activity, count in activity_count.items()]

        # Eksekusi query untuk setiap data
        cursor.executemany(query, data_to_insert)
        conn.commit()
        print("Detail analysis berhasil disimpan.")

    except mysql.connector.Error as e:
        conn.rollback()
        print(f"Error: {e}")

    finally:
        cursor.close()
        conn.close()

def get_monitoring_data():
    """Mengambil data dari tabel monitoring"""
    conn = connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM monitoring")
    data = cursor.fetchall()
    conn.close()
    return pd.DataFrame(data)

def get_detail_monitoring(id_monitoring):
    conn = connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""SELECT * FROM detail_monitoring WHERE id_monitoring = %s""", (id_monitoring,))
    data = cursor.fetchall()
    conn.close()
    return pd.DataFrame(data)