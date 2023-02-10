from email import encoders
from email.mime.base import MIMEBase
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from ReadConfig import readconfig


port = readconfig("MAIL", option="PORT")
smtp_server = readconfig("MAIL", option="SERVER")
login = readconfig("MAIL", option="MSG_FROM")
password = readconfig("MAIL", option="PASSWD")
sender_email = readconfig("MAIL", option="MSG_FROM")
receiver_email = readconfig("MAIL", option="MSG_TO")


def main(args):
    message = MIMEMultipart("alternative")
    message["Subject"] = "JIRA bug tracking"
    message["From"] = sender_email
    message["To"] = receiver_email

    # Add body to email
    body = "this is jira bug tracking report"
    message.attach(MIMEText(body, "plain"))

    filename = "./result/sprint" + args[0] + ".html"
    # Open PDF file in binary mode

    # We assume that the file is in the directory where you run your Python script from
    with open(filename, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Encode to base64
    encoders.encode_base64(part)

    # Add header
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )

    # Add attachment to your message and convert it to string
    message.attach(part)

    filename2 = "./result/sprint" + args[0] + ".txt"
    # Open PDF file in binary mode

    # We assume that the file is in the directory where you run your Python script from
    with open(filename2, "rb") as attachment:
        # The content type "application/octet-stream" means that a MIME attachment is a binary file
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Encode to base64
    encoders.encode_base64(part)

    # Add header
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename2}",
    )

    # Add attachment to your message and convert it to string
    message.attach(part)
    text = message.as_string()

    # send your email
    try:
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls()
            server.login(login, password)
            server.sendmail(
                sender_email, receiver_email, message.as_string()
            )
        print("Successfully sent email")
    except smtplib.SMTPException:
        print("Error: unable to send email")
