#siem9 Client

The siem9 client application will run in the background, capturing network traffic and collecting system logs all in real-time. It will then send the information it gets to the siem9 server for further processing.

To install the client:
```
sudo python setup.py install
sudo service siem9 start
```

The client will now be installed and running. And will stop/start on its own on shutdown and startup.

**_Tested on Ubuntu 16.04 and Kali Linux_**
