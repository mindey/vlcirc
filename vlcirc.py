#
# Usage:
# python2.7 vlcirc.py /path/to/video/file your_irc_channel
# <irc_user> play
# <irc_user> play at h:mm:ss
#
# Example: (Linux and MacOS)
#
# 1) Execute command:
#    python2.7 vlcirc.py /home/mindey/YourVideoFile.avi your_irc_channel
# 2) Open website:
#    http://webchat.freenode.net/?channels=your_irc_channel
# 3) Once all of your friends had come to channel, typing:
#    play at h:mm:ss
#
# Will start VLC player on all of the friends' computers almost simultaneously.
#
# For convenience, you may consider adding some thing like:
#        alias vlcirc='python /home/user/vlcirc.py $*'
# to your ~/.bashrc

#
# Example: (Windows)
# 
# cp vlcirc.py C:\Python27\
# cp YourVideoFile.avi C:\Python27\
# cd C:\Python27\
# python.exe vlcirc.py YourVideoFile.avi your_irc_channel
#
# This project is licensed under GPLv3.0 license:
# http://www.gnu.org/licenses/gpl-3.0.txt

from random import random
from sys import argv
from socket import socket, AF_INET, SOCK_STREAM
from os import system
from os.path import exists
from platform import system as syst
from time import sleep
import re
import urllib2

vlc_path = 'vlc'
video_path = argv[1]
irc_nickname = 'Ply'+str(int(random()*10**5))
irc_channel = argv[2]

# Linux
if syst()=='Linux':
    vlc_path = 'vlc'

# Mac-OS
elif syst()=='Darwin':
    if exists('/Applications/VLC.app/Contents/MacOS/VLC'):
        vlc_path = '/Applications/VLC.app/Contents/MacOS/VLC'
    else:
        """ Try to retrieve path by checking possible versions """
        url = 'http://download.videolan.org/pub/videolan/vlc/'
        versions = re.findall('(?<=")(\d+\.\d+\.\d+(?=/))', urllib2.urlopen(url).read())
        for version in versions:
            if exists('/Volumes/vlc-%s/VLC.app/Contents/MacOS/VLC' % version):
                vlc_path = '/Volumes/vlc-%s/VLC.app/Contents/MacOS/VLC' % version
                break

# Win-OS
elif syst()=='Windows':
  if exists('C:\\Program Files\\VideoLAN\\VLC\\vlc.exe'):
        vlc_path = '"C:\\Program Files\\VideoLAN\\VLC\\vlc.exe"'
  if exists('C:\\Program Files (x86)\\VideoLAN\\VLC\\vlc.exe'):
        vlc_path = '"C:\\Program Files (x86)\\VideoLAN\\VLC\\vlc.exe"'


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

    print data # IRC channel data

    if data.find ( 'PING' ) != -1:
        irc.send ( 'PONG ' + data.split() [ 1 ] + '\r\n' )

    if 'End of /NAMES list' in data:
        print "Now, join the channel: http://webchat.freenode.net/?channels=%s channel, and type 'play at 1:30' to start video at 1:30 min." % irc_channel 

    if 'play at' in data:
        T = [int(t) for t in data.split('lay at ')[1].split(' ')[0].split(':')][::-1]
        S = [3600, 60, 1][::-1][:len(T)]

        if T:
            time = sum([t*s for t,s in zip(T[:len(S)], S)])
        else:
            time = 0

        print 'TIME=',time
        system('%s --start-time %s %s &' % (vlc_path, time, video_path))

  pass

# Main
ircstream()
