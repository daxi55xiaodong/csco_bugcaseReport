import os,sys,time,datetime
import os.path
import base64
import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders

class Mail():
    def __init__(self,file_name):
        self.filename = file_name
        self.fromx = 'smarttools.cisco.com'
        self.to = 'jobai@cisco.com'

    def write_email(self):
        msg = MIMEMultipart()
        msg['Subject'] = 'Weekly BUG-CASE Check For PSS-SNTC (BETA)'
        msg['From'] = 'smarttools@cisco.com'
        msg['To']   = 'jobai@cisco.com'
        msg.preamble = 'weekly report'

        fp = open(self.filename, 'rb')
        xls = MIMEBase('application','vnd.ms-excel')
        xls.set_payload(fp.read())
        fp.close()
        encoders.encode_base64(xls)
        xls.add_header('Content-Disposition', 'attachment', filename=filename)
        msg.attach(xls)

        mail_content = '''
        <html><body><p>Hi Team,</p> \n <p>Please refer to the attachment for details</p> \n<p>Thanks & BR</p> \n<p>Smart service support team</p> \n</body></html>
        '''

        msg.attach(MIMEText(mail_content, 'html'))

        s = smtplib.SMTP('outbound.cisco.com:25')
        s.ehlo
        s.sendmail(self.fromx,self.to,msg.as_string())
        s.close()

if __name__ == '__main__':
    pathname = os.path.dirname(sys.argv[0])
    date=datetime.date.today()
    filename=os.path.join(pathname,"%s-bugReport.xls")%date
    new_mail = Mail(filename)
    new_mail.write_email()
