# Section-9-SIEM
SIEM for Software Engineering

Things to work on:

Ryan
  - Error checking
    - If file is a proper zip file
    - If login credentials are correct
    - If token ID is correct
    - If there are error creating or opening the file
  - Create user authentication system
  - Organize filesystem to extract zip into each user's file

Stefan
  - Compatability (i.e. some distro's may or may not have a /var/log/messages. Need to check for that)
  - Error Handling
    - abnormal termination
    - no internet connection
      - connection cut off during dispatch
      
  - Make the client a service in (/etc/init.d)
  - Implement tear.py in main program
  - Write install script(s)

BTW editing the file is nano will NOT add any spaces, so edit it in another editor, if that doesn't work you can edit it on the website
