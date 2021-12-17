import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def email_pwrs(code):
    sender_email = "jfusion3601@gmail.com"
    receiver_email = "joshua.hy.chans@gmail.com"
    password = "jfusion122404"

    message = MIMEMultipart("alternative")
    message["Subject"] = "Master Password Change"
    message["From"] = sender_email
    message["To"] = receiver_email

    # Create the plain-text and HTML version of your message
    text = f"""\
    Josh,

    A master password reset has been requested. If you did not request this change, delete this email immediately.

    Else, please use the verification code below to verify your identity.

    {code}

    Once you have verified your identity, delete this email.

    Your security access key will be changed accordingly, and your data will be re-encrypted.


    Regards,

    Security Detail
    """
    html = f"""\
    <p>&nbsp;</p>
    <p>Josh,</p>
    <p><span style="--darkreader-inline-bgcolor: #29297a;">A <strong>master password</strong> reset has been requested. If you did not request this change, delete this email immediately.</span></p>
    <p>Else, please use the verification code below to verify your identity.</p>
    <hr />
    <h1 style="text-align: center;"><span style="color: #ff9900;">{code}</span></h1>
    <hr />
    <p style="text-align: left;">Once you have verified your identity, delete this email.</p>
    <p style="text-align: left;">Your security access key will be changed accordingly, and your data will be re-encrypted.</p>
    <p style="text-align: left;">&nbsp;</p>
    <p style="text-align: left;">Regards,</p>
    <p style="text-align: left;">Security Detail</p>
    """

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )
