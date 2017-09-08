import os
import sys
import getpass
from auth import GithubAuth

def query_yes_no(question, default=None):
    if default is True:
        prompt = " [Y/n] "
    elif default is False:
        prompt = " [y/N] "
    else:
        prompt = " [y/n] "

    while (True):
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == "":
            return default
        elif choice == "yes" or choice == "y":
            return True
        elif choice == "no" or choice == "n":
            return False
        sys.stdout.write("Please respond with 'yes' or 'no'\n");

def query_string(question, password=False):
    while (True):
        sys.stdout.write(question)
        response = input().lower()
        if response.strip() != "":
            return response.strip()

if not len(sys.argv) != 1:
    print("usage: " + sys.argv[0] + " <command> [<args>]")
    exit(1)

if sys.argv[1] == "init":
    if os.path.isfile("todosconfig.toml"):
        print(sys.argv[0] + ": already been initialized.")
        exit(1)
    
    github = query_yes_no("Do you want to create github issues?", False)
    if github:
        try_number = 0
        while try_number < 3:
            username = query_string("Please enter your github username: ")
            password = getpass.getpass("Please enter your github password: ")
            github_auth = GithubAuth().Authenticate(username, password)
            if github_auth is not None:
                break
            else:
                print("Bad credentials, please try again")
        if github_auth is None:
            print("Bad credentials, aborting.")
            exit(1)
    f = open("todosconfig.toml", "w")
    f.write("github_token = \"" + github_auth + "\"\n")
    
    f = open(".gitignore", "a+")
    f.write("\ntodosconfig.toml\n");
    
else:
    print(sys.argv[0] + ": is not a " + sys.argv[0] + " command.")
    
