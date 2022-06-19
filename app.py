from flask import Flask, request, redirect, url_for, flash, render_template

app = Flask(__name__)
app.secret_key = '123'

dataBase = []

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        nama_matkul = request.form['nama_matkul']
        hari = request.form['hari']
        jam_mulai = request.form['jam_mulai']
        jam_akhir = request.form['jam_akhir']
        dataTemp = [nama_matkul, hari, jam_mulai, jam_akhir]

        for data in dataBase:
            if hari == data[1]:
                if jam_mulai >= data[2] and jam_mulai <= data[3]:
                    flash(f'Jadwal tabrakan 1 dengan "{data[0]}";danger')
                    return redirect(url_for('index'))
                elif jam_akhir >= data[2] and jam_akhir <= data[3]:
                    flash(f'Jadwal tabrakan 2 dengan "{data[0]}";danger')
                    return redirect(url_for('index'))
                elif data[2] >= jam_mulai and data[2] <= jam_akhir:
                    flash(f'Jadwal tabrakan 3 dengan "{data[0]}";danger')
                    return redirect(url_for('index'))
                elif data[3] >= jam_mulai and data[3] <= jam_akhir:
                    flash(f'Jadwal tabrakan 4 dengan "{data[0]}";danger')
                    return redirect(url_for('index'))

        dataBase.append(dataTemp)
        return render_template('index.html', data=dataBase)
    else:
        return render_template('index.html', data=dataBase)

@app.route('/delete')
def delete():
    aydi = int(request.args.get('id'))
    if aydi:
        aydi -= 1
        dataBase.pop(aydi)
        flash('Berhasil menghapus;success')
        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)