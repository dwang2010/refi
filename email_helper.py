# helper class to simplify email related tasks

import smtplib
from email.message import EmailMessage

class EmailHelper:
    def __init__(self):
        self.server = None

    # login to e-mail server (google gmail)
    def login(self, user, pwd):
        try:
            self.server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            self.server.ehlo()
            self.server.login(user, pwd)
        except:
            print ("failed to login to e-mail server")

    # send email message
    def send(self, src, dest, msg):
        if self.server:
            self.server.sendmail(src, [dest], msg.as_string())

    # terminate connection to server
    def close(self):
        if self.server:
            self.server.quit()
