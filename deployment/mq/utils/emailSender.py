# -*- coding: utf-8 -*-

import os.path
import sys

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE
from email.MIMEBase import MIMEBase
from email.MIMEImage import MIMEImage
from email import Encoders

class EmailSender(object):
    def __init__(self):
        #reload(sys) 
        #sys.setdefaultencoding('gb2312')

        self.smtpServer = configs.Email_SMTP
        self.username = configs.Email_UserName
        self.password = configs.Email_Password
        self.supportHTML = configs.Email_SupportHTML
        self.supportAttach = configs.Email_SupportAttachment
        
    def _replaceImages(self, imgPath, msgRoot):
        try:
            fp = open(imgPath, 'rb')
            img = MIMEImage(fp.read())
            fp.close()
            imgId = os.path.basename(imgPath).replace('.jpg','').replace('.gif','')
            img.add_header('Content-ID', '<%s>' % imgId)
            msgRoot.attach(img)
        except:
            pass
        
    def SendEmail(self, subject, senderEmail, senderDisplayName, toEmail, emailContent, attachment, htmlImagesArr_replaced = None):
        msgRoot = MIMEMultipart()
        msgRoot['Subject'] = subject
        msgRoot['From'] = senderDisplayName
        
        if type(toEmail) == list:
            msgRoot['To'] = COMMASPACE.join(toEmail)
        else:
            msgRoot['To'] = toEmail
        
        msgAlternative = MIMEMultipart()
        msgRoot.attach(msgAlternative)
        
        if self.supportHTML:
            msgContent = MIMEText(emailContent, 'html', 'utf-8')
            msgAlternative.attach(msgContent)
        else:
            msgContent = MIMEText(emailContent, 'text', 'utf-8')
            msgAlternative.attach(msgContent)
        
        try:
            if self.supportAttach and attachment <> None:
                if type(attachment) == list:
                    for file in attachment:
                        objFile = open(file, 'rb')
                        attachmentContent = objFile.read()
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(attachmentContent)
                        objFile.close()
                        
                        Encoders.encode_base64(part)
                        part.add_header('Content-Disposition', 'attachment; filename=%s' % os.path.basename(file))
                        msgRoot.attach(part)
                else:
                    objFile = open(attachment, 'rb')
                    attachmentContent = objFile.read()
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachmentContent)
                    objFile.close()
                        
                    Encoders.encode_base64(part)
                    part.add_header('Content-Disposition', 'attachment; filename=%s' % os.path.basename(attachment))
                    msgRoot.attach(part)
        except:
            print >> sys.stdout, 'Error: can not attach one or all files.'
            
        if htmlImagesArr_replaced <> None:
            for img in htmlImagesArr_replaced:
                self._replaceImages(img, msgRoot)
        
        try:
           smtp = smtplib.SMTP()
           smtp.connect(self.smtpServer)
           smtp.login(self.username, self.password)
           smtp.sendmail(senderEmail, toEmail, msgRoot.as_string())
           
           print >> sys.stdout, "[OK]--Email sent to: %r" % toEmail
        except Exception,e:
            print >> sys.stdout, 'Error: Can not send email!'  
        