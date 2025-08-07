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
    "Gets the user identity and group information for a given username"
    try:
        user_record = pwd.getpwnam(username) # use the 'pwd' module to get users account info. Uses /etc/passwd to retrieve information such as UID, GID, home directory, shell.
        primary_gid = user_record.pw_gid # takes the user's Primary Group ID(GID) from /etc/passwd/
        primary_group = grp.getgrgid(primary_gid).gr_name # Uses 'grp' module to get the name of the group based on GID. Will return the Primary group name.

        other_groups = [] # Builds a list of all secondary groups the user belongs to(excludes primary group)
        for group in grp.getgrall(): # returns all system groups, and filters through the ones the username is in the member list.
            if username in group.gr_mem:
                other_groups.append(group.gr_name) # Adds group to the list.

        sudo_user = 'sudo' in other_groups or primary_group == 'sudo' # Checks to see if user has "sudo" status in any group(primary or secondary).

        output = f"\n==== User Identity ====\n"
        output += f"UID: {user_record.pw_uid}\n" # Appends the user's UID to the result.
        output += f"Primary Group: {primary_group} (GID: {primary_gid})\n" # Primary group and GID
        
        if len(other_groups) > 0: # Checks if the list has at least one item in it.
            secondary_groups = ", ".join(other_groups) # combines the group names with commas.
        else:
            secondary_groups = "None" # No groups other than primary present.

        output += f"Secondary Groups: {secondary_groups}\n"

        if sudo_user: # returns if the user has sudo access
            output += "Sudo User: Yes\n" 
        else:
            output += "Sudo User: No\n"

        return output
    
    except Exception as error: # If any error occurs in the try block, this will catch it and return a user-friendly message.
        return f"\n==== User Identity ====\nError: {error}"
    

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
        output = subprocess.check_output(['chage', '-l', username], text=True) # Runs the 'chage -l username' command using python. 'chage' allows a user to view or modify password aging or account expiration settings. '-l' tells 'chage' to list all expiry info for that specific user.
        # 'subprocess.check_output' runs the command in the terminal and captures the output. 'text=True' ensures the output is returned as a string. 
        return "\n==== Account Expiry Details ====\n" + output # If the previous command runs successfully, this will return a formatted string. Output from the command is added to the section header.
    
    except subprocess.CalledProcessError: # If 'chage' command does not work, python raises the following error meaning the command failed.
        return "\n==== Account Expiry Details ====\nError: expiry info not available."
 


def generate_report(username, user_data):
    "returns all the infomation obtained as a text file"

def main():
    username = get_username()
    info = account_expiries(username)
    print(info)
    
if __name__ == "__main__":
    main()

