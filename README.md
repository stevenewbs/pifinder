pifinder
========

Two simple python scripts that that use UDP to locate your Raspberry Pi on a network

Useage


pifinder_server.py - designed to be called at boot time, needs permission to put the log into /var/log/
pifinder_client.py - can be run from the command line from your PC

Only requirement is python2 - I have yet to find a Linux OS where it isnt included as standard

For standard raspbain:

1) Copy pifinder_server.py to the raspberry pi.
<pre>
scp pifinder_server.py pi@raspberrypi:/home/pi/
</pre>
2) Edit /etc/rc.local and add the following line before the exit 0
<pre>
/usr/bin/python /home/pi/pifinder_server.py
</pre>
3) Reboot the pi

4) Run the client from your computer
<pre>
./pifinder_client.py
</pre>



