import zerto as z
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
import threading
from config import settings
import argparse

parser = argparse.ArgumentParser(description='ZVM Monitoring Tool')
parser.add_argument('--test', help='Sends test email', action='store_true')


args = parser.parse_args()


class Alerts():

    def __init__(self):
        self.zerto = z.ZertoGet()
        self.site_percent = self.zerto.get_percent_vpgs_up()
        self.zvm_throughput = self.zerto.get_throughput_zvm()
        self.site_throughput = self.zerto.get_throughput_sites()
        self.threshold = settings.threshold

    def determine(self):
        problems = []

        ###PROBLEM 1: IS ZVM THROUGHPUT 0?
        if self.zvm_throughput <= 0:
            #print(self.zvm_throughput)
            problems.append(f"Total throughput for entire ZVM is 0")

        ###PROBLEM 2: ARE ANY SITE THROUGHPUTS 0?
        for site in self.site_throughput:
            for key, value in site.items():
                if value <= 0:
                    problems.append(f"Site {key} throughput is 0")

        ###PROBLEM 3: ARE ANY SITE VPG PERCENTAGES BELOW THRESHOLD?
        for site in self.site_percent:
            for key, value in site.items():
                if value < self.threshold:
                    problems.append(f"ZVM has less than {self.threshold}% of VPGs up")

        self.problems = problems
                    

    def send_alert(self):
        if self.problems == []:
            print("No problems detected")
            return
        print("The following problems have been detected:")
        for problem in self.problems:
            print(problem)


class SendEmails(Alerts):
    def __init__(self):
        super().__init__()
        self.server = settings.smtp_address
        self.determine()
        self.sender = settings.smtp_sender
        self.receiver = settings.smtp_receiver

        if args.test:
            self.subject = f"Test Email from ZVM Monitoring Tool"
        else:
            self.subject = f"A problem has been detected with your ZVM"

        if args.test:
            self.body = f"""
            This is a test email to verify that the ZVM monitoring tool is working correctly.

            If you have received this email, the tool is working as expected.
            """
        else:
            self.body = f"""
            
            The following problems have been detected with your ZVM:

            {self.problems}

            Please investigate immediately!
            """
        self.port = settings.smtp_port
    
    def get_problems(self):
        return self.problems

    def send(self):
        msg = MIMEMultipart()
        msg['From'] = self.sender
        msg['To'] = self.receiver
        msg['Subject'] = self.subject
        if self.problems == []:
            print("No problems detected")
            return
        else:
            msg.attach(MIMEText(self.body, 'plain'))
            text = msg.as_string()
            server = smtplib.SMTP(self.server, self.port)
            server.sendmail(self.sender, self.receiver, text)
            server.quit()

###Loop Logic
consecutive_problem_count = 0
def monitor(): #Creates a while loop function that can be called to run the monitoring logic indefinitely
    global consecutive_problem_count
    a = 0
    a = int(settings.interval) * 60
    #print(a)
    interval = a

    consecutive_threshold = 3
    while True:

        alert = SendEmails()
        problems = alert.get_problems()

        if problems == []:
            consecutive_problem_count = 0
            print("No problems detected")
        else:

            consecutive_problem_count += 1
            #print(consecutive_problem_count)
            print(f"Problem detected {problems}")

            if consecutive_problem_count >= 0:
                if consecutive_problem_count == consecutive_threshold:
                    alert.send()
                    print(f"Sending alert for ZVM")
                    consecutive_problem_count = 0

        time.sleep(int(interval))


if args.test:
    test = SendEmails()
    test.problems = ["Test email"]
    test.send()
    exit()



zvm_thread = threading.Thread(target=monitor)
zvm_thread.start()
zvm_thread.join()







