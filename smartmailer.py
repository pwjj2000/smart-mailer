import sys, os, re
import numpy as np
import pandas as pd
import smtplib
import time
from tabulate import tabulate
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


SENDER_EMAIL = '' #Add email
SENDER_PASSWORD = '' #Add password
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
BODY_PLACEHOLDER = '#name#'
DEPARTMENT_PLACEHOLDER = '#department#'
DELAY = 1
EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

# Setup required information/data.
def setup(dept):
    # Load maildata.csv and select data from selected department only
    curr_dir = os.path.dirname(os.path.realpath(__file__))
    csv_filename = os.path.join(curr_dir, 'maildata.csv')
    maildata_df = pd.read_csv(csv_filename)
    
    # Counter that keeps track of emails sent for each department
    count = {d: 0 for d in set(maildata_df['DEPARTMENT'].values)}

    if dept != 'all':
        maildata_df = maildata_df[maildata_df['DEPARTMENT'] == dept]
    maildata_df.reset_index()

    # Check email addresses' validity
    for _, row in maildata_df.iterrows():
        # Parse information from row
        email = row['EMAIL']
        if not is_valid_email(email):
            print(f'{email} is not a valid email. Edit the csv file and try again.')
            exit()

    # Load email.txt
    txt_filename = os.path.join(curr_dir, 'email.txt')
    with open(txt_filename, 'r') as f:
        email_contents = f.readlines()
        
    return maildata_df, email_contents, count

# Check if email address is valid or not
def is_valid_email(email):
    return re.match(EMAIL_REGEX, email)

# Prepare email contents based on subject and body information from mail.txt
def prepare_email(email_contents, email, name, department):
    subject = email_contents[0].strip() 
    body = "".join(email_contents[1:]).strip() 

    # Replace placeholders with actual values
    body = body.replace(BODY_PLACEHOLDER, name).replace(DEPARTMENT_PLACEHOLDER, department)
    return subject, body

# Establish SMTP connection and send email
def send_email(s, subject, body, receiver):
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL
    msg['To'] = receiver
    msg.attach(MIMEText(body, 'html'))
    s.sendmail(SENDER_EMAIL, receiver, msg.as_string())

    

if __name__ == "__main__":
    dept = sys.argv[1]
    maildata_df, email_contents, count = setup(dept)

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as s:
        s.starttls()
        s.login(SENDER_EMAIL, SENDER_PASSWORD)
        # Iterate over each row that we need to send email to
        for _, row in maildata_df.iterrows():
            # Parse information from row
            email, name, department = row['EMAIL'], row['NAME'], row['DEPARTMENT']
            subject, body = prepare_email(email_contents, email, name, department)
            send_email(s, subject, body, email)
            count[department] += 1
            time.sleep(DELAY)

    table = tabulate(count.items(), headers=['Department', 'Count'])

    print('Number of emails sent (by Department):')
    print(table)