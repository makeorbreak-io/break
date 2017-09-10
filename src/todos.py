import os
import sys
import getpass
import toml
import requests

from .auth import GithubAuth
from src.parser.parser import Parser
from src.plugins.github import Plugin as GithubPlugin
from src.plugins.text import Plugin as TextPlugin
from src.plugins.trello import Plugin as TrelloPlugin

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

trello_api_key = "d63a77f604be006624b28e02159ce9a9"

# Main functionality
def main():
    if len(sys.argv) == 1:
        if not os.path.isfile(os.getcwd() + "/todosconfig.toml"):
            print(sys.argv[0] + ": cannot find todosconfig.toml. Run 'todos init' to create it.")
            exit(1)

        with open(os.getcwd() + "/todosconfig.toml", "r") as f:
            config = toml.loads(f.read())

            tags = config["tags"]
            tag_names = tags.keys()

            parser = Parser(os.getcwd(), tag_names)
            parser.parse()
            issues = parser.issues

            # Output to text file
            text_path = config["text-path"] + "/Tasks.txt"
            plugin = TextPlugin(text_path, issues, tag_names)
            success = plugin.run()

            if not success:
                print(sys.argv[0] + ": failed to output to text file.")

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

            # Output to trello issues
            if any("trello" in s for s in config["target"]):
                plugin = TrelloPlugin(config["trello-token"],
                                      trello_api_key,
                                      issues,
                                      config["trello-board"],
                                      config["trello-tasks-list"],
                                      config["trello-done-list"],
                                      tags) # Change this
                success = plugin.run()

                if not success:
                    print(sys.argv[0] + ": failed to output to trello.")


    # Init functionality
    elif sys.argv[1] == "init":
        if os.path.isfile("todosconfig.toml"):
            print(sys.argv[0] + ": already been initialized.")
            exit(1)

        try:
            current_dir = os.path.basename(os.path.realpath(os.getcwd()))
            project_name = query_string("What is the name of the project? [" + current_dir + "] ", current_dir)

            text_path = query_string("Where should the output file be placed? [" + os.getcwd() + "] ", os.getcwd())

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
                        print(sys.argv[0] + ": bad credentials, aborting.")
                if github_auth is None:
                    print(sys.argv[0] + ": bad credentials, aborting.")
                    exit(1)

            trello = query_yes_no("Do you want to put your tasks on a trello board?", False)
            trello_token = None
            todo_list = None
            done_list = None
            if trello:
                print("Get your application token from:")
                print("https://trello.com/1/authorize?key=" + trello_api_key + "&name=TODOS&expiration=never&response_type=token&scope=read,write")
                trello_token = query_string("Paste your token here: ")
                trello_board = query_string("What's the name of the trello board? [" + current_dir + "] ", current_dir)

                # Create the trello board
                r = requests.get("https://trello.com/1/members/my/boards?key=" + trello_api_key + "&token=" + trello_token)
                if r.status_code < 200 or r.status_code > 299:
                    print(sys.argv[0] + ": bad credentials, aborting.")
                    exit(1)
                else:
                    boards = r.json()
                    if not any(x["name"] == trello_board for x in boards):
                        r = requests.post("https://trello.com/1/boards", json = {"key": trello_api_key, "token": trello_token, "name": trello_board, "defaultLists": False})
                        board = r.json()
                        board_id = board["id"]
                    else:
                        board_id = [x["id"] for x in boards if x["name"] == trello_board][0]

                    r = requests.get("https://api.trello.com/1/boards/" + board_id + "/lists?key=" + trello_api_key + "&token=" + trello_token)
                    board_lists = r.json()
                    
                    # Check if the list exists first
                    if any(x["name"] == "TODOS Done" for x in board_lists):
                        done_list = [x["id"] for x in board_lists if x["name"] == "TODOS Done"][0]
                    else:
                        r = requests.post("https://trello.com/1/boards/" + board_id + "/lists", json = {"key": trello_api_key, "token": trello_token, "name": "TODOS Done", "defaultLists": False})
                        if r.status_code < 200 or r.status_code > 299:
                            print(sys.argv[0] + ": failed to create trello board, aborting.")
                            exit(1)
                        else:
                            list = r.json()
                            done_list = list["id"]

                    # Check if the list exists first
                    if any(x["name"] == "TODOS Tasks" for x in board_lists):
                        todo_list = [x["id"] for x in board_lists if x["name"] == "TODOS Tasks"][0]
                    else:
                        r = requests.post("https://trello.com/1/boards/" + board_id + "/lists", json = {"key": trello_api_key, "token": trello_token, "name": "TODOS Tasks", "defaultLists": False})
                        if r.status_code < 200 or r.status_code > 299:
                            print(sys.argv[0] + ": failed to create trello board, aborting.")
                            exit(1)
                        else:
                            list = r.json()
                            todo_list = list["id"]
                            
        except KeyboardInterrupt:
            print("")
            exit(1)
            
        config = {
            "title": project_name,
            "tags": {
                "TODO": "yellow",
                "FIXME": "red",
                "NOTE": "green",
            },
            "target": [],
            "text-path": text_path
        }

        if github:
            config["target"].append("github")
            config["github-token"] = github_auth
            config["github-repo"] = github_repo
            
        if trello:
            config["target"].append("trello")
            config["trello-token"] = trello_token
            config["trello-board"] = board_id
            config["trello-tasks-list"] = todo_list
            config["trello-done-list"] = done_list

        with open(os.getcwd() + "/todosconfig.toml", "w") as f:
            f.write(toml.dumps(config))

        f = open(".gitignore", "a+")
        f.write("\ntodosconfig.toml\nTasks.txt\n.todos\n")

    else:
        print(sys.argv[0] + ": is not a " + sys.argv[0] + " command.")
