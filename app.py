from flask import Flask, request, redirect, url_for, flash, render_template
import sqlite3

app = Flask(__name__)
app.secret_key = '123'

def db_connection():
    db = None
    try:
        db = sqlite3.connect('krstool.sqlite')
    except sqlite3.Error as e:
        print(e)
    return db

db = db_connection()
cur = db.cursor()
cur.execute('''
    CREATE TABLE IF NOT EXISTS matkul(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nama_matkul VARCHAR(100),
        hari VARCHAR(100),
        jam_mulai VARCHAR(100),
        jam_akhir VARCHAR(100)
    );
''')
db.close()


@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        nama_matkul = request.form['nama_matkul']
        hari = request.form['hari']
        jam_mulai = request.form['jam_mulai']
        jam_akhir = request.form['jam_akhir']
        
        db = db_connection()
        cur = db.cursor()
        cur.execute('''
            SELECT * FROM matkul;
        ''')
        dataBase = cur.fetchall()
        
        for data in dataBase:
            if hari == data[2]:
                if jam_mulai >= data[3] and jam_mulai <= data[4]:
                    flash(f'Jadwal tabrakan 1 dengan "{data[1]}";danger')
                    return redirect(url_for('index'))
                elif jam_akhir >= data[3] and jam_akhir <= data[4]:
                    flash(f'Jadwal tabrakan 2 dengan "{data[1]}";danger')
                    return redirect(url_for('index'))
                elif data[3] >= jam_mulai and data[3] <= jam_akhir:
                    flash(f'Jadwal tabrakan 3 dengan "{data[1]}";danger')
                    return redirect(url_for('index'))
                elif data[4] >= jam_mulai and data[4] <= jam_akhir:
                    flash(f'Jadwal tabrakan 4 dengan "{data[1]}";danger')
                    return redirect(url_for('index'))

        try:
            db = db_connection()
            cur = db.cursor()
            cur.execute(f'''
                INSERT INTO matkul(nama_matkul, hari, jam_mulai, jam_akhir) 
                VALUES("{nama_matkul}","{hari}","{jam_mulai}","{jam_akhir}");
            ''')
            print('BERHASIL TAMBAH DATA')
            db.commit()
            db.close()
        except sqlite3.Error as e:
            print(e)

    db = db_connection()
    cur = db.cursor()
    cur.execute('''
        SELECT * FROM matkul;
    ''')
    data = cur.fetchall()
    db.close()
    return render_template('index.html', data=data)

@app.route('/delete')
def delete():
    aydi = int(request.args.get('id'))
    if aydi:
        db = db_connection()
        cur = db.cursor()
        cur.execute(f'''DELETE FROM matkul WHERE id={aydi}''')
        db.commit()
        db.close()
        flash('Berhasil menghapus;success')
        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)