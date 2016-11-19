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
  - [ CLIENT-SIDE ]Send username, then password, then token (send blank if the client doesn't yet have a token)
  - [ CLIENT-SIDE ]If the sever has to send you a token recieve it, otherwise skip so it doesn't hang
  - [ CLIENT-SIDE ]Make sure the authentication is enrypted over the network
  - [ CLIENT-SIDE ]Handle tokens

Stefan
  + Continues to collect data when client can't connect
    + added a giftwrap() in collectory.py to zip the entire directory that has all the package(s).zip before sending.
  - Implement tear.py into the main program
  - Compatability (i.e. some distro's may or may not have a /var/log/messages. Need to check for that)
  - Error Handling
    - connection cut off during dispatch()
    - sending/saving packages before system shutdown
  - Make the client a service in (/etc/init.d)
  - Write install script(s)

Sylvain
  - configure python environment on server
  -install django
  - graphing app //graphos(flot)
  - login
  - workflow management(git)
  - setting up models/db
  - figure what else is down the pipeline

Imad
- creating client-side HTML files (login.html and register.html)
  - forms and validation
  - storing information in database (sqlite3)
- creating server-side HTML file (upload.html)
  - making sure it is robust (strictly only accept compressed data - zip files of any format + other requirements)  
