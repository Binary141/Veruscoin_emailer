import requests
import json
import smtplib, ssl
from time import sleep

while True:

#--------------------- Variable declaration
    f = open('config.json')

    data = json.load(f)

    smtp_server = "smtp.gmail.com"
    port = 587  # For starttls
    sender_email = data['email_details'][0]['sender_email']
    recipient_email = data['email_details'][0]['recipient_email'] 
    password_email = data['email_details'][0]['email_password']

# Create a secure SSL context
    context = ssl.create_default_context()

    Active_worker_list = []
    Offline_workers = ""

    Request_URL = "https://luckpool.net/verus/miner/" + data['miner_details'][0]['miner_wallet'] #data['miner_details']... is the wallet from the JSON file

    miners = data['miner_details'][0]['miner_name'].split()
#compare this list to the list that is returned in the get request
#--------------------- End Variable declaration


    for i in requests.get(Request_URL).json()['workers']:
        temp = ""
        for letter in range(len(i)):
            if i[letter] != ":":
                temp += i[letter]
            else:
                Active_worker_list.append(temp)
                break

    for worker in miners:
        if worker not in Active_worker_list:
            Offline_workers += worker
            #can check to see if the worker is being picked up as offline
            #print(worker, " Not working")
    if(Offline_workers != ""):
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
            # Print any error messages
            print(e)
        finally:
            server.quit() 
    else:
        print("No email was sent")

    f.close()
    sleep(900)
