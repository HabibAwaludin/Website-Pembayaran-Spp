from pymongo import MongoClient

# Membuat koneksi ke MongoDB
client = MongoClient('mongodb+srv://AyangFreya:AyangElla@projectayang.c1mw30u.mongodb.net/?retryWrites=true&w=majority')
db = client['Ayang_freya']
users_collection = db['users']

# Tambahkan entri pengguna ke dalam koleksi users
def add_user(username, password, role):
    user_data = {
        'username': username,
        'password': password,
        'role': role
    }
    users_collection.insert_one(user_data)

# Tambahkan beberapa pengguna awal
add_user('admin', 'admin1', 'admin')

print("Users added successfully")
