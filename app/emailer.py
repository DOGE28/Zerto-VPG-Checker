import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import settings

class Email():
    """
    This class is used to send an email to the email address specified in the to_email attribute.
    
    """
    def __init__(self):
        self.from_email = settings.smtp_user
        self.to_email = "tsullivan@tonaquint.com"
        self.subject = "Test Email"
        self.message = "This email is a test to make sure the email functionality is working."
    
    def create_email(self, message:str=None):
        if message:
            self.message = message
        msg = MIMEMultipart()
        #msg['From'] = self.from_email
        msg['To'] = self.to_email
        msg['Subject'] = self.subject
        return msg.attach(MIMEText(self.message, 'plain'))
        
    
    def send_email(self, created_email):
        server = smtplib.SMTP(settings.smtp_server, settings.smtp_port, timeout=120)
        #server.login(self.from_email, settings.smtp_password)
        text = created_email.as_string()
        server.sendmail(created_email, self.to_email, text)
        server.quit()
        

