from flask import Flask, render_template, Response,request



debug_server = 1

if debug_server == 0:
   from torrent_collect import TorrentCollect
   import control as cl
   pi_service = TorrentCollect()
   pi_service.run()

app = Flask(__name__)

@app.route("/", methods = ['GET','POST'])
def index():
   if request.method == 'POST':
      if request.form.get('Up') == 'Up':
         #cl.simluate_input('Up')
         print ("Up")
         pass
      elif request.form.get('Down') == 'Down':
         #cl.simluate_input('Down')
         print ("Down")
         pass
      elif request.form.get('Right') == 'Right':
         #cl.simluate_input('Right')
         print ("Right")
         pass
      elif request.form.get('Left') == 'Left':
         #cl.simluate_input('Left')
         print ("Left")
         pass
      elif request.form.get('OK') == 'OK':
         #cl.simluate_input('Return')
         print ("OK")
         pass
      elif request.form.get('Pause') == 'Pause':
         #cl.simluate_input('ctrl+p')
         print ("Pause")
         pass
      elif request.form.get('Stop') == 'Stop':
         #cl.simluate_input('ctrl+q')
         print ("Stop")
         pass
      elif request.form.get('Exit') == 'Exit':
         #cl.simluate_input('ctrl+e')
         print ("Exit")
         pass
      else:
         print ("None")
       
   return render_template('index.html')
                    
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)