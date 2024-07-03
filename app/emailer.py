import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import settings

class Email():
    def __init__(self):
        self.from_email = settings.smtp_user
        self.to_email = ""
        self.subject = "Test Email"
        self.message = "This email is a test to make sure the email functionality is working."
    
    def create_email(self):
        msg = MIMEMultipart()
        msg['From'] = self.from_email
        msg['To'] = self.to_email
        msg['Subject'] = self.subject
        return msg.attach(MIMEText(self.message, 'plain'))
        
    
    def send_email(self, created_email):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(self.from_email, "password")
        text = created_email.as_string()
        server.sendmail(created_email, self.to_email, text)
        server.quit()
        

