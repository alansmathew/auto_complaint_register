import smtplib
import requests
import datetime
import time
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sys
sys.path.insert(0,'/Users/alansmathew/Desktop/confidential/')
from password import pas, username, myemailID, ISPmailID #password internetusername personalmail ispmail
from signature import sig

no_connection_time = datetime.datetime.today()
connection_back_on_time = datetime.datetime.today()

all_time_log = open("all_time_log.txt","a+")
all_time_log.close()

current_log = open("current_log.txt","a+")
current_log.truncate(0)
current_log.close()


def save_current_log(action):
    time_date = datetime.datetime.today()
    current_log = open("current_log.txt","a+")
    if (action=="start"):
        global no_connection_time
        no_connection_time = time_date
    else:
        global connection_back_on_time
        connection_back_on_time = time_date
    text=action+" "+str(time_date)+"\n"
    current_log.write(text)
    current_log.close()
    return

def send_email():
    global no_connection_time,connection_back_on_time
    down_time = str(connection_back_on_time - no_connection_time)[:-7]
    count=1
    data = ""
    with open("all_time_log.txt","r") as f: data = f.readlines()
    if data: count=int(data[-1].split()[0])+1
    print("\n" + str(count) + " " +  str(no_connection_time)[:-7] + " " + str(connection_back_on_time)[:-7] + " " + down_time)
    with open("all_time_log.txt","a+") as f: f.write(log_text)
    email_text="To whom it may concern,<br> <br>&emsp; &emsp; I'm hereby writing this email to convey the complaint that, Den Internet Network was down for a time period of <b>"\
        + str(no_connection_time)[:-7] + " to " + str(connection_back_on_time)[:-7] + "</b> for almost <b>" + down_time + "</b> under the branch Ponkunnam (Ph: 9447038086), Champapthal (Ph: 9496160401)."\
            + " Looking forward for better connections !<br><br> username:" + username + "<br><br><br> " + sig
    
    s = smtplib.SMTP('smtp.gmail.com', 587) 
    s.starttls() 
    s.login(myemailID, pas) 
    msg = MIMEMultipart()
    msg["Subject"] = "No Internet | complaint number " + str(count)
    text = MIMEText(email_text, "html")
    msg.attach(text)
    s.sendmail(myemailID, ISPmailID, msg.as_string()) 
    s.quit()
    print(count," Email sent")

def check_connection(host='http://google.com'):
    try:
        requests.get(host,timeout=2)
        current_log=open("current_log.txt","r")
        last_string="".join(list(current_log.readlines()))
        if(last_string.find("stop")<0 and last_string != ""):
            save_current_log("stop")
            send_email()
            current_log = open("current_log.txt","a+")
            current_log.truncate(0)
            current_log.close()

    except:
        current_log=open("current_log.txt","r")
        last_string= "".join(list(current_log.readlines()))
        if(last_string == ""):
            save_current_log("start")       

while(1):
    time.sleep(1.5)
    check_connection()
