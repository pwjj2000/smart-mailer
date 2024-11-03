import sys, os
import numpy as np
import pandas as pd
import smtplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


SENDER_EMAIL = '' #Add email
SENDER_PASSWORD = '' #Add password
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
BODY_PLACEHOLDER = '#name#'
DEPARTMENT_PLACEHOLDER = '#department#'
DELAY = 1
    

# Setup required information/data.
def setup(dept):
    # Load maildata.csv and select data from selected department only
    curr_dir = os.path.dirname(os.path.realpath(__file__))
    csv_filename = os.path.join(curr_dir, 'maildata.csv')
    maildata_df = pd.read_csv(csv_filename)
    if dept != 'all':
        maildata_df = maildata_df[maildata_df['DEPARTMENT'] == dept]
    maildata_df.reset_index()

    # Load email.txt
    txt_filename = os.path.join(curr_dir, 'email.txt')
    with open(txt_filename, 'r') as f:
        email_contents = f.readlines()
        
    return maildata_df, email_contents

# Prepare email contents based on subject and body information from mail.txt
def prepare_email(email_contents, email, name, department):
    subject = email_contents[0].strip() 
    body = "".join(email_contents[1:]).strip() 

    # Replace placeholders with actual values
    body = body.replace(BODY_PLACEHOLDER, name).replace(DEPARTMENT_PLACEHOLDER, department)
    return subject, body

# Establish SMTP connection and send email
def send_email(subject, body, receiver):
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL
    msg['To'] = receiver
    msg.attach(MIMEText(body, 'html'))
    s.sendmail(SENDER_EMAIL, receiver, msg.as_string())

    

if __name__ == "__main__":
    dept = sys.argv[1]
    maildata_df, email_contents = setup(dept)

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as s:
        s.starttls()
        s.login(SENDER_EMAIL, SENDER_PASSWORD)
        # Iterate over each row that we need to send email to
        for _, row in maildata_df.iterrows():
            # Parse information from row
            email, name, department = row['EMAIL'], row['NAME'], row['DEPARTMENT']
            subject, body = prepare_email(email_contents, email, name, department)
            send_email(subject, body, email)
            time.sleep(DELAY)
        

    
