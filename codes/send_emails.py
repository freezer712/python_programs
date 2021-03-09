import smtplib
from email.utils import parseaddr, formataddr
from email.header import Header
from email.mime.text import MIMEText






from_addr = 'username<addr>' #sender username and address
to_addr = 'addr1,addr2' #single user can use 'username<addr>'
address = from_addr.split('<')[1].split('>')[0]##sender addr
password = 'password or authorization code'
mail_msg = '''
        your email content
'''

def send_mail():
    msg = MIMEText(mail_msg, 'html', 'utf-8') ## 'plain' for txt and 'html' for html codes
    name, addr = parseaddr(from_addr)
    msg['From'] = formataddr((Header(name, 'utf-8').encode(), addr))
    # name, addr = parseaddr(to_addr)
    # msg["To"] = formataddr((Header(name, 'utf-8').encode(), addr)) # just for single user
    msg['To'] = to_addr
    msg["Subject"] = Header('your email subject', 'utf-8').encode()

    server = smtplib.SMTP_SSL('smtp.qq.com', 465) # 'smtp.qq.com' for qq Mail,and 'smtp.exmail.qq.com' for tencent enterprise email
    server.login(address, password)
    server.set_debuglevel(2)
    server.sendmail(address, to_addr.split(","), msg.as_string())
    #
    server.quit()
    print("Emails sent successfully.")


if __name__ == '__main__':
    send_mail()
