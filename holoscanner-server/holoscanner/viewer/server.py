from flask import Flask, render_template
from holoscanner import config

app = Flask(__name__)
app.debug = True
app.static_folder = './static'


@app.route('/')
def index():
    return render_template('viewer.html')


if __name__=='__main__':
    app.run(host=config.VIEWER_ADDR,
            port=config.VIEWER_PORT)
