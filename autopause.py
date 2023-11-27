import sys
import dbus
import pulsectl
import time
import signal

def sig_handler(signal, frame):
   sys.exit(0)

signal.signal(signal.SIGINT, sig_handler)
session_bus = dbus.SessionBus()
spotify = session_bus.get_object('org.mpris.MediaPlayer2.spotify', '/org/mpris/MediaPlayer2')
player_iface = dbus.Interface(spotify, 'org.mpris.MediaPlayer2.Player')
props_iface = dbus.Interface(spotify, 'org.freedesktop.DBus.Properties')

def check_spotify():
   with pulsectl.Pulse('my-client') as pulse:
       spotify_sink_input = next(filter(lambda si: 'Spotify' in si.name, pulse.sink_input_list()))
       spotify_status = props_iface.Get('org.mpris.MediaPlayer2.Player', 'PlaybackStatus')
       sink_inputs = pulse.sink_input_list()
       uncorked = filter(lambda si: not 'Spotify' in si.name and not si.corked, sink_inputs)
       if len(list(uncorked)) > 0:

           if spotify_status == 'Playing':
               player_iface.Pause()
       elif spotify_status == 'Paused':
           player_iface.Play()


while True:
   check_spotify()
   time.sleep(1)
