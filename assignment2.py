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
    "Gets the user identity and group information for a given username"
    

def check_sudo_attempts(username):
    "obtains the number of times the 'sudo' command was passed or failed"

def account_expiries(username):
    "check the given username password expiration settings"

def generate_report(username, user_data):
    "returns all the infomation obtained as a text file"

def main():

if __name__ == "__main__":
    main()

