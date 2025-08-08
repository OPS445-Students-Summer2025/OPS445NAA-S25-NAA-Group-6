# Summer 2025 Assignment 2

System_user_monitor.py script creates a detailed report for a specific linux user. In the system user monitoring script, the user will enter a valid account(username) name and script will return user identity, computer log time, account expiries, and sudo status.

Reports are then saved to the script runner's home directory: ~/user_reports/.



How requirements are accomplished:

Identity & groups: pwd, grp modules (primary group + all secondary groups).

Sudo membership: checks whether user is in group sudo (primary or secondary).

Current login session & idle: w <username>.

Previous login history: last <username>.

Sudo attempts: parses /var/log/auth.log for lines mentioning the user; counts “COMMAND=” (success) vs “authentication failure” (failure).

Expiry info: chage -l <username> (requires root to view other users).

What output is presented
Sectioned report:

User Identity: UID, primary group (name & GID), secondary groups, sudo user (Yes/No)

Login Activity: current (from w) + past sessions (from last)

Sudo Attempts: count of successes/failures

Account Expiry Details: chage -l output or a friendly error

Saved to: ~/user_reports/user_report_<username>_<timestamp>.txt (for the account running the script).

Requirements:

Linux (Debian/Ubuntu/CentOS-like) with:

/var/log/auth.log readable (run with sudo for best results)

chage, w, last available on PATH

Python 3 (standard library only)

Permission note: To inspect other users’ expiry data and read auth logs, run with 'sudo'


