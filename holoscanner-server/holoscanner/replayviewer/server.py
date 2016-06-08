import argparse
from flask import Flask, render_template, request, jsonify
from holoscanner import config
import pdb
import json
import os

parser = argparse.ArgumentParser(
    description='Main server for HoloScanner')
parser.add_argument('--save-mesh-dir', dest='save_mesh_dir', type=str,
                    required=False)

args = parser.parse_args()

app = Flask(__name__)
app.debug = True
app.static_folder = './static'

# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = 'uploads/'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['json', 'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('replayviewer.html')

# Route that will process the file upload
@app.route('/uploadajx', methods=['POST'])
def upldfile():
    print('in file upload')
    #pdb.set_trace()

    if len(request.data)>0:
        msg_str = request.data.decode("utf-8")
        msg_obj = json.loads(msg_str)
        with open(os.path.join(app.config['UPLOAD_FOLDER'], msg_obj['filename']), 'w') as outfile:
            json.dump(msg_obj['data'], outfile)
            print('done with saving file!')
    return ''

# This route is expecting a parameter containing the name
# of a file. Then it will locate that file on the upload
# directory and show it on the browser, so if the user uploads
# an image, that image is going to be show after the upload
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

if __name__=='__main__':
    app.run(host=config.REPLAYVIEWER_ADDR,
            port=config.REPLAYVIEWER_PORT)
