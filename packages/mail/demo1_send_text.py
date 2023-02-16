if __name__ == '__main__':
    import smtplib
    from email.mime.text import MIMEText


    def send_email(subject, body, sender, recipients, password):
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = ', '.join(recipients)
        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_server.login(sender, password)
        smtp_server.sendmail(sender, recipients, msg.as_string())
        smtp_server.quit()


    subject = "Email Subject"
    body = "This is the body of the text message"
    sender = "shawninjuly@gmail.com"
    password = "zjwigxgruzvgmfaw"  # google 应用专用密码！, ref: https://myaccount.google.com/apppasswords?pli=1&rapt=AEjHL4OCKSPTpmzjxIQv7oe8s6mbw7OdIUuDZJzV1Cl7cnfoXMLPp_8vb8eFOFu_fCH0qRntGfaH7Sl351UoHMEIchb5GpteLg
    recipients = ["877210964@qq.com"]
    send_email(subject, body, sender, recipients, password)
