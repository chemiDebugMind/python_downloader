from email.message import EmailMessage
import ssl
import smtplib
email_sender = 'tenzinchemi50@gmail.com'
email_password = '..'
email_receiver = 'passangchemi@gmail.com'


subject = 'testing'
body ="""
    Testing it 
"""

em = EmailMessage()

em['from']  = email_sender
em['to'] = email_receiver
em['subject'] = subject

em.set_content(body)

context = ssl.create_default_context()

with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
    smtp.login(email_sender, email_password)
    smtp.sendmail(email_sender, email_receiver, em.as_string())
