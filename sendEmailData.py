[btctomcat@vpnnat sendEmailScript]$ cat sendEmailData.py
#!/usr/bin/python

import smtplib, getopt, sys
import argparse
from email.MIMEMultipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders
import os, socket

def sendGmail(fromUser, toAddr, subject, text, cc=None, bcc=None, reply_to=None, attach=None,
         html=None, pre=False, custom_headers=None, useGmail=False, gmail_user=None, gmail_pwd=None):
    msg = MIMEMultipart()

    dummyFrom = ''
    if gmail_user:
        dummyFrom = ' <' + fromUser + '>'
    msg['From'] = fromUser + dummyFrom
    msg['Subject'] = subject

    to = []

    if toAddr:
        # To gets added to the text header as well as list of recipients
        toAddr = toAddr.split(',')
        toAddrTemp = ', '.join(toAddr)
        msg.add_header('To', toAddrTemp)
        to += toAddr

    if cc:
        # cc gets added to the text header as well as list of recipients
        cc = cc.split(',')
        ccTemp = ', '.join(cc)
        msg.add_header('Cc', ccTemp)
        to += cc

    if bcc:
        bcc = bcc.split(',')
        # bcc does not get added to the headers, but is a recipient
        to += bcc

    if reply_to:
        msg.add_header('Reply-To', reply_to)

    # Encapsulate the plain and HTML versions of the message body in an
    # 'alternative' part, so message agents can decide which they want to
    # display.

    text += "\n-----------------------------------------\n" + socket.gethostname() + "\n-----------------------------------------\n"

    if pre:
        html = "%s" % text
    if html:
        msgAlternative = MIMEMultipart('alternative')
        msg.attach(msgAlternative)

        msgText = MIMEText(text)
        msgAlternative.attach(msgText)

        # We reference the image in the IMG SRC attribute by the ID we give it
        # below
        msgText = MIMEText(html, 'html')
        msgAlternative.attach(msgText)
    else:
        msg.attach(MIMEText(text))

    if attach:
        attach = attach.split(',')
        attList = []
        attList += attach

        for i, attName in enumerate(attList):
            part = MIMEApplication(open(attName).read())
            part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(attName))
            msg.attach(part)


    if custom_headers:
        for k, v in custom_headers.iteritems():
            msg.add_header(k, v)


    if useGmail == 'True':
        mailServer = smtplib.SMTP("smtp.gmail.com:25")
        mailServer.ehlo()
        mailServer.starttls()
        mailServer.login(gmail_user, gmail_pwd)
    else:
        mailServer = smtplib.SMTP("smtp.idmission.com")

    mailServer.sendmail(fromUser, to, msg.as_string())
    # Should be mailServer.quit(), but that crashes...
    mailServer.close()

def main():
    parser = argparse.ArgumentParser(description='Send email')
    parser.add_argument("-f", dest = "fromAddr", help = "From Address", default = "from@al.com")
    parser.add_argument("-t", dest = "toAddr", help = "To Address", default = None)
    parser.add_argument("-c", dest = "ccAddr", help = "CC Address", default = None)
    parser.add_argument("-bcc", dest = "bccAddr", help = "Bcc Address", default = None)
    parser.add_argument("-s", dest = "subject", help = "Mail Subject", default = "This is a test subject.")
    parser.add_argument("-m", dest = "message", help = "Mail Body", default = "This is a test mail body.")
    parser.add_argument("-mf", dest="messageFile", type=str, help="Mail Body from this file", default=None)
    parser.add_argument("-a", dest = "attachments", help = "Mail Attachments", default = None)
    parser.add_argument("-r", dest = "replyToAddr", help = "Reply To", default = None)
    parser.add_argument("-ug", dest = "useGmail", help = "Use Gmail Flag", default = False)
    parser.add_argument("-gL", dest = "gmailLogin", help = "Gmail Login id", default = None)
    parser.add_argument("-gP", dest = "gmailPassword", help = "Gmail Password", default = None)

    args = parser.parse_args()

    if args.messageFile:
        args.message = open(args.messageFile).read();


    sendGmail(fromUser = args.fromAddr, toAddr = args.toAddr, subject = args.subject, text = args.message,
        cc = args.ccAddr, bcc = args.bccAddr, reply_to = args.replyToAddr, attach = args.attachments,
        html = None, pre = True, custom_headers = None, useGmail=args.useGmail, gmail_user=args.gmailLogin, gmail_pwd=args.gmailPassword)

if __name__ == "__main__":
    main();



