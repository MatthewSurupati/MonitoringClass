import hashlib
from datetime import datetime

def hash_mata_kuliah(mata_kuliah, waktu):
    data = f"{mata_kuliah}-{waktu}"
    return hashlib.sha256(data.encode()).hexdigest()[:255]