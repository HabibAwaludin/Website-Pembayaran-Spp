from bson import ObjectId
from flask import Flask, Response, render_template, redirect, url_for, request
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from pymongo import MongoClient
from fpdf import FPDF

app = Flask(__name__)
app.secret_key = 'LisaMary'

login_manager = LoginManager()
login_manager.init_app(app)

# Koneksi MongoDB
client = MongoClient('mongodb+srv://AyangFreya:AyangElla@projectayang.c1mw30u.mongodb.net/?retryWrites=true&w=majority')
db = client['Ayang_freya']
users_collection = db['users']
dataspp_collection = db['dataspp']
datakelas_collection = db['datakelas']
datasiswa_collection = db['datasiswa']
pembayaran_collection = db['pembayaran']


class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Laporan Pembayaran SPP', 0, 1, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'Halaman %s' % self.page_no(), 0, 0, 'C')

class User(UserMixin):
    pass


@login_manager.user_loader
def user_loader(username):
    user_data = users_collection.find_one({'username': username})
    if not user_data:
        return

    user = User()
    user.id = username
    user.role = user_data.get('role', 'unknown')  # Menggunakan get untuk mendapatkan nilai 'role', default jika tidak ada adalah 'unknown'
    return user

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/laporan')
def laporam():
    return render_template('laporan.html')

@app.route('/laporan-petugas')
def laporan():
    return render_template('laporan_petugas.html')

@app.route('/laporan-siswa')
def laporan_siswa():
    return render_template('laporan_siswa.html')

@app.route('/data-spp')
def spp():
    dataspps = dataspp_collection.find()
    return render_template('dataspp.html', dataspps=dataspps)

@app.route('/transaksi')
def transaksi():
    bayar = pembayaran_collection.find()
    return render_template('data_transaksi.html', pembayaran=bayar)

@app.route('/transaksi-petugas')
def transaksi_petugasi():
    bayar = pembayaran_collection.find()
    return render_template('data_transaksi_petugas.html', pembayaran=bayar)

@app.route('/tambah-kelas')
def tambah_kelas():
    return render_template('tambah_kelas.html')

@app.route('/tambah-siswa')
def tambah_siswa():
    return render_template('tambah_siswa.html')

@app.route('/tambah-pengguna')
def tambah_pengguna():
    return render_template('tambah_petugas.html')

@app.route('/data-pengguna')
def data_pengguna():
    user = users_collection.find()
    return render_template('data_petugas.html', users=user)

@app.route('/tambah-data')
def tambah():
    return render_template('tambah_data.html')

@app.route('/edit-kelas')
def edi_tkelas():
    return render_template('edit_kelas.html')

@app.route('/edit-data')
def edit():
    return render_template('edit_data.html')

@app.route('/add', methods=['POST'])
def add_dataspp():
    if request.method == 'POST':
        tahun = request.form['tahun']
        nominal = request.form['nominal']
                
        data_spp = {
            'tahun': tahun,
            'nominal': nominal
        }
        dataspp_collection.insert_one(data_spp)        
        return redirect(url_for('spp'))
    
@app.route('/add-data', methods=['GET', 'POST'])
def add_datakelas():
    if request.method == 'POST':
        nama_kelas = request.form['nama_kelas']
        kompetensi_keahlian = request.form['kompetensi_keahlian']
                
        data_kelas = {
            'nama_kelas': nama_kelas,
            'kompetensi_keahlian': kompetensi_keahlian
        }
        datakelas_collection.insert_one(data_kelas)        
        return redirect(url_for('kelas'))  # Mengarahkan kembali ke halaman data-kelas setelah menambahkan data
    elif request.method == 'GET':
        return render_template('data_kelas.html')
    
@app.route('/add-petugas', methods=['GET', 'POST'])
def add_datapetugas():
    if request.method == 'POST':
        nama_kelas = request.form['nama_kelas']
        kompetensi_keahlian = request.form['kompetensi_keahlian']
                
        data_kelas = {
            'nama_kelas': nama_kelas,
            'kompetensi_keahlian': kompetensi_keahlian
        }
        datakelas_collection.insert_one(data_kelas)        
        return redirect(url_for('kelas'))  # Mengarahkan kembali ke halaman data-kelas setelah menambahkan data
    elif request.method == 'GET':
        return render_template('data_kelas.html')
    
@app.route('/add-siswa', methods=['POST'])
def add_siswa():
    if request.method == 'POST':
        nisn = request.form['nisn']
        nis = request.form['nis']
        name = request.form['name']
        id_kelas = request.form['id_kelas']
        alamat = request.form['alamat']
        no_telp = request.form['no_telp']
        tahun_masuk = request.form['tahun']

        siswa = {
            'nisn': nisn,
            'nis': nis,
            'name': name,
            'id_kelas': id_kelas,
            'alamat': alamat,
            'no_telp': no_telp,
            'tahun_masuk': tahun_masuk
        }

        datasiswa_collection.insert_one(siswa)
        return redirect(url_for('siswa'))

    return redirect(url_for('tambah_siswa'))

@app.route('/admin/add_user', methods=['GET', 'POST'])
@login_required
def add_user():
    if current_user.role != 'admin':
        return 'Unauthorized'

    if request.method == 'POST':
        id_petugas = request.form['id_petugas']
        nama_petugas = request.form['nama_petugas']
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        users_collection.insert_one({'username': username, 'password': password, 'role': role, 'id_petugas':id_petugas, 'nama_petugas': nama_petugas})
        return redirect(url_for('data_pengguna'))
    else:
        return render_template('tambah_pengguna.html') 


@app.route('/input_pembayaran', methods=['POST'])
def input_pembayaran():
    if request.method == 'POST':
        id_petugas = request.form['id_petugas']
        nisn = request.form['nisn']
        tgl_bayar = request.form['tgl_bayar']
        bulan_dibayar = request.form['bulan_dibayar']
        tahun_dibayar = request.form['tahun_dibayar']
        id_spp = request.form['id_spp']
        jumlah_bayar = request.form['jumlah_bayar']

        pembayaran = {
            'id_petugas': id_petugas,
            'nisn': nisn,
            'tgl_bayar': tgl_bayar,
            'bulan_bayar': bulan_dibayar,
            'tahun_dibayar': tahun_dibayar,
            'id_spp': id_spp,
            'jumlah_bayar': jumlah_bayar
        }

        pembayaran_collection.insert_one(pembayaran)
        return redirect(url_for('transaksi'))

@app.route('/input_pembayaran-petugas', methods=['POST'])
def input_pembayaran_petugas():
    if request.method == 'POST':
        id_petugas = request.form['id_petugas']
        nisn = request.form['nisn']
        tgl_bayar = request.form['tgl_bayar']
        bulan_dibayar = request.form['bulan_dibayar']
        tahun_dibayar = request.form['tahun_dibayar']
        id_spp = request.form['id_spp']
        jumlah_bayar = request.form['jumlah_bayar']

        pembayaran = {
            'id_petugas': id_petugas,
            'nisn': nisn,
            'tgl_bayar': tgl_bayar,
            'bulan_bayar': bulan_dibayar,
            'tahun_dibayar': tahun_dibayar,
            'id_spp': id_spp,
            'jumlah_bayar': jumlah_bayar
        }

        pembayaran_collection.insert_one(pembayaran)
        return redirect(url_for('transaksi_petugasi'))


@app.route('/edit/<dataspp_id>', methods=['GET', 'POST'])
def edit_data(dataspp_id):  
    if request.method == 'GET':
        data_spp = dataspp_collection.find_one({'_id': ObjectId(dataspp_id)})
        if data_spp:
            return render_template('edit_data.html', data_spp=data_spp)
        else:
            return "Address not found", 404
    elif request.method == 'POST':
        tahun = request.form['tahun']
        nominal = request.form['nominal']

        dataspp_collection.update_one(
            {'_id': ObjectId(dataspp_id)},
            {'$set': {
                'tahun': tahun,
                'nominal': nominal,
            }}
        )

        return redirect(url_for('spp'))

@app.route('/edit/add_user/<users_id>', methods=['GET', 'POST'])
def edit_user(users_id):  
    if request.method == 'GET':
        user = users_collection.find_one({'_id': ObjectId(users_id)})
        if user:
            return render_template('edit_user.html', user=user)  # Mengganti users=user menjadi user=user
        else:
            return "Address not found", 404
    elif request.method == 'POST':
        id_petugas = request.form['id_petugas']
        nama_petugas = request.form['nama_petugas']
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        users_collection.update_one(
            {'_id': ObjectId(users_id)},
            {'$set': {
                'id_petugas': id_petugas,
                'nama_petugas': nama_petugas,
                'username': username,
                'password': password,
                'role': role,
            }}
        )

        return redirect(url_for('data_pengguna'))



@app.route('/edit-kelas/<datakelas_id>', methods=['GET', 'POST'])
def edit_kelas(datakelas_id): 
    if request.method == 'GET':
        data_kelas = datakelas_collection.find_one({'_id': ObjectId(datakelas_id)})
        if data_kelas:
            return render_template('edit_kelas.html', data_kelas=data_kelas)
        else:
            return "Data kelas not found", 404
    elif request.method == 'POST':
        nama_kelas = request.form['nama_kelas']
        kompetensi_keahlian = request.form['kompetensi_keahlian']

        datakelas_collection.update_one(
            {'_id': ObjectId(datakelas_id)},
            {'$set': {
                'nama_kelas': nama_kelas,
                'kompetensi_keahlian': kompetensi_keahlian,
            }}
        )

        return redirect(url_for('kelas'))
    
@app.route('/edit-siswa/<datasiswa_id>', methods=['GET', 'POST'])
def edit_siswa(datasiswa_id): 
    if request.method == 'GET':
        data = datasiswa_collection.find_one({'_id': ObjectId(datasiswa_id)})
        if data:
            return render_template('edit_siswa.html', data=data)
        else:
            return "Data siswa tidak ditemukan", 404
    elif request.method == 'POST':
        nisn = request.form['nisn']
        nis = request.form['nis']
        name = request.form['name']
        id_kelas = request.form['id_kelas']
        alamat = request.form['alamat']
        no_telp = request.form['no_telp']
        tahun_masuk = request.form['tahun']

        datasiswa_collection.update_one(
            {'_id': ObjectId(datasiswa_id)},
            {'$set': {
                'nisn': nisn,
                'nis': nis,
                'name': name,
                'id_kelas': id_kelas,
                'alamat': alamat,
                'no_telp': no_telp,
                'tahun_masuk': tahun_masuk
            }}
        )

        return redirect(url_for('siswa'))

    
@app.route('/delete/<dataspp_id>', methods=['GET', 'POST'])
def delete_data(dataspp_id):
    if request.method == 'GET':
        return render_template('delete_confirmation.html', dataspp_id=dataspp_id)
    elif request.method == 'POST':
        dataspp_collection.delete_one({'_id': ObjectId(dataspp_id)})
        return redirect(url_for('spp'))

@app.route('/delete-siswa/<data_id>', methods=['GET', 'POST'])
def delete_siswa(data_id):
    if request.method == 'GET':
        return render_template('delete1.html', data_id=data_id)
    elif request.method == 'POST':
        datasiswa_collection.delete_one({'_id': ObjectId(data_id)})
        return redirect(url_for('siswa'))

@app.route('/delete-kelas/<datakelas_id>', methods=['GET', 'POST'])
def delete(datakelas_id):
    if request.method == 'GET':
        return render_template('delete.html', datakelas_id=datakelas_id)
    elif request.method == 'POST':
        datakelas_collection.delete_one({'_id': ObjectId(datakelas_id)})
        return redirect(url_for('kelas'))

@app.route('/data-kelas')
def kelas():
    datakelas = datakelas_collection.find()
    return render_template('data_kelas.html', datakelas=datakelas)

@app.route('/data-siswa')
def siswa():
    datasiswa = datasiswa_collection.find()
    return render_template('data_siswa.html', datasiswa=datasiswa)

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    user_data = users_collection.find_one({'username': username, 'password': password})
    if user_data:
        user = User()
        user.id = username
        user.role = user_data['role']  # Load role from MongoDB
        login_user(user)
        return redirect(url_for('dashboard'))
    else:
        return 'Invalid username or password'

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'admin':
        return render_template('admin_dashboard.html')
    elif current_user.role == 'petugas':
        return render_template('petugas_dashboard.html')
    elif current_user.role == 'siswa':
        return render_template('student_dashboard.html')
    else:
        return 'Welcome to the visitor dashboard!'

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/generate-pdf', methods=['POST'])
def generate_pdf():
    dari_tanggal = request.form.get('daritanggal')
    sampai_tanggal = request.form.get('sampaitanggal')

    pembayaran = pembayaran_collection.find({
        'tgl_bayar': {'$gte': dari_tanggal, '$lte': sampai_tanggal}
    })

    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Laporan Pembayaran SPP", ln=True, align='C')
    pdf.ln(10)

    for bayar in pembayaran:
        pdf.cell(200, 10, txt=f"ID: {bayar['_id']}", ln=True)
        pdf.cell(200, 10, txt=f"ID Petugas: {bayar['id_petugas']}", ln=True)
        pdf.cell(200, 10, txt=f"NISN: {bayar['nisn']}", ln=True)
        pdf.cell(200, 10, txt=f"Tanggal Bayar: {bayar['tgl_bayar']}", ln=True)
        pdf.cell(200, 10, txt=f"Bulan Bayar: {bayar['bulan_bayar']}", ln=True)
        pdf.cell(200, 10, txt=f"Tahun Bayar: {bayar['tahun_dibayar']}", ln=True)
        pdf.cell(200, 10, txt=f"ID SPP: {bayar['id_spp']}", ln=True)
        pdf.cell(200, 10, txt=f"Jumlah Bayar: {bayar['jumlah_bayar']}", ln=True)
        pdf.ln(10)

    pdf_output = pdf.output(dest='S').encode('latin1')
    
    response = Response(pdf_output)
    response.headers.set('Content-Disposition', 'attachment', filename='laporan_pembayaran_spp.pdf')
    response.headers.set('Content-Type', 'application/pdf')
    return response

    

if __name__ == '__main__':
    app.run(debug=True)
