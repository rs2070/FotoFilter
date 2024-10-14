from flask import Flask, request, jsonify, render_template, send_from_directory, session, send_file
import os
from werkzeug.utils import secure_filename
import zipfile
import io

from face_detection import FaceDetector
from blur_detection import process_blurry, BlurDetector
from similarity_detection import find_duplicates

app = Flask(__name__)
app.secret_key = 'very_secure_secret'
app.config['UPLOAD_FOLDER'] = 'uploaded_images'
app.config['PROCESSED_IMAGES_FOLDER'] = 'processed_images'
app.config['STATIC_FOLDER'] = 'static'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['PROCESSED_IMAGES_FOLDER'], exist_ok=True)

face_detector = FaceDetector()

@app.route('/')
def index():
    session.clear()
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    zip_option = request.json.get('zip', 'no')
    flagged_images = session.get('flagged_images', [])
    if zip_option == 'yes':
        memory_file = io.BytesIO()
        with zipfile.ZipFile(memory_file, 'w') as zf:
            for filename in flagged_images:
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                zf.write(file_path, arcname=filename)
        memory_file.seek(0)
        return send_file(memory_file, as_attachment=True, download_name='filtered_images.zip')
    else:
        file_urls = ['/uploaded_images/' + filename for filename in flagged_images]
        print("FILES TO DOWNLOAD ARE GONNA BE:", file_urls)
        return jsonify({'file_urls': file_urls})
        

@app.route('/analyze', methods=['POST'])
def analyze():
    files = request.files.getlist('files')
    action = request.form.get('action')
    results = []
    flagged_images = []

    for f in os.listdir(app.config['UPLOAD_FOLDER']): #clear upload folder before saving new files
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], f))

    if action == 'duplicates':
        all_filenames = []  #store all uploaded filenames
        for file in files:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            all_filenames.append(filename)  #add to all filenames list

        duplicates = find_duplicates(app.config['UPLOAD_FOLDER'])
        duplicates_set = set(sum(duplicates.values(), []))  #flatten list of duplicates and convert to set for faster operations
        non_duplicate_images = [filename for filename in all_filenames if filename not in duplicates_set]  #filter duplicates

        results = [{"image": original, "status": "duplicate"} for original, copies in duplicates.items()]
        session['flagged_images'] = non_duplicate_images  #put non-duplicates for download


    elif action == 'faces' or action == 'blur':
        for file in files:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            if action == 'faces':
                has_face, _ = face_detector.detect_faces_and_eyes(file_path)
                if has_face:
                    results.append({"image": filename, "status": "face_detected"})
                    flagged_images.append(filename)
            elif action == 'blur':
                blur_detector = BlurDetector()
                if blur_detector.is_blurry(file_path):
                    results.append({"image": filename, "status": "blurry"})
                else:
                    flagged_images.append(filename)

        session['flagged_images'] = flagged_images

    response_data = {'results': results, 'flagged_images': flagged_images}
    return jsonify(response_data)


@app.route('/uploaded_images/<filename>') #serve uploaded images
def uploaded_image(filename):
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    except Exception as e:
        return str(e), 404

@app.route('/processed_images/<filename>')
def send_processed_image(filename):
    try:
        return send_from_directory(app.config['PROCESSED_IMAGES_FOLDER'], filename)
    except Exception as e:
        return str(e), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)