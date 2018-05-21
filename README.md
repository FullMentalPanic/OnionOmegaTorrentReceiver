# PiTorrentTV

Hardware: 

  Rassberry Pi 3 , Usbstorage, 
  
Software:

 1. Simple omxplayer GUI application

    C++ - Qt5 omxplayer

 2  Server in Pi

    flask + gunicorn + nginx + supervisor

 3 - Pi control and Torrent download function
    
    python 3

    thread 1 collect torrent from email
    thread 2 trace torrent from web
    thread 3 add torrent in transmission
    thread 4 monitor hdd spare and pi temp
