# Section-9-SIEM
SIEM for Software Engineering

Things to work on:

Ryan
  - Check how many packages are being recieved in case the client lost connection
    - check # of packages
    - get timestamps and name accordingly
  - Error checking
    - If file is a proper zip file
    - If there are error creating or opening the file
  - Create user authentication system (find secure way)
  - Organize filesystem to extract zip into each user's file
  - [ CLIENT-SIDE ]Make sure the authentication is enrypted over the network

Stefan
  - Implement tear.py into the main program (using Scapy)
  - Error Handling
    - connection cut off during dispatch()
    - need to write signal handler in client.py

Sylvain
  X configure python environment on server
  X install django
  - graphing app //graphos(flot)
  - workflow management(git)
  - setting up models/db
  X setting up Gunicorn,
  - need to setup NGINX + proper port and setup TLS
  - create and admin
  - figure what else is down the pipeline

Imad
- creating client-side HTML files (login.html and register.html)
  - forms and validation
  - storing information in database (sqlite3)
- creating server-side HTML file (upload.html)
  - making sure it is robust (strictly only accept compressed data - zip files of any format + other requirements)  
