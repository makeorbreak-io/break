import os
import sys
import getpass
import toml

from auth import GithubAuth
from parser.parser import Parser
from plugins.github import Plugin as GithubPlugin

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

def query_string(question, default=""):
    while (True):
        sys.stdout.write(question)
        response = input().lower()
        if response.strip() != "":
            return response.strip()
        elif default != "":
            return default

# Main functionality
if len(sys.argv) == 1:
    if not os.path.isfile(os.getcwd() + "/todosconfig.toml"):
        print(sys.argv[0] + ": cannot find todosconfig.toml.")
        exit(1)

    parser = Parser(os.getcwd())
    parser.parse()
    issues = parser.issues

    with open(os.getcwd() + "/todosconfig.toml", "r") as f:
        config = toml.loads(f.read())

        # Output to github issues
        if any("github" in s for s in config["target"]):
            github_repo = config["github-repo"]
            if github_repo.endswith("/"):
                parts = github_repo.split("/")
                github_repo_user = parts[len(parts)-3]
                github_repo_name = partr[len(parts)-2]
            else:
                parts = github_repo.split("/")
                github_repo_user = parts[len(parts)-2]
                github_repo_name = parts[len(parts)-1]

            plugin = GithubPlugin(config["github-token"], issues, github_repo_user, github_repo_name)
            success = plugin.run()
            if not success:
                print(sys.argv[0] + ": failed to output to github.")            
        
# Init functionality
elif sys.argv[1] == "init":
    if os.path.isfile("todosconfig.toml"):
        print(sys.argv[0] + ": already been initialized.")
        exit(1)

    current_dir = os.path.basename(os.path.dirname(os.path.realpath(__file__)))
    project_name = query_string("What is the name of the project? [" + current_dir + "]", current_dir)
    
    github = query_yes_no("Do you want to create github issues?", False)
    github_auth = None
    github_repo = None
    if github:
        try_number = 0
        while try_number < 3:
            username = query_string("Please enter your github username: ")
            password = getpass.getpass("Please enter your github password: ")
            github_auth = GithubAuth().Authenticate(username, password, project_name)
            if github_auth is not None:
                github_repo = query_string("Please enter the link to the github repository: ")
                break
            else:
                print("Bad credentials, please try again")
        if github_auth is None:
            print("Bad credentials, aborting.")
            exit(1)

    config = {
        "title": project_name,
        "tags": [],
        "target": []
    }
    
    if github_auth is not None:
        config["github-token"] = github_auth
        config["github-repo"] = github_repo
        config["target"].append("github")
    
    with open(os.getcwd() + "/todosconfig.toml", "w") as f:
        f.write(toml.dumps(config))
    
    f = open(".gitignore", "a+")
    f.write("\ntodosconfig.toml\n");
    
else:
    print(sys.argv[0] + ": is not a " + sys.argv[0] + " command.")
    
