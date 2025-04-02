# lcrun

## Purpose
Run Linux commands on multiple hosts from a list.

**Date:** 2017-Nov-11  
**Author:** [ibrahim.k@sap.com](mailto:ibrahim.k@sap.com)  
**Version:** 0.1  

---

## Description
This Python script is designed to run Linux SSH commands on a list of hosts and display outputs from all the hosts in the terminal. You can provide the list of host names to be checked in a plain CSV file with username and password.

For key-based authentication, install a key agent and import the required keys before running this script. In this case, you only need to provide the hostname and username in the input file.

This script extensively uses the **pxssh** module from the **pexpect** library. Ensure that this library is installed before using the script.

### **Connecting to a Single System**
If you need to connect to only one system, you can use the `-l` option instead of creating an input file to specify the host, username, and password directly.

---

## **Input File**
The input file should be kept under the `input` directory with the following format:

- **Password Authentication:**
  ```csv
  hostname,username,password
  ```

- **Key-Based Authentication:**
  ```csv
  hostname,username
  ```

Each host's details (username and password) must be on a new line. Blank lines in the file are ignored.

For key-based authentication, if the key is not in the connecting host’s `known_hosts` file, it is added automatically. If this does not work, try connecting manually once and add the keys to `known_hosts`.

---

## **Output**
The script prints the output on the console and also saves it in the `output` directory. The filename of the output file follows the format:

```
YYYYMMDD-HHMMSS (Example: 20171101-152053)
```

---

## **Examples**

Run a command on all hosts specified in an input file:
```bash
lcrun -i <input_file> 'command'
```

Example usage:
```bash
lcrun -i hosts.csv 'uname -a'
```
This connects to all hosts listed in `hosts.csv`, runs `uname -a`, and displays OS details.

```bash
lcrun -i hosts.csv 'uptime'
```
Displays the uptime of all hosts in `hosts.csv`.

Connect to additional hosts:
```bash
lcrun -i hosts.csv -l localhost -u username -p password 'who'
```
This connects to all hosts in `hosts.csv`, plus an additional host `localhost`, and displays the logged-in users.

---

## **Usage**
```bash
lcrun -i <input_file> 'command'
```

### **Options:**
| Option | Description |
|--------|-------------|
| `-h, --help` | Show help message and exit |
| `-i <input_file>, --inputs=INPUT_FILE` | Hosts file (each line: `servername,username,password`) |
| `-l <hostname>, --hostname=HOSTNAME` | Additional hostname (optional) |
| `-p <password>, --password=PASSWORD` | Password for additional host (used with `-l`, optional) |
| `-u <username>, --username=USERNAME` | Username for additional host (used with `-l`, optional) |

---

## **Prerequisites**
Ensure the following dependencies are installed before running the script:
```bash
pip install pexpect
```

---

## **License**
This project is licensed under the MIT License.

---

### **Contributions & Issues**
Feel free to submit issues or contribute improvements via GitHub pull requests.

