'''A Function to send mail from the SMTP servers.
The set server is of gmail , any other server can be uses by updating the variable smtp_server.
Before use:
1. Add your mail id in the sender_email variable and its password will be asked on the run.
2. Can hard cod ethe password in the commend password variable. Avoid this way for better security.
'''

import smtplib, ssl
import getpass
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from os.path import basename
from email import encoders

'''
Input:
message: A string to be mail in the body.
to: List of string with the mail ids to send the mail.
subject: A string to be added in subject.
attachments: A list of path of the files to be attached from your system.
'''
def send_mail(message,to,subject ="",attachment_file_list=[]):
    port = 587  # For starttls
    smtp_server = "smtp.gmail.com"
    sender_email = "your.mail.id@gmail.com"
    receiver_email = to
    # This will prompt you to enter the password.
    password = getpass.getpass("Type your password and press enter:")
    # The below line can be used to save the password.Please ignore it for better security. Can use if you are using the function locally.
#    password="your_password"

    m = MIMEMultipart()
    m["To"] = ', '.join(receiver_email)
    m["Subject"] = subject
    # m["Bcc"] = receiver_email  # Recommended for mass emails
    # Add body to email
    m.attach(MIMEText(message, "plain"))

# Open file in binary mode
    for filename in attachment_file_list:
            with open(filename, "rb") as attachment:
                # Add file as application/octet-stream
                # Email client can usually download this automatically as attachment
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                file_name = filename.split("/")[-1]
                part.add_header(
                    "Content-Disposition",
                    f"attachment; filename= {file_name}",
                )

                # Add attachment to message and convert message to string
                m.attach(part)


    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
#         server.sendmail(sender_email, receiver_email, message)
        server.sendmail(sender_email, receiver_email, m.as_string())
