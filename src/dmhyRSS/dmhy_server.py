from flask import Flask, render_template, Response,request
from flask_socketio import SocketIO
import os

debug_server = 0

if debug_server == 0:
   from torrent_collect import TorrentCollect
   import control as cl
   pi_service = TorrentCollect()
   pi_service.run()
   cl.Set_xdotool_env()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route("/")
def index():
    return render_template('index.html')

@socketio.on('my event')
def handle_my_event(arg):
    #print (arg)
    if arg == 'Up':
        cl.simluate_input('Up')
        #print ("Up")
        pass
    elif arg == 'Down':
        cl.simluate_input('Down')
        #print ("Down")
        pass
    elif arg == 'Right':
        cl.simluate_input('Right')
        #print ("Right")
        pass
    elif arg == 'Left':
        cl.simluate_input('Left')
        #print ("Left")
        pass
    elif arg == 'OK':
        cl.simluate_input('Return')
        #print ("OK")
        pass
    elif arg == 'Pause':
        cl.simluate_input('ctrl+p')
        #print ("Pause")
        pass
    elif arg == 'Stop':
        cl.simluate_input('ctrl+q')
        #print ("Stop")
        pass
    elif arg == 'Exit':
        cl.simluate_input('ctrl+e')
        #print ("Exit")
        os.system("sudo shutdown -h now")
        pass
    else:
        print (arg)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')
