This script works with VLC Player ( http://www.videolan.org/ )

# Usage:

```
python2.7 vlcirc.py /path/to/video/file your_irc_channel
```

Then in the channel:
```
<irc_user> play
<irc_user> play at h:mm:ss
```

## Example: (Linux and MacOS)

1. Execute command:
```
python2.7 vlcirc.py ~/path/to/YourVideoFile.avi your_irc_channel
```
2. Open IRC channel:
```
http://webchat.freenode.net/?channels=your_irc_channel
```
3. Once all of your friends had come to channel, typing:
```
   <irc_user> play at h:mm:ss
```
will start VLC player on all of the friends' computers almost simultaneously.

For convenience, you may consider adding some thing like:
```
alias vlcirc='python /home/user/vlcirc.py $*'
```
to your ~/.bashrc or ~/.zshrc.

## Example: (Windows)
```
cp vlcirc.py C:\Python27\
cp YourVideoFile.avi C:\Python27\
cd C:\Python27\
python.exe vlcirc.py YourVideoFile.avi your_irc_channel
```

# Notes

P.S. I found that *libvlc* library, although convenient, but not readily available on various systems.

I had tried evdev - a keylogger approach, which allows one to avoid typing commands in IRC, but it requires admin rights.

Wishing to make it immediately usable on more different platforms, I refrained from using these approaches.

*To-Do:* Knowing each of the computers' clock times and ping times, the synchronization could be improved by approximating (rather accurately) the error due to the different ping times of each user, and, it seems, that in order to have more functionality like this, using *libvlc* would be convenient.

This project is licensed under: GPLv3.0 license.




