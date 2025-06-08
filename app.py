from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
from weasyprint import HTML
import os
import uuid

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.form.to_dict()
    photo_path = None

    file = request.files.get('photo')
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        unique_filename = str(uuid.uuid4()) + "_" + filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(filepath)
        photo_path = filepath

    html = render_template('resume_template.html', **data, photo=photo_path)
    pdf_file_path = os.path.join('static', 'generated_resume.pdf')
    HTML(string=html, base_url='.').write_pdf(pdf_file_path)

    return send_file(pdf_file_path, as_attachment=True, download_name='resume.pdf')

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)