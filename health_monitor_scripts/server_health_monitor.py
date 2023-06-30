__author__ = 'Ajay Singh <ajaysingh002@gmail.com>'
__copyright__ = 'Copyright 2022, test Systems'
__maintainer__ = 'Ajay Singh'
__email__ = 'ajaysingh002@gmail.com'
__date__= 'Sep 02, 2022'
__version__ = 1.0

import re
import paramiko
import smtplib

global error_collector
error_collector = []
global logfile
logfile= 'server_health_monitor_log.txt'
global fo
fo = open(logfile, 'w+')

plan_to_verify = {
    "1" : {
        "hostname": "ajaynp-demo-lnx",
        "ip" : "172.24.77.213",
        "username" : "ajaynp-demo-lnx",
        "password" : "test123",
        "commands" : ["DISKSPACE_AVAILABLE::/dev/mapper/ubuntu--vg-ubuntu--lv", "FREE_MEMORY"],
    },
    "2" : {
        "hostname": "ajaynp-stg-lnx",
        "ip" : "11.105.39.54",
        "username" : "ajaynp",
        "password" : "test@123",
        "commands" : ["DISKSPACE_AVAILABLE::/dev/sda1", "FREE_MEMORY"],
    },
    "3" : {
        "hostname": "ajaynp-test2-lnx",
        "ip" : "11.106.209.107",
        "username" : "test",
        "password" : "test123",
        "commands" : ["DIR_EXISTS::/opt/testsim"],
    },
    "4" : {
        "hostname": "11.64.104.35",
        "ip" : "ajaynptest10-ucs",
        "username" : "test",
        "password" : "test123",
        "commands" : ["DIR_EXISTS::/opt/testsim"],
    },
    "5" : {
        "hostname": "ajaynptest4-lnx",
        "ip" : "-",
        "username" : "ajaynptest",
        "password" : "ajaynptest&11",
        "commands" : ["CHECK_PING::11.11.1.21", "CHECK_PING::11.11.1.27", 
            "CHECK_PING::11.64.104.43", 
             "CHECK_PING::11.64.104.184", "CHECK_PING::11.64.108.11",
            "CHECK_PING::11.64.104.122", "CHECK_PING::11.64.104.128", "CHECK_PING::11.64.104.121"],
    },
    "6" : {
        "hostname": "11.64.104.191",
        "ip" : "ajaynptest11-ucs",
        "username" : "root",
        "password" : "Ci$c0@321",
        "commands" : ["DIR_EXISTS::/auto/vxr/pyvxr/latest/vxr.py", "CHECK_PING::11.64.104.182", "CHECK_PING::11.64.104.74"],
    },
}


def ajprint(msg):
    print(msg)
    fo.write("%s \n" %msg)


def connect_ssh(hostname, username, password):
    global client
    client = paramiko.client.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname, username=username, password=password)
        ajprint('Connected: %s' % hostname)
        return (1)
    except Exception as ex:
        ajprint("*** ERROR:: Failed to connect the node: %s : %s ***" % (hostname, str(ex)))
        error_collector.append("*** ERROR:: Failed to connect the node: %s : %s ***" % (hostname, str(ex)))
        return (0)


def disconnect_ssh(hostname, ip):
    client.close()
    ajprint("Connection Closed: %s [%s]" % (hostname, ip))


def check_disk_space(grepOption):
    command = "df -h"
    if grepOption:
        command = command + " | grep " + grepOption
    _stdin, _stdout,_stderr = execute_command(command)
    #ajprint(_stdin.read().decode())
    stdout = _stdout.read().decode()
    stderr = _stderr.read().decode()
    if stderr:
        ajprint("*** ERROR:: Error received from the command: %s on executing on client: %s" % (command, clientHostname))
        error_collector.append("*** ERROR:: Error received from the command: %s on executing on client: %s" % (command, clientHostname))
        ajprint("stderr = %s" % stderr)
    else:
        ajprint("stdout = \'%s\'" % stdout.strip())
        m = re.search("\d+%", stdout.strip())
        usedSpacePercentage = m.group(0)
        ajprint("usedSpacePercentage = %s" % usedSpacePercentage)
        return(usedSpacePercentage)


def check_free_memory():
    command = "free -m | grep Mem:"
    _stdin, _stdout,_stderr = execute_command(command)
    #ajprint(_stdin.read().decode())
    stdout = _stdout.read().decode()
    stderr = _stderr.read().decode()
    availableMemory = 0
    ajprint("stdout = \'%s\'" % stdout.strip())
    if not stdout:
        ajprint("*** ERROR:: No output received from the command: %s on executing on client: %s" % (command, clientHostname))
        error_collector.append("*** ERROR:: No output received from the command: %s on executing on client: %s" % (command, clientHostname))
    else:
        m = re.search("\s+(\d+)$", stdout.strip())
        availableMemory = int(m.group(0).strip())
    if stderr:
        ajprint("*** ERROR:: Error received from the command: %s on executing on client: %s" % (command, clientHostname))
        error_collector.append("*** ERROR:: Error received from the command: %s on executing on client: %s" % (command, clientHostname))
        ajprint("stderr = %s" % stderr)
    ajprint("availableMemory = %s" % availableMemory)
    return(availableMemory)


def check_dir_exists(dirToCheck):
    command = "ls " + dirToCheck
    _stdin, _stdout,_stderr = execute_command(command)
    #ajprint(_stdin.read().decode())
    stdout = _stdout.read().decode()
    stderr = _stderr.read().decode()
    if stderr:
        ajprint("*** ERROR:: Error received from the command: %s on executing on client: %s" % (command, clientHostname))
        error_collector.append("*** ERROR:: Error received from the command: %s on executing on client: %s" % (command, clientHostname))
        ajprint("stderr = %s" % stderr)
        return(0)
    else:
        ajprint("stdout = \'%s\'" % stdout.strip())
        return(1)


def check_ip_pings(ipToPing):
    command = "ping -c 2 " + ipToPing
    _stdin, _stdout,_stderr = execute_command(command)
    #ajprint(_stdin.read().decode())
    stdout = _stdout.read().decode()
    stderr = _stderr.read().decode()
    if stderr:
        ajprint("*** ERROR:: Error received from the command: %s on executing on client: %s" % (command, clientHostname))
        error_collector.append("*** ERROR:: Error received from the command: %s on executing on client: %s" % (command, clientHostname))
        ajprint("stderr = %s" % stderr)
        return(0)
    else:
        ajprint("stdout = \'%s\'" % stdout.strip())
        m = re.search("(\d+)% packet loss", stdout.strip())
        pktLossPercentage = m.group(0)
        packetLossPercentage = pktLossPercentage.split("%")[0]
        ajprint("packetLossPercentage = %s" % packetLossPercentage)
        if int(packetLossPercentage) == 0:
            return(1)
        else:
            return(0)


def execute_command(command):
    ajprint("Executing command: %s" % command)
    return(client.exec_command(command))


def send_email():
    email_from = 'ajaysingh002@gmail.com'
    email_to = 'ajaynp-india-test@test.com'
    #email_to = 'ajaysingh002@gmail.com, shrcs@test.com'
    email_subject = "Server Health Monitor Agent Email"

    fo.flush()
    fread = open(logfile, 'r')
    cons_data = fread.readlines()

    cons_email_text = "\n"
    cons_email_text += "<b>ERRORS RECEIVED::</b>" + "<br>"
    if len(error_collector) == 0:
        cons_email_text += "None" + "<br>"
    for error in error_collector:
        cons_email_text += error + "<br>"
    cons_email_text += "<hr>"
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
        smtpObj = smtplib.SMTP("email.test.com")
        ajprint("Sending final email")
        smtpObj.sendmail(email_from, email_to, email_body)
        ajprint("Successfully sent final email")
    except smtplib.SMTPException:
        ajprint("*** ERROR: unable to send final email")
        error_collector.append("*** ERROR: unable to send final email")


def main_method():
    #for node in plan_to_verify.values():
    for key, values in plan_to_verify.items():
        # global plan_item_number
        # plan_item_number = key
        ajprint("*" * 80)
        global clientHostname
        clientHostname = plan_to_verify[key]["hostname"]
        clientIp = plan_to_verify[key]["ip"]
        clientUsername = plan_to_verify[key]["username"]
        clientPassword = plan_to_verify[key]["password"]
        commands = plan_to_verify[key]["commands"]
        #commands = node["commands"]
        ajprint("Connecting: %s" % clientHostname)
        if not connect_ssh(clientHostname, clientUsername, clientPassword):
            ajprint("*** ERROR: Node down or incorrect credentials provided. Failed to connect: %s : %s : %s" % (clientHostname, clientUsername, clientPassword))
            error_collector.append("*** ERROR: Node down or incorrect credentials provided. Failed to connect: %s : %s : %s" % (clientHostname, clientUsername, clientPassword))
        else:
            for cmd in commands:
                ajprint("=-" * 30)
                ajprint("Executing: %s" % cmd)
                if "DISKSPACE_AVAILABLE" in cmd:
                    grepOption = cmd.split("::")[1] if len(cmd.split("::")) > 1 else ""
                    spaceUsed = check_disk_space(grepOption)
                    #ajprint(type(spaceUsed))
                    space_used = spaceUsed.replace("%", "")
                    if int(space_used) == 0:
                        ajprint("*** ERROR:: Incorrect command. Please check the grepOption \'%s\'. Used space = \'%s\' on host \'%s\'" % (grepOption, space_used, clientHostname))
                        error_collector.append("*** ERROR:: Incorrect command. Please check the grepOption \'%s\'. Used space = \'%s\' on host \'%s\'" % (grepOption, space_used, clientHostname))
                    elif int(space_used) > 90:
                        ajprint("*** ERROR:: System low on space. Used space = \'%s\' on host \'%s\'" % (space_used, clientHostname))
                        error_collector.append("*** ERROR:: System low on space. Used space = \'%s\' on host \'%s\'" % (space_used, clientHostname))
                    else:
                        ajprint("Current used space = \'%s\' on host \'%s\'" % (space_used, clientHostname))
                if "FREE_MEMORY" in cmd:
                    memory_available = check_free_memory()
                    if int(memory_available) == 0:
                        ajprint("*** ERROR:: No Available Memory. Memory Available = \'%s\' on host \'%s\'" % (memory_available, clientHostname))
                        error_collector.append("*** ERROR:: System low on space. Used space = \'%s\' on host \'%s\'" % (space_used, clientHostname))
                    elif int(memory_available) < 10000:
                        ajprint("*** ERROR:: System low on memory. Memory Available = \'%s\' on host \'%s\'" % (memory_available, clientHostname))
                        error_collector.append("*** ERROR:: System low on memory. Memory Available = \'%s\' on host \'%s\'" % (memory_available, clientHostname))
                    else:
                        ajprint("Current available Memory = \'%s\' on host \'%s\'" % (memory_available, clientHostname))
                if "DIR_EXISTS" in cmd:
                    dirToCheck = cmd.split("::")[1] if len(cmd.split("::")) > 1 else "IN COMPLETE COMMAND. PROVIDE DIR TO CHECK"
                    if not check_dir_exists(dirToCheck):
                        ajprint("*** ERROR:: Directory \'%s\' doesnot exist on host \'%s\'" % (dirToCheck, clientHostname))
                        error_collector.append("*** ERROR:: Directory \'%s\' doesnot exist on host \'%s\'" % (dirToCheck, clientHostname))
                    else:
                        ajprint("As expected, found directory \'%s\' on host \'%s\'" % (dirToCheck, clientHostname))
                if "CHECK_PING" in cmd:
                    if len(cmd.split("::")) > 1:
                        ipToPing = cmd.split("::")[1]
                        if not check_ip_pings(ipToPing):
                            ajprint("*** ERROR:: IP \'%s\' is not pinging." % (ipToPing))
                            error_collector.append("*** ERROR:: IP \'%s\' is not pinging." % (ipToPing))
                        else:
                            ajprint("As expected, IP \'%s\' is pingable." % (ipToPing))
                    else:
                        ajprint("*** ERROR:: INCOMPLETE COMMAND. PROVIDE IP TO PING")
                        error_collector.append("*** ERROR:: INCOMPLETE COMMAND. PROVIDE IP TO PING")
            ajprint("=-" * 30)
            disconnect_ssh(clientHostname, clientIp)
    # Send email
    send_email()
    # Print error_collector
    ajprint("*" * 90)
    ajprint("ERRORS RECEIVED::")
    if len(error_collector) == 0:
        ajprint("None")
    for error in error_collector:
        ajprint(error)
    ajprint("*" * 90)


main_method()

fo.close()
print("Closed Output File")


