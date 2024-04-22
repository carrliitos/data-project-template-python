import os
import smtplib
import string
import sys

from configobj import ConfigObj
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate

def send_with_attachment(msg, file):
    """
    Add attachment to email
    """

    filetosend = os.path.basename(file)
    header = 'Content-Disposition', 'attachment; filename="%s"' % filetosend
    attachment = MIMEBase('application', "octet-stream")

    try:
        with open(file, "rb") as fh:
            data = fh.read()
        attachment.set_payload(data)
        encoders.encode_base64(attachment)
        attachment.add_header(*header)
        msg.attach(attachment)
    except IOError:
        msg = f"Error opening attachment file {file}"
        print(msg)
        sys.exit(1)

    return msg

def send_email(subject, body_text, to_emails, 
                cc_emails, bcc_emails, file_to_attach):
    """
    Send email
    """

    base_path = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_path, "config/emailconfig.ini")
    
    # get the config
    if os.path.exists(config_path):
        cfg = ConfigObj(config_path)
        cfg_dict = cfg.dict()
    else:
        print("Config not found! Exiting!")
        sys.exit(1)
        
    # extract server and from_addr from config
    host = cfg_dict["smtp"]["server"]
    from_addr = cfg_dict["smtp"]["from_addr"]
    port = cfg_dict["smtp"]["port"]
    uid = cfg_dict["smtp"]["uid"]
    pwd = cfg_dict["smtp"]["pwd"]
    
    # create the message
    msg = MIMEMultipart()
    msg["From"] = from_addr
    msg["Subject"] = subject
    msg["Date"] = formatdate(localtime=True)
    if body_text:
        msg.attach( MIMEText(body_text) )
    
    msg["To"] = ', '.join(to_emails)
    msg["cc"] = ', '.join(cc_emails)
    
    if file_to_attach:
        send_with_attachment(msg, file_to_attach)
    
    emails = to_emails + cc_emails
    
    server = smtplib.SMTP(host, port)
    server.ehlo()
    server.starttls()
    server.login(uid, pwd)
    server.sendmail(from_addr, emails, msg.as_string())
    server.quit()
    