#!/usr/bin/bash
#sudo su
cd /home/eyetec/TA-3rdGen/lib/
sudo chmod +x /home/eyetec/TA-3rdGen/lib/campimetria/scripts/ativa_xscreensaver.sh
sudo python mainTA.py & sudo irxevent /home/eyetec/.lircrc 
& sudo xmodmap -e "pointer = 0 0 0 0 0 0 0 0 0 0"


