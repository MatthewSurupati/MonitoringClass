import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

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