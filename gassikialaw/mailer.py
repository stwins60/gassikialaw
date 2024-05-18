import smtplib
from dotenv import load_dotenv
import os
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

load_dotenv()
logging.basicConfig(level=logging.INFO)

USERNAME = os.getenv('EMAIL')
SERVER = os.getenv('SERVER')
SERVER_PASS = os.getenv('SERVER_PASS')
PORT = os.getenv('PORT')

def sendMyEmail(sender_email, receiver_email, subject, msg):
    try:
        server = smtplib.SMTP_SSL(SERVER, PORT)
        server.ehlo()
        server.login(USERNAME, SERVER_PASS)
        print('Connected to server')
        part = MIMEText(msg, 'html')
        message = MIMEMultipart('alternative')
        message['Subject'] = subject
        message['From'] = sender_email
        message['To'] = receiver_email
        message.attach(part)
        # sender_email = "gassikialaw@gmail.com"
        # receiver_email = 'gassikialaw@gmail.com'
        # message = 'From: {}\nTo: {}\nSubject: {}\n\n{}'.format(sender_email, receiver_email, subject, msg)
        # message = 'From: {}\nTo: {}\nSubject: {}\n\n{}'.format(sender_email, receiver_email, 'Test', 'This is a test email')
        server.sendmail(sender_email, receiver_email, message.as_string())
        print('Email sent successfully')
        logging.INFO('Email sent succesfully')
    except Exception as e:
        print(e)
        print('Failed to connect to server')