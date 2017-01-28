import urllib2
import re

assignment_url = "http://faculty.cs.tamu.edu/schaefer/teaching/221_Spring2017/"
folder_url = 'C:\\Users\\Blake\\Google Drive\\Academics\\2017 Spring\\CSCE 221\\Assignments\\'

response = urllib2.urlopen(assignment_url+"assignments.html")
html = response.read() # HTML of the webpage, as a string
# print "HTML:", html

x = 1
pattern = "(PA|HW)(" + str(x) + ").doc"
assignments = [m.start() for m in re.finditer(pattern, html)]
hw = assignments[0]
pa = assignments[1]

hw = (html[hw:hw+7], "Homework")                 # Name of Homework file
pa = (html[pa:pa+7], "Programming Assignments")  # Name of Programming Assignment file
names = [hw, pa]

for n in names:
    doc_name = n[0]
    doc_url = "Assignments/" + doc_name
    doc_type = n[1]
    # print assignment_url+doc_name
    doc_url = assignment_url + doc_url
    print "Doc URL:", doc_url
    doc = urllib2.urlopen(doc_url)
    win_path = folder_url + doc_type + "\\" + doc_name
    print "WinPath:", win_path
    with open(win_path, 'wb') as output:
        output.write(doc.read())

# Use regex to find all links. Keep increading number in pattern (HW1, 2, etc)
# up to 5 until there is no match. If there is no match before 5, download the prev
# number. Save the *downloaded* numbers to a file. If the file contains 5, return.

# Separate the homework and programming assignments

# Save what has already been downloaded (?), download the rest