import smtplib
import imghdr
from email.message import EmailMessage

PASSWORD = "mxbd pgyh zxvf hudr"
SENDER = "tranquil3477@gmail.com"
RECEIVER = "tranquil3477@gmail.com"


def send_email(image_path):
    print("send_function function started.")
    email_message = EmailMessage()
    email_message["Subject:"] = "New customer showed up"
    email_message.set_content("Hey, we just saw a new customer.")

    # Get image with open method using rb (read binary)
    with open(image_path, "rb") as file:
        content = file.read()

    # Add attachment and use imghdr library to get type of image
    email_message.add_attachment(content, maintype="image",
                                 subtype=imghdr.what(None, content))

    # Create gmail server to send the email
    gmail = smtplib.SMTP("smtp.gmail.com", 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(SENDER, PASSWORD)
    gmail.sendmail(SENDER, RECEIVER, email_message.as_string())
    gmail.quit()
    print("send_email function ended.")


if __name__ == "__main__":
    send_email(image_path="images/19.png")
