import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import uuid
from .models import ResetPassword, Profile
from django.contrib.auth.models import User


def send_gmail(receiver_address):
    sender_address = 'deviceshopecommerce@gmail.com'
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'Reset your password'
    id = uuid.uuid4()
    mail_content = f'Open this link to reset your password: http://127.0.0.1:8000/change_password/{id}'  # Xabar matni
    message.attach(MIMEText(mail_content, 'plain'))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_address, "tmgg xxvr uxyn rzxz")
    text = message.as_string()
    server.sendmail(sender_address, receiver_address, text)
    server.quit()
    if User.objects.filter(email=receiver_address).exists():
        user = User.objects.get(email=receiver_address)
        if not ResetPassword.objects.filter(user=user).exists():
            ResetPassword.objects.create(url=id, user=user)
    else:
        return 'User with this email not found' 
    return None
