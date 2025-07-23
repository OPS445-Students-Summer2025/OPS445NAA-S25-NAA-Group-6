#!/usr/bin/env python3
#Description: Assignment2 script - System monitoring Project. User will enter valid account name and will return computer log time, user account type, and sudo status

import subprocess # Can run external programs or system commands from within the python script.


def get_username():
    "User enters a valid username on the system"

def is_user_valid(username):
    "Checks to see if entered user account exists"

def user_login_sessions(username):
    "returns login history for given username"

def user_groups(username):
    "Gets the user identity and group information for a given username"

def check_sudo_attempts(username):
    "obtains the number of times the 'sudo' command was passed or failed"

def account_expiries(username):
    "check the given username password expiration settings"

def generate_report(username, user_data):
    "returns all the infomation obtained as a text file"

if __name__ == "__main__":

