import csv

import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

def connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='Tangkabiringan@1',
        database='classmonitoring'
    )

def create_user(username, password):
    conn = connection()
    cursor = conn.cursor()
    password_hash = generate_password_hash(password)  # Hash password sebelum disimpan
    cursor.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)", (username, password_hash))
    conn.commit()
    cursor.close()
    conn.close()

def insert_data(class_code, class_name):
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO class (class_code, class_name) VALUES (%s, %s)", (class_code, class_name))
    conn.commit()
    cursor.close()
    conn.close()

def read_txt_file(file_path):
    with open(file_path, 'r', encoding="utf-8") as file:
        reader = csv.reader(file, delimiter=';')
        data = [row for row in reader if len(row) == 2]
    return data

if __name__ == '__main__':
    file_path = "resource/ClassData.txt"
    data = read_txt_file(file_path)

    if data:
        for class_code, class_name in data:
            insert_data(class_code, class_name)
        print(f"{len(data)} data berhasil dimasukkan ke database.")
    else:
        print("File kosong atau tidak valid.")