from flask import Flask, request, render_template, jsonify
import os
from deepfake_detection import build_model, detect_deepfake
from werkzeug.utils import secure_filename
import tensorflow as tf

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'mp4'}

# Load the fine-tuned model
model = tf.keras.models.load_model('fine_tuned_deepfake_model.h5')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])PS D:\Major Project\project> python app.py               
2025-05-03 12:54:19.996685: I tensorflow/core/util/port.cc:153] oneDNN custom operations are on. You may see slightly different numerical results due to floating-point round-off errors from different computation orders. To turn them off, set the environment variable `TF_ENABLE_ONEDNN_OPTS=0`.
2025-05-03 12:54:21.587268: I tensorflow/core/util/port.cc:153] oneDNN custom operations are on. You may see slightly different numerical results due to floating-point round-off errors from different computation orders. To turn them off, set the environment variable `TF_ENABLE_ONEDNN_OPTS=0`.
2025-05-03 12:54:25.100551: I tensorflow/core/platform/cpu_feature_guard.cc:210] This TensorFlow binary is optimized to use available CPU instructions in performance-critical operations.
To enable the following instructions: SSE3 SSE4.1 SSE4.2 AVX AVX2 FMA, in other operations, rebuild TensorFlow with the appropriate compiler flags.
Traceback (most recent call last):
  File "D:\Major Project\project\app.py", line 12, in <module>
    model = tf.keras.models.load_model('fine_tuned_deepfake_model.h5')
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\TUFF\AppData\Local\Programs\Python\Python311\Lib\site-packages\keras\src\saving\saving_api.py", line 196, in load_model
    return legacy_h5_format.load_model_from_hdf5(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\TUFF\AppData\Local\Programs\Python\Python311\Lib\site-packages\keras\src\legacy\saving\legacy_h5_format.py", line 116, in load_model_from_hdf5       
    f = h5py.File(filepath, mode="r")
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\TUFF\AppData\Local\Programs\Python\Python311\Lib\site-packages\h5py\_hl\files.py", line 564, in __init__
    fid = make_fid(name, mode, userblock_size, fapl, fcpl, swmr=swmr)
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\TUFF\AppData\Local\Programs\Python\Python311\Lib\site-packages\h5py\_hl\files.py", line 238, in make_fid
    fid = h5f.open(name, flags, fapl=fapl)
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "h5py\\_objects.pyx", line 54, in h5py._objects.with_phil.wrapper
  File "h5py\\_objects.pyx", line 55, in h5py._objects.with_phil.wrapper
  File "h5py\\h5f.pyx", line 102, in h5py.h5f.open
FileNotFoundError: [Errno 2] Unable to synchronously open file (unable to open file: name = 'fine_tuned_deepfake_model.h5', errno = 2, error message = 'No such file or directory', flags = 0, o_flags = 0)
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        is_video = filename.endswith('.mp4')
        pred, message = detect_deepfake(model, file_path, is_video)
        os.remove(file_path)
        return jsonify({'result': message, 'confidence': float(pred)})
    return jsonify({'error': 'Invalid file type'}), 400

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)