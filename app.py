from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
import os
from pdf2docx import Converter

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def convert():
    if request.method == 'POST':
        f = request.files['file']
        filename = secure_filename(f.filename)
        f.save(filename)

        # Convert the PDF to Word
        word_filename = os.path.splitext(filename)[0] + '.docx'
        cv = Converter(filename)
        cv.convert(word_filename, start=0, end=None)
        cv.close()

        # Clean up the files
        os.remove(filename)

        return render_template('index.html', message='Conversion complete!', download_link=word_filename)

    return render_template('index.html')

@app.route('/download/<filename>', methods=['GET'])
def download(filename):
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
