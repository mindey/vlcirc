#
# Usage:
# python vlcirc.py /path/to/video/file irc_channel
#
# Example: (Linux and MacOS)
#
# 1) Execute command:
#    python vlcirc.py /home/mindey/AlienPlanet.avi MindeyXX1
# 2) Open website:
#    http://webchat.freenode.net/?channels=MindeyXX1
# 3) Once all of your friends had come to channel, typing:
#    play time=180
#
# Will start VLC player on all of the friends' computers almost simultaneously.
#
# For convenience, you may consider adding some thing like:
#        alias vlci='python /home/mi/vlcirc.py $*'
# to your ~/.bashrc

#
# Example: (Windows)
# 
# cp vlcirc.py C:\Python27\
# cp AlienPlanet.avi C:\Python27\
# cd C:\Python27\
# python.exe vlcirc.py AlienPlanet.avi MindeyXX1
#
# This project is licensed under GPLv3.0 license:
# http://www.gnu.org/licenses/gpl-3.0.txt

from random import random
from sys import argv
from socket import socket, AF_INET, SOCK_STREAM
from os import system
from platform import system as syst
from time import sleep

video_path = argv[1]
irc_nickname = 'Ply'+str(int(random()*10**5))
irc_channel = argv[2]
try:
  correction = float(argv[3])
except:
  correction = 0

# IRC Connect
network = 'irc.freenode.net'
port = 6667
irc = socket ( AF_INET, SOCK_STREAM )
irc.connect ( ( network, port ) )
print irc.recv ( 4096 )
irc.send ( 'NICK %s\r\n' % irc_nickname )
irc.send ( 'USER %s PyIRC PyIRC :Python IRC\r\n' % irc_nickname )
irc.send ( 'JOIN #%s\r\n' % irc_channel)

# IRC Stream
def ircstream():
  while True:
    data = irc.recv ( 4096 )
    if data.find ( 'PING' ) != -1:
      irc.send ( 'PONG ' + data.split() [ 1 ] + '\r\n' )
    print data # IRC channel data
    if 'End of /NAMES list' in data:
      print "Now, join the channel: http://webchat.freenode.net/?channels=%s channel, and type 'play time=180' to start video at 2:00 min." % irc_channel 
    if ('play' in data) or ('pause' in data):
      if 'lay time=' in data:
        time = int(data.split('lay time=')[1].split(' ')[0])
      elif 'lay at ' in data:
        T = [int(t) for t in data.split('lay at ')[1].split(' ')[0].split(':')]
        if len(T) == 3:
          time = T[0]*3600+T[1]*60+T[2]
        elif len(T) == 2:
          time = T[0]*60+T[1]
        elif len(T) == 1:
          time = T[0]
        else:
          time = 0
      else:
        time = 0
      if correction > 0:
        sleep(correction)
      # Linux
      if syst()=='Linux':
        system('vlc --start-time %s %s &' % (time,video_path))
      # Mac-OS
      elif syst()=='Darwin':
        system('/Applications/VLC.app/Contents/MacOS/VLC --start-time %s %s &' % (time,video_path))
      # Win-OS
      elif syst()=='Windows':
        system('"C:\\Program Files\\VideoLAN\\VLC\\vlc.exe" --start-time %s %s &' % (time,video_path))
  pass

# Main
ircstream()
