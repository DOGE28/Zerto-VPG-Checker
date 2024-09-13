import zerto as z
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText








class Alerts():

    def __init__(self, location):
        self.location = location
        location_values = ['sgu prod', 'boi prod', 'fb prod', 'sgu inf', 'boi inf', 'okc inf']
        if location not in location_values:
            raise ValueError(f"Invalid location... Please choose from the following: {location_values}")
        self.zerto = z.ZertoGet(location)
        self.site_percent = self.zerto.get_percent_vpgs_up()
        self.zvm_throughput = self.zerto.get_throughput_zvm()
        self.site_throughput = self.zerto.get_throughput_sites()
        self.threshold = 90

    def determine(self):
        problems = []

        ###PROBLEM 1: IS ZVM THROUGHPUT 0?
        if self.zvm_throughput <= 0 and self.location != 'boi inf':
            problems.append(f"ZVM throughput is 0 for {self.location}")

        ###PROBLEM 2: ARE ANY SITE THROUGHPUTS 0?
        for site in self.site_throughput:
            for key, value in site.items():
                if value <= 0:
                    problems.append(f"Site {key} throughput is 0")

        ###PROBLEM 3: ARE ANY SITE VPG PERCENTAGES BELOW THRESHOLD?
        for site in self.site_percent:
            for key, value in site.items():
                if value < self.threshold:
                    problems.append(f"Site {key} has less than {self.threshold}% of VPGs up")

        self.problems = problems
                    

    def send_alert(self):
        if self.problems == []:
            print("No problems detected")
            return
        print("The following problems have been detected:")
        for problem in self.problems:
            print(problem)


class SendEmails(Alerts):
    def __init__(self, location):
        super().__init__(location)
        self.determine()
        self.sender = "systems@tonaquint.com"
        self.receiver = "tsullivan@tonaquint.com"
        self.subject = f"A problem has been detected at the {self.location.upper()} ZVM"
        self.body = f"""This is a test email
        
        The following problems have been detected at the {self.location.upper()} ZVM:

        {self.problems}

        Please investigate immediately!
        """
        self.server = "10.200.201.15"
        self.port = 25

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



sgu_prod = SendEmails('sgu prod')
sgu_prod.send()

boi_prod = SendEmails('boi prod')
boi_prod.send()

fb_prod = SendEmails('fb prod')
fb_prod.send()

sgu_inf = SendEmails('sgu inf')
sgu_inf.send()

#boi_inf = SendEmails('boi inf')
#boi_inf.send()



# try:
#     okc_inf = SendEmails('okc inf')
#     okc_inf.send()
# except ValueError as e:
#     print("You attempted to connect to OKC...")
#     print("You're probably on the VPN and can't connect...")
