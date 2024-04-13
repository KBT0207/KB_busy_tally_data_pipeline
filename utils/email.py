import logging
import os
import schedule
import time
from datetime import datetime
from dotenv import load_dotenv
import yagmail


load_dotenv()


yag = yagmail.SMTP("jovokb@gmail.com", 
                   os.getenv('SENDER_EMAIL_PASSWORD')) 
# Adding Content and sending it 


def email_send(reciever, cc = None, bcc = None, subject=None, contents= None, attachemnts=None):
    yag.send(to= reciever, 
             cc= cc ,
             bcc= bcc, 
             subject = subject, 
             contents= contents, 
             attachments= attachemnts)

                

class YagmailHandler(logging.Handler):
    def __init__(self, to, subject, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.to = to
        self.subject = subject

    def emit(self, record):
        log_entry = self.format(record)
        #yag = yagmail.SMTP("jovokb@gmail.com", os.getenv('SENDER_EMAIL_PASSWORD')) 
        yag.send(to=self.to, subject=self.subject, contents=log_entry)


class YagmailDailyHandler(logging.Handler):
    def __init__(self, to, subject, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.to = to
        self.subject = subject
        self.last_emailed_date = None

    def emit(self, record):
        log_entry = self.format(record)
        now = datetime.now()
        if self.last_emailed_date is None or now.date() != self.last_emailed_date:
            #yag = yagmail.SMTP("jovokb@gmail.com", os.getenv('SENDER_EMAIL_PASSWORD')) 
            yag.send(to=self.to, subject=self.subject, contents=log_entry)
            self.last_emailed_date = now.date()


