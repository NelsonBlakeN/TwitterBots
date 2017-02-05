import urllib2
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Use regex to find all links. Keep increading number in pattern (HW1, 2, etc)
# up to 5 until there is no match. If there is no match before 5, download the prev
# number. Save the *downloaded* numbers to a file. If the file contains 5, return.

# Separate the homework and programming assignments

# Save what has already been downloaded, download the rest

html = """<p>This notification is to let you know the AutoDownload program ran today.<br><br>
    The following is the result that was collected:<br>
    %s
"""

def download_csce_hw():
    assignment_url = "http://faculty.cs.tamu.edu/schaefer/teaching/221_Spring2017/"
    folder_url = 'C:\\Users\\Blake\\Google Drive\\Academics\\2017 Spring\\CSCE 221\\Assignments\\'
    filename = r'C:\Users\Blake\Dropbox\DevWork\TwitterBots\AutoDownload\last_downloaded.txt'

    response = urllib2.urlopen(assignment_url+"assignments.html")
    html = response.read() # HTML of the webpage, as a string

    last_dl_file = open(filename, 'r')
    x = int(last_dl_file.readline()) + 1
    pattern = "(PA|HW)(" + str(x) + ").doc"
    assignments = [m.start() for m in re.finditer(pattern, html)]
    if not assignments:
        return "No new assignments have been posted."
    names = []
    for a in assignments:   # Generalized, in case only HW/PA for that number has been posted.
        name = html[a:a+7]
        if "HW" in name:
            hw = (name, "Homework")
            names.append(hw)
        elif "PA" in name:
            pa = (name, "Programming Assignments")
            names.append(pa)

    result = ", ".join(names)
    for n in names:
        doc_name = n[0]
        doc_url = "Assignments/" + doc_name
        doc_type = n[1]
        doc_url = assignment_url + doc_url
        doc = urllib2.urlopen(doc_url)
        win_path = folder_url + doc_type + "\\" + doc_name
        with open(win_path, 'wb') as output:
            output.write(doc.read())

    with open(filename, 'w') as output: # Save the last assignment posted in the sequence to the text file
        output.truncate()
        output.write(str(x))

    return result + " has been posted and saved to your path."

def send_email(cs_result = ""):
    email = ""
    password = ""
    with open("email_creds.txt", 'r') as e:
        email = e.readline()
        password = e.readline()

    msg = MIMEMultipart('alternative')
    msg['Subject'] = "AutoDownload Notification"
    msg['From'] = email
    msg['To'] = "blake@blake-n-nelson.com"

    body = MIMEText(html % cs_result, 'html')
    msg.attach(body)

    mail = smtplib.SMTP('smtp.gmail.com', 587)
    mail.ehlo()
    mail.starttls()
    mail.login(email, password)
    mail.sendmail(email, "blake@blake-n-nelson.com", msg.as_string())
    mail.quit()


if __name__ == "__main__":
    r1 = download_csce_hw()
    send_email(r1)