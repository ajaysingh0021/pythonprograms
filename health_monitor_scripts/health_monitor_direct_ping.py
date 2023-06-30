# Made to run from Windows OS

__author__ = 'Ajay Singh'
__copyright__ = 'none'
__maintainer__ = 'Ajay Singh'
__email__ = 'ajaysingh002@gmail.com'
__date__= 'Jun 30, 2023'
__version__ = 1.0

import smtplib
import subprocess
import platform


# Check OS type
os_type = platform.system()
# Add the commands to run
if os_type == 'Windows':
    commands_to_verify = [
        ['ping', '-n', '4', 'www.google.com'],
    ]
else:
    commands_to_verify = [
        ['ping', '-c', '4', 'www.google.com'],
    ]

def ajprint(msg):
    print(msg)
    fo.write("%s \n" %msg)

def execute_command(command):
    ajprint("Executing command: %s" % command)
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    ajprint("output=%s error=%s" %(output, error))
    if("0% loss" in output.decode('utf-8') or "0% packet loss" in output.decode('utf-8')):
        return(0)
    else:
        return(99)
    
def send_email(logfile):
    email_from = 'ajaysingh002@gmail.com'
    email_to = 'ajaysingh002@gmail.com'
    email_subject = "*** WEBSITE DOWN ***"

    fo.flush()
    fread = open(logfile, 'r')
    cons_data = fread.readlines()

    cons_email_text = "\n"
    # cons_email_text += "<b>ERRORS RECEIVED::</b>" + "<br>"
    cons_email_text += "<b>LOG FILE CONTENTS::</b>"
    cons_email_text += "<hr>"
    for line in cons_data:
        cons_email_text += str(line) + "<br>"
    cons_email_text += "<hr>"
    fread.close()
    
    email_body  = "From: " + email_from + "\n"
    email_body += "To: " + email_to + "\n"
    email_body += "Subject: " + email_subject + "\n"
    email_body += "Content-type: text/html\n"
    email_body += cons_email_text

    try:
        smtpObj = smtplib.SMTP("email.ajay.com")
        ajprint("Sending final email")
        smtpObj.sendmail(email_from, email_to, email_body)
        ajprint("Successfully sent final email")
    except smtplib.SMTPException:
        ajprint("*** ERROR: unable to send final email")
    

if __name__ == "__main__":
    b_send_email = False
    # Open the log file to write
    logfile= 'health_monitor_direct_ping_log.txt'
    print(f'Opening log file {logfile}')
    fo = open(logfile, 'w+')

    for cmd in commands_to_verify:
        ajprint("=-" * 30)
        if int(execute_command(cmd)) == 0:
            ajprint("Command Successful")
        else:
            ajprint("Command Failed")
            b_send_email = True
        ajprint("=-" * 30)
    
    # Send email email failure occurs
    if b_send_email:
        send_email(logfile)
    #send_email(logfile)
    # Close the log file
    fo.close()
    print("Closed Output File")

    print("Program complete!")