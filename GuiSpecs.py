import os
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

# initialize connection to our email server
email = str(input("Enter your email address: "))
password = str(input("Enter your password: "))
subject = str(input("Enter the subject: "))
text = str(input("Enter the message text: "))  # Message to send
print("---You can only send to a maximum of 10 recipients at a time.---")
to = []
count = 0
while count < 10:
    recipient = str(input("Enter a recipient's address: "))
    if recipient != "":
        to.append(recipient)
        count += 1
    else:
        print(f"list completed successfully. Sending to:\n{to}\n...")
        break
else:
    print(f"list completed successfully. Sending to:\n{to}")
smtp = smtplib.SMTP('smtp.gmail.com', 587)
smtp.ehlo()
smtp.starttls()

try:
    smtp.login(email, password)  # Login with your email and password
except Exception as error:
    print(error)


# send our email message 'msg' to our boss
def message(img=None, attachment=None):
    msg = MIMEMultipart()  # build message contents
    msg['Subject'] = subject  # Add Subject
    msg.attach(MIMEText(text))  # Add text contents
    if img is not None:  # Check if we have anything given in the img parameter
        if type(img) is not list:  # Check whether we have the lists of images or not!
            img = [img]  # if it isn't a list, make it one

        for one_img in img:  # Now iterate through our list
            img_data = open(one_img, 'rb').read()  # read the image binary data
            # Attach the image data to MIMEMultipart
            # using MIMEImage, we add the given filename use os.basename
            msg.attach(MIMEImage(img_data, name=os.path.basename(one_img)))

    if attachment is not None:  # We do the same for attachments as we did for images
        if type(attachment) is not list:  # Check whether we have the lists of attachments or not!
            attachment = [attachment]  # if it isn't a list, make it one

        for one_attachment in attachment:
            with open(one_attachment, 'rb') as f:
                file = MIMEApplication(f.read(), name=os.path.basename(one_attachment))
            # Read in the attachment using MIMEApplication
            file['Content-Disposition'] = f'attachment; \
            filename="{os.path.basename(one_attachment)}"'
    msg.attach(file)  # At last, Add the attachment to our message object
    return msg


message()
try:
    for address in to:  # Provide some data to the sendmail function!
        smtp.sendmail(from_addr=email, to_addrs=address, msg=msg)
except Exception as e:
    print(e)
finally:
    smtp.quit()  # Finally, don't forget to close the connection
