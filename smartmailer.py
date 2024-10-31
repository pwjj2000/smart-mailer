import sys, os
import numpy as np
import pandas as pd

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
    subject, body = email_contents[0], email_contents[1:]

# Establish SMTP connection and send email
def send_email():
    pass

if __name__ == "__main__":
    dept = sys.argv[1]
    maildata_df, email_contents = setup(dept)

    # Iterate over each row that we need to send email to
    for _, row in maildata_df.iterrows():
        # Parse information from row
        email, name, department = row['EMAIL'], row['NAME'], row['DEPARTMENT']
        prepare_email(email_contents, email, name, department)

        

    
