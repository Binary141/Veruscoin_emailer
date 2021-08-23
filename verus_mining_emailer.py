import requests
import json
import smtplib, ssl
from time import sleep

#For the emailer program to work, you will need to create an app password for the gmail account to make it easier to revoke access from your
# account in the future. Google has a guide here: https://support.google.com/mail/answer/185833?hl=en-GB

while True: #this way it will run indefinitely inside of a docker container

#--------------------- Variable declaration
    smtp_server = "smtp.gmail.com"
    port = 587  # For starttls
    sender_email = "example@gmail.com"
    recipient_email = "example@gmail.com"  
    password_email = "APP_PASSWORD"
    miner_wallet = "RNX1d1T5nXvJVx6xy4ifc2kBahXpracX8S" #Verus coin wallet
# Create a secure SSL context
    context = ssl.create_default_context()
    Offline_workers = ""
    Request_URL = "https://luckpool.net/verus/miner/" + miner_wallet #data['miner_details']... is the wallet from the JSON file

#--------------------- End Variable declaration
    for i in requests.get(Request_URL).json()['workers']:
        temp = i.split(':')
        if(temp[3] == "off"):
            print(temp[0])
            Offline_workers += temp[0]
            Offline_workers += ","

    if(Offline_workers != ""): #As long as the list isn't empty, it will run this to send the email
        if(Offline_workers[-1] == ','): #removes trailing comma from the email subject if the list is not empty
            Offline_workers = Offline_workers[:-1]

# Try to log in to server and send email
        try:
            server = smtplib.SMTP(smtp_server,port)
            server.starttls(context=context) # Secure the connection
            server.login(sender_email, password_email)

            #message:
            SUBJECT = "Miner(s) " + Offline_workers + " Is offline"
            TEXT = ""
            message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)

            #send the email
            server.sendmail(sender_email, recipient_email, message)

            print("The email was sent")
        except Exception as e:
            # Print any error messages. Printing will keep the program running in case there is an error
            print(e)
        finally:
            server.quit() 
    else:
        print("No email was sent")

    sleep(900)
