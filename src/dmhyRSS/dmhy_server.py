from flask import Flask, render_template, Response,flash, request, redirect, url_for
from flask_socketio import SocketIO
from werkzeug.utils import secure_filename
import os

debug_server = 1

if debug_server == 0:
   from torrent_collect import TorrentCollect
   import control as cl
   pi_service = TorrentCollect()
   pi_service.run()
   cl.Set_xdotool_env()
UPLOAD_FOLDER = ''
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
socketio = SocketIO(app)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/upload", methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
    # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and file.filename == 'config.yml':
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('index'))
    return render_template('upload.html')

@socketio.on('my event')
def handle_my_event(arg):
    #print (arg)
    if arg == 'Up':
        cl.simluate_input('Up')
        printMsg ("Up",debug_server)
        pass
    elif arg == 'Down':
        cl.simluate_input('Down')
        printMsg ("Down",debug_server)
        pass
    elif arg == 'Right':
        cl.simluate_input('Right')
        printMsg ("Right",debug_server)
        pass
    elif arg == 'Left':
        cl.simluate_input('Left')
        printMsg ("Left",debug_server)
        pass
    elif arg == 'OK':
        cl.simluate_input('Return')
        printMsg ("OK",debug_server)
        pass
    elif arg == 'Pause':
        cl.simluate_input('ctrl+p')
        printMsg ("Pause",debug_server)
        pass
    elif arg == 'Stop':
        cl.simluate_input('ctrl+q')
        printMsg ("Stop",debug_server)
        pass
    elif arg == 'Exit':
        cl.simluate_input('ctrl+e')
        printMsg ("Exit",debug_server)
        os.system("sudo shutdown -h now")
        pass
    else:
        print (arg)

def printMsg(str, debug = 1):
    if debug == 1:
        print(str)
    else:
        return

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')
