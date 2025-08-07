#!/usr/bin/env python3
#Description: Assignment2 script - System monitoring Project. User will enter valid account name and will return computer log time, user account type, and sudo status

import subprocess # Can run external programs or system commands from within the python script.
import pwd # Access the 'pwd' module. Retrieve information about user accounts on a Unix/Linux system.
import grp 
import datetime
import os

def get_username():
    "User enters a valid username on the system"
    username = input("Enter a Username: ").strip() # Asks user for username. Removes and leading or trailing spaces from the input.
    return username

def is_user_valid(username):
    "Checks to see if entered user account exists"
    try:
        pwd.getpwnam(username) # Looks up information for the username by searching the systems user database(accessed through the 'pwd' module).
        return True # If user exists, return true(this is a valid system user)

    except KeyError: # If the previous check fails, its because the user does not exist, so python raises a KeyError.
        return False # Returns False, therefore user does not exist.

def user_login_activity(username):
    "returns login history for given username"

    output = "\n==== Login Activity ====\n" # Section title

    # Current login session & idle status
    try: # Executes the following code and will raise errors such as the user not currently logged in.
        current_session = subprocess.check_output(['w', username], text=True) # Runs the shell command 'w'(Who is logged in and idle time) for a specific username. 'subprocess.check_output' captures the command's output, and 'text=True' ensures its returned as a string.
        output += "[Current Session & Idle Status]\n" + current_session # Appends a section title, and the user's session info to the output string.

    except subprocess.CalledProcessError: # If the 'w' command does not work(user is not logged in), python raises this error meaning the command failed.
        output += "[Current Session & Idle Status]\nUser account is currently inactive.\n" # User-friendly message is printed.

    # Past login session history
    try:
        past_session = subprocess.check_output(['last', username], text=True) # Runs the shell command 'last'(history of past logins) for a specific username.
        output += "\n[Past Session History]\n" + past_session # Appends title and session info to output.

    except subprocess.CalledProcessError: # If the 'last' command does not work(no records, new user), python raises this error meaning the command failed.
        output += "\n[Past Session History]\nError: Previous history not available.\n"

    return output

def user_identity(username):
    '''Gets the UID, GID, group memberships, and privilege warnings for a given user.
    Returns a dictionary of results, or an error message if the user doesn't exist.'''
    try:
        user_info = pwd.getpwnam(username) #this will throw  a keyerror if the useer does not exist
        uid = user_info.pw_uid  # gets us the user ID 
        gid = user_info.pw_gid  # same thing but gets us the Group ID 

        group_list = []  # so here is a lists of all the groups the user is a member of
        for group in grp.getgrall(): # this loops through all the groups present in the system
            if username in group.gr_mem or group.gr_gid == gid: #If this user is listed in the group OR if the group ID matches their main group
                group_list.append(group.gr_name) #then this adds that groups name to the list

        # Checking for sudo and adm groups
        privilege_warnings = []
        if 'sudo' in group_list: #if the useer is in the sudo group, they can run the admin commads
            privilege_warnings.append('User has sudo privileges.')
        if 'adm' in group_list:  # If the user is in the adm group, they can read system logs
            privilege_warnings.append('User has adm (log access) privileges.')

        return {
            'uid': uid,
            'gid': gid,
            'groups': group_list,
            'warnings': privilege_warnings
        }

    except KeyError:  # catches an error that would happen if the username doesn’t exist like a typo Instead of crashing the program
        return {
            'error': 'User not found'
        }

def check_sudo_attempts(username):
    "obtains the number of times the 'sudo' command was passed or failed"
    try:
        with open('/var/log/auth.log', 'r') as auth_file: # Opens the file in read-only mode. The '/var/log/auth.log' file stores system authentication messages(like 'sudo' usage and authentication failures). 'with' is a safe way to open the file, since it closes automatically when finished.
            sudo_success = 0 # Counts # of successful 'sudo' commands the user ran.
            sudo_failure = 0 # Counts # of failed 'sudo' password attempts they made.

            for line in auth_file: # Loop through each line of the file(each line in file is an event)
                if "sudo" in line and username in line: # Filters through the lines that mention "sudo"('sudo'-related action), and include the given username(specific user).
                    if "COMMAND=" in line: # If the user successfully ran a 'sudo' command
                        sudo_success += 1 # Success counter increases by 1

                    elif "authentication failure" in line: # If the user's 'sudo' password attempt failed
                        sudo_failure += 1 # Failure counter increases by 1

        return (f"\n==== Sudo Attempts ====\n" # returns string in following format
                f"Successful attempts: {sudo_success}\n"
                f"Failed attempts: {sudo_failure}")

    except FileNotFoundError: # If '/var/log/auth.log' does not exist or can't be opened(not present in system).
        return "\n==== Sudo Attempts ====\nError: Could not access '/var/log/auth.log'. This system may use journalctl instead." # Returns user-friendly error message.

    except PermissionError: # The file '/var/log/auth.log' is present, but the user needs permission to read it.
        return "\n==== Sudo Attempts ====\nError: Access denied. Try to run the script using 'sudo'."

def account_expiries(username):
    "check the given username password expiration settings"
    try:
        shadow_output = subprocess.check_output(['chage', '-l', username], text=True) # Run chage -l to get expiry settings
        return "\n==== Account Expiry Info ====\n" + shadow_output
    except subprocess.CalledProcessError:
        return "\n==== Account Expiry Info ====\nError: Unable to fetch expiry information."

def generate_report(username, user_data):
    "returns all the infomation obtained as a text file"

    filename = "report_" + username + ".txt"  # iam naming the report file by using the username so it is easy to know who it belongs to
    with open(filename, "w") as report: # opening the file in write mode, which will create the file or overwrite it if it already exists

        # Get the current date and time so we can include it in the report
        now = datetime.datetime.now()
        date_str = now.strftime("%Y-%m-%d")  # Example: 2025-08-07
        time_str = now.strftime("%H:%M:%S")  # Example: 14:30:55

        # First, it writes the basic info about the user and a title
        report.write("==== System Report ====\n")
        report.write("Date: " + date_str + "    Time: " + time_str + "\n\n")
        report.write("==== User Information ====\n")
        report.write("Username: " + username + "\n")
        report.write("UID: " + str(user_data['uid']) + "\n")  # then their UID
        report.write("GID: " + str(user_data['gid']) + "\n")  # and their GID

        # Now writes the list of groups this user is in, separated by commas(eg:sudo,admin...)
        report.write("Groups: " + ", ".join(user_data['groups']) + "\n\n")

        # If there are any warnings (like sudo or adm access), it writes them too
        if user_data['warnings']:
            report.write("==== Privilege Warnings ====\n")
            for warning in user_data['warnings']:
                report.write("- " + warning + "\n")

        report.write("\n=== End of Report ===\n")

    # shows a message in to know that it worked out 
    print("Report saved as", filename)

def main():

    username = get_username() # asks the user to enetr  their username
    if not is_user_valid(username): # this checks if th euser really exists in the system
        print("Error: That user does not exist on this system.")
        return  # Stop the program here if the username is invalid

    user_data = user_identity(username) # so if the user is valid we should get their id information 
    if 'error' in user_data: # if theres a error while trying to fetch the id (eg: 'User not found') it will stop th>
        print("Error:", user_data['error'])
        return

    # Generates a report and saves it to a text file
    generate_report(username, user_data)

    # Call the extra functions that return formatted text and display them
    print(user_login_activity(username))
    print(check_sudo_attempts(username))
    print(account_expiries(username))

if __name__ == "__main__":
    main()
