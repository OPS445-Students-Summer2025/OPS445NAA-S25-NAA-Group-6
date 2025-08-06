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

def account_expiries(username):
    "check the given username password expiration settings"

def generate_report(username, user_data):
    "returns all the infomation obtained as a text file"

def main():
    pass

if __name__ == "__main__":
    main()
