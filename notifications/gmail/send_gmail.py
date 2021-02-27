"""
This is for the reference on how to send gmail using PYTHON

use quickstart gmail API for allowing apps to send emails 

less secure option would be to enable that option for short term 

"""


import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# Start smtp server local using below
# python -m smtpd -c DebuggingServer -n localhost:1025

# Turn off less secure https://myaccount.google.com/lesssecureapps

port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = "sample gmail.com"
password = input("Enter Your Password")
receiver_email = "sample gmail.com"

message = MIMEMultipart("alternative")
message["Subject"] = "multipart test"
message["From"] = sender_email
message["To"] = receiver_email

# Create the plain-text and HTML version of your message
text = """\
Hi,
How are you?
"""
html = """\
<html>
  <body>
    <p>Hi,<br>
       How are you?<br>
    </p>
  </body>
</html>
"""
filename = 'document.pdf'
# Open PDF file in binary mode
with open(filename, "rb") as attachment:
    # Add file as application/octet-stream
    # Email client can usually download this automatically as attachment
    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment.read())

# Encode file in ASCII characters to send by email    
encoders.encode_base64(part)

# Add header as key/value pair to attachment part
part.add_header(
    "Content-Disposition",
    f"attachment; filename= {filename}",
)



# Turn these into plain/html MIMEText objects
part1 = MIMEText(text, "plain")
part2 = MIMEText(html, "html")

# Add HTML/plain-text parts to MIMEMultipart message
# The email client will try to render the last part first
message.attach(part1)
message.attach(part2)

# Add attachment to message and convert message to string
message.attach(part)

# Create secure connection with server and send email
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(
        sender_email, receiver_email, message.as_string()
    )