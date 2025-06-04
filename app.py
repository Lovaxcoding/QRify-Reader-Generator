from flask import Flask, render_template, request, redirect, url_for, flash
import os
from func import generate_qr_code, read_qr_code_from_image
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "supersecretkey"

UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.form.get('data')
    if not data:
        flash('Veuillez entrer un texte à encoder.', 'error')
        return redirect(url_for('index'))

    file_path = os.path.join('static', 'qrcode.png')
    success = generate_qr_code(data, file_path=file_path)

    if success:
        return render_template('index.html', qr_image=file_path, data=data)
    else:
        flash('Erreur lors de la génération du QR code.', 'error')
        return redirect(url_for('index'))

@app.route('/read', methods=['POST'])
def read():
    file = request.files.get('qr_image')
    if not file:
        flash('Veuillez télécharger une image contenant un QR code.', 'error')
        return redirect(url_for('index'))

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    result = read_qr_code_from_image(file_path)
    if result:
        flash(f'QR Code détecté : {result}', 'success')
    else:
        flash("Aucun QR code détecté dans l'image.", 'error')

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
