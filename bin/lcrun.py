#!/usr/bin/python
"""
Purpose:    Run linux command on multiple hosts list
Date:       2017-Nov-11
Author:     ibrahim.k@sap.com
Version:    0.1

  Description:
    This python script is designed to run linux ssh commands on a list of
    hosts and display outputs from all the hosts in the display. You can
    provide the list of host names to be        checked in a plain csv file with
    username and password. In case you need     use keybased authentication,
    you need to install a key agent and import the requied keys in it before
    running this script. For keybased authentication, you need to only give
    the hostname and the username in the input file.

    This script extensively uses the "pxssh" program from the "pexpect" library
    So this library need to be imported to work with this script.

    Connecting to only one system: In this case, you do not want to create the
    input file, but just use the -l option with the script to mention the host,
    username and password.

    Input file: The input file should be kept under the 'input' directory with
    the below format:
    hostname,username,password          -> In case of password authentication
    hostname,username                           -> In case of key based authentication

    Each host details(username and password) must be in a new line.
    Blank lines in between these host details will not make any problem, since
    the script will ignore any new line entries.

    In the key based authentication, if the key is not in the connecting hosts
    known_hosts file, it adds automatically, If this does not work, try to
    connect manually once and add the keys to known_hosts file.
	
	Output of the script will be printed on the console as well as redirected to a 
	file in the output directory. The filename of the output file will be the current
	date and time stamp. Example: 20171101-152053 (in the format: %Y%m%d-%H%M%S)


  Examples:

    lcrun -i <input_file> 'command'

    The above example will run the 'command' on all the hosts mentioned under the file
    input_file and display the output on to the screen.

    lcrun -i hosts.csv 'uname -a'

    Connects to all the hosts mentioned in the hosts.csv file and runs the command 'uname -a'
    and provide all the os details on the screen for each hosts.

    lcrun -i hosts.csv 'uptime'

    Connects to the hosts mentioned in the hosts.csv file and outputs the uptime for all those
    hosts on the screen

    lcrun -i hosts.csv -l localhost -u username -p password 'who'

    Connects to all the hosts in the hosts.csv and also to an extra host localhost with username
    and password and display the users logged in currently to those machines.



  Usage: lcrun -i <input_file> 'command'

    Options:
        -h, --help            show this help message and exit
        -i <input_file>, --inputs=INPUT_FILE
                        hosts file (each line "servername,username,password")
        -l <hostname>, --hostname=HOSTNAME
                        Additional hostname [optional]
        -p <password>, --password=PASSWORD
                        Password for the additional host, with -l [optional]
        -u <username>, --username=USERNAME
                        Username for the additional host used with -l
                        [optional]
"""
import os
import sys
import csv
import re
sys.path.append('../')
import lib.pexpect
from optparse import OptionParser
from lib.pexpect import pxssh
from lib.pexpect import ExceptionPexpect


"""
Relative path for the input file, always the input file should be under the input directory.
"""

INPUT_DIR = "../input"


def option_parser():
    """
        Parser for command line options, the input file,
        [username and password, if not provided in the input file with -l option]
    """

    parser = OptionParser(conflict_handler="resolve")

    parser.usage = "%prog [OPTIONS] command [...]"
    parser.epilog = "This script runs the provided command in all the hosts mentioned in the input file and " \
                    "displays the output on the screen\n Example: lcrun.py -i hosts.csv 'ls -l' "
    parser.add_option('-i', '--inputs', dest="input_file", action='append',
                      help='hosts file (each line "servername,username,password")')
    parser.add_option('-l', '--hostname', dest='hostname', action='append', help='Additional hostname [optional]')
    parser.add_option('-p', '--password', dest='password', action='append',
                      help='Password for the additional host, with -l [optional]')
    parser.add_option('-u', '--username', dest='username',
                      help='Username for the additional host used with -l [optional]', action='append')

    return parser


def parse_args():
    """
    Method for checking the arguments and values on the command line. if no input file is given
    and no extra host added with -l option, parser error is raised and exit from program

    Also if there is no command is entered as the last argument, parser error will be raised and
    program will exit.
    """
    parser = option_parser()
    (opts, arguments) = parser.parse_args()

    if opts.input_file is None and opts.hostname is None:
        parser.error("Not entered the input file. Example: lcrun.py -i hosts.csv \"ls -l\"")
        exit(0)
    if len(arguments) == 0:
        parser.error('Command not specified.')
        exit(0)
    return opts, arguments


def connect_host(hostname, username, password, commandline):
    """
        Method for connecting to the host and executing the given comment with password authentication, the input file
        contains three columns with hostname/server name, username and password
    """
    try:
        print 'Using password authentication'
        s = pxssh.pxssh()
        s.login(hostname, username, password, login_timeout=20)
        if commandline.startswith('sudo '):
            commandline = commandline[5:]
            rootprompt = re.compile('.*[$#]')
            s.sendline('sudo -s')
            i = s.expect([rootprompt, 'assword.*: '])
            if i == 0:
                print "did not need password!"
                pass
            elif i == 1:
                print "sending password"
                s.sendline('rSL9mMdB')
                j = s.expect([rootprompt, 'Sorry, try again'])
                if j == 0:
                    pass
                elif j == 1:
                    raise Exception("bad password")
            else:
                raise Exception("unexpected output")
            s.set_unique_prompt()
        s.sendline(commandline)
        s.prompt(timeout=10)
        print 'OUTPUT: '
        print '\t', s.before
        if commandline.startswith('sudo '):
            s.sendline('exit')
        s.logout()
        print '=============================='
		return 0
    except ExceptionPexpect as ep:
        print 'Could not connect to the host ->', hostname, "\nError: ", ep
		return 1
    except e:
        print "Could not connect to the host"
		return 2


def connect_host_key(hostname, username, commandline):
    """
        Method to connect to the given host using key based authentication. the input file should have two columns with
        hostname/server name and username
        Most importantly the ssh agent should be running with the added private keys
    """
    try:
        print 'using Key based Authentication'
        s = pxssh.pxssh()
        s.SSH_OPTS += " -o StrictHostKeyChecking=no"
        s.force_password = False
        s.login(hostname, username, login_timeout=20)
        if commandline.startswith('sudo '):
            commandline = commandline[5:]
            rootprompt = re.compile('.*[$#]')
            s.sendline('sudo -s')
            i = s.expect([rootprompt, 'assword.*: '])
            if i == 0:
                print "did not need password!"
                pass
            elif i == 1:
                print "sending password"
                s.sendline('rSL9mMdB')
                j = s.expect([rootprompt, 'Sorry, try again'])
                if j == 0:
                    pass
                elif j == 1:
                    raise Exception("bad password")
            else:
                raise Exception("unexpected output")
            s.set_unique_prompt()
        s.sendline(commandline)
        s.prompt(timeout=10)
        print 'OUTPUT: '
        print '\t', s.before
        #if commandline.startswith('sudo '):
        s.sendline('exit')
        s.logout()
        print '=============================='
		return 0
    except ExceptionPexpect as ep:
        print 'Could not connect to the host ->', hostname, "\nError: ", ep
		return 1

def connect_using_file():
    """
    This method uses the input file mentioned on the command line as
    input and connects to all the hosts in the list and executes the
    command. Finally displays the output on the screen and exits the program
    Exception will be thrown in case of any error in the file(format error or
    reading error)

    Also this method identifies, whether it is a key based authentication or password
    authentication and call the appropriate methods based on the host details
    mentioned on the input_file
    """
    input_file = os.path.join(INPUT_DIR, ''.join(options.input_file))

    try:
        with open(input_file, 'rb') as f:
            reader = csv.reader(f)

            for i, line in enumerate(reader):
                if len(line) == 0 or ''.join(line).startswith('#'):  # If there is any blank lines or lines with an # in the file, ignore it
                    continue
                print "\n\n\nConnecting to host", line[0]
                print '##############################'
                print '\t', line[0]
                print '##############################'
                if len(line) == 3:
                    connect_host(line[0], line[1], line[2], cmdline)
                elif len(line) == 2:
                    connect_host_key(line[0], line[1], cmdline)

                else:
                    print 'ERROR ::: Missing entries in the input file'
    except IOError as input_error:
        print "Cannot open the input file :", input_error


def check_sudo_cmd(commandline):
    """
    Function to check whether the command entered is a sudo command. In this case
    Confirm to run the sudo command on the host. If the user inputs Y/y the program
    will continue, else with any other input the program will exit.
    """
    if commandline.startswith('sudo '):
        confirm = raw_input('\nCommand requires sudo access,do you want to continue(y/n)?')
        if confirm == 'y' or 'Y':
            return 1
        else:
            print '\nExiting the program, since it is a sudo command'
            exit(0)
    """
    This Logger class is to log all the stdout to a file as well as on the console
    The output files will be stored in the "outputs" directory with the date and time
    stamp as the file name
    """
class Logger(object):
    def __init__(self):
        self.terminal = sys.stdout
		outfile = os.path.join("../output", datetime.now().strftime("%Y%m%d-%H%M%S"))
        self.log = open(outfile, "w")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        # this flush method is needed for python 3 compatibility.
        # this handles the flush command by doing nothing.
        # you might want to specify some extra behavior here.
        pass
		

# Main function

if __name__ == "__main__":

    options, args = parse_args()
    cmdline = ''.join(args)
    IsSudo = check_sudo_cmd(cmdline)
    sys.stdout = Logger()
	try:
        if options.input_file is not None:
            connect_using_file()

        if options.hostname is not None:
            connect_host(''.join(options.hostname), ''.join(options.username), ''.join(options.password), cmdline)

    except IOError:
        """
        Throw the below error in case an error occurs during the reading of input file
        In case the file is write protected or damaged, the program will be exited with
        exit code 1 and display the error message.
        """
        _, e, _ = sys.exc_info()
        sys.stderr.write('Could not open hosts file: %s\n' % e.strerror)
        sys.exit(1)
