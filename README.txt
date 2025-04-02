Inputnput file should be kept under the 'input directory'
Run the lcrun script with an input file : Example:-> lcrun -i hosts.csv ls

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
