import picamera
import smtplib, ssl, email
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import time
import imaplib
import email
import traceback
from email.header import decode_header
import datetime

smtp_server = "smtp.gmail.com"
sender_email = "<your email"  # Enter your address
receiver_email = "receiveremail"  # Enter receiver address
password = "password"

imap_server = "imap.gmail.com" 
imap_port = 993

def sendMail(listOfEmails):
    camera = picamera.PiCamera()
    time.sleep(2)
    camera.resolution = (800, 600)
    camera.vflip = True
    camera.contrast = 10
    camera.brightness = 65
    camera.capture('/home/vineeth/AquariumMonitor/static/images/aquarium.jpg')
    camera.close()

    subject = "Aquarium Status"
    body = "Check the aquarium"
    port = 465  # For SSL
    
    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = ";".join(listOfEmails)
    message["Subject"] = subject

    # Add body to email
    message.attach(MIMEText(body, "plain"))
    
    filename = "/home/vineeth/AquariumMonitor/static/images/aquarium.jpg"  # In same directory as script
    
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

    # Add attachment to message and convert message to string
    message.attach(part)
    text = message.as_string()
    print("attach file")
    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)

        
def read_email_from_gmail():
    listOfEmails = [ ]
    try:
        mail = imaplib.IMAP4_SSL(imap_server)
        mail.login(sender_email,password)
        mail.select('inbox')

        data = mail.search(None, '(UNSEEN)')
        mail_ids = data[1]
        id_list = mail_ids[0].split()   
        
        print(id_list)
        for i in id_list:
            data = mail.fetch(str(int(i)), '(RFC822)' )
            for response_part in data:
                arr = response_part[0]
                if isinstance(arr, tuple):
                    msg = email.message_from_string(str(arr[1],'utf-8'))
                    email_subject = msg['subject']
                    print(email_subject)
                    email_from = msg['from']
                    if email_subject.lower() == 'sadhanamkayilundo':
                        print(email_from)
                        listOfEmails.append(email_from)
        return listOfEmails
    except Exception as e:
        traceback.print_exc() 
        print(str(e))

while True:
    listOfEmails = read_email_from_gmail()
    print(listOfEmails)
    #curTime = datetime.datetime.now().astimezone()
    #email_date = 'Wed, 21 Dec 2022 20:10:36 +0530'
    #email_d = datetime.datetime.strptime(email_date,"%a, %d %b %Y %H:%M:%S %z")
    print(listOfEmails)
    if listOfEmails:
        sendMail(listOfEmails)
    time.sleep(30)
