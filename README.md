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

Stefan
  - Check if client loses connection and can't upload
    - send number of packets to server
    - send username, then password, then token (send blank if the client doesn't yet have a token)
      - if the sever has to send you a token recieve it, otherwise skip so it doesn't hang
    - make sure the authentication is enrypted over the network
  - Handle tokens
  - Compatability (i.e. some distro's may or may not have a /var/log/messages. Need to check for that)
  - Error Handling
    - abnormal termination
    - no internet connection
      - connection cut off during dispatch
  - Make the client a service in (/etc/init.d)
  - Implement tear.py in main program
  - Write install script(s)

BTW editing the file is nano will NOT add any spaces, so edit it in another editor, if that doesn't work you can edit it on the website

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
