from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
import image_encode
import image_decode
import uuid

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ENCODED_FOLDER'] = 'encoded'
app.config['DECODED_FOLDER'] = 'decoded'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['ENCODED_FOLDER'], exist_ok=True)
os.makedirs(app.config['DECODED_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encode', methods=['GET', 'POST'])
def encode():
    if request.method == 'POST':
        image = request.files['carrier']
        secret_message = request.form['secret_message']
        if image and secret_message:
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
            new_image_name = str(uuid.uuid4()) + ".png"
            new_image_path = os.path.join(app.config['ENCODED_FOLDER'], new_image_name)
            image.save(image_path)
            image_encode.encode(image_path, secret_message, new_image_path)
            return redirect(url_for('encoded_image', image_name=new_image_name))
    return render_template('encode.html')

@app.route('/encoded/<image_name>', methods=['GET', 'POST'])
def encoded_image(image_name):
    if request.method == 'POST':
        new_name = request.form['new_image_name'] + ".png"
        new_path = os.path.join(app.config['ENCODED_FOLDER'], new_name)
        os.rename(os.path.join(app.config['ENCODED_FOLDER'], image_name), new_path)
        return redirect(url_for('download_file', filename=new_name))
    return render_template('encoded.html', image_name=image_name)

@app.route('/decode', methods=['GET', 'POST'])
def decode():
    if request.method == 'POST':
        image = request.files['carrier']
        if image:
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
            image.save(image_path)
            decoded_message = image_decode.decode(image_path)
            return render_template('decode.html', decoded_message=decoded_message)
    return render_template('decode.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/encoded/<filename>')
def encoded_file(filename):
    return send_from_directory(app.config['ENCODED_FOLDER'], filename)

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['ENCODED_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
