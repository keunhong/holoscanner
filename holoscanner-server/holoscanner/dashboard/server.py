import argparse
from flask import Flask, render_template
from holoscanner import config

parser = argparse.ArgumentParser(
    description='Main server for HoloScanner')
parser.add_argument('--save-mesh-dir', dest='save_mesh_dir', type=str,
                    required=False)

args = parser.parse_args()

app = Flask(__name__)
app.debug = True
app.static_folder = './static'


@app.route('/')
def index():
    return render_template('dashboard.html')


if __name__=='__main__':
    app.run(host=config.DASHBOARD_ADDR,
            port=config.DASHBOARD_PORT)
