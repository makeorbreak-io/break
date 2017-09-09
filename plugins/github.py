import requests

from requests.auth import HTTPBasicAuth
from .parser import Parser

class IssueCollection:
    def __init__(self, tag, content = None, comment = None, assignees = None):
        self.tag = tag
        self.comment = comment
        if content is None:
            self.content = []
        else:
            self.content = content
        if assignees is None:
            self.assignees = []
        else:
            self.assignees = assignees

class Plugin:
    def __init__(self, token, issues, repo_user, repo_name):
        self.token = token
        self.issues = issues
        self.session = requests.Session()
        self.session.headers.update({"Authorization": "token " + self.token})
        self.repo_user = repo_user
        self.repo_name = repo_name

    def run(self):
        r = self.session.get("https://api.github.com/repos/" + self.repo_user + "/" + self.repo_name + "/issues")
        if r.status_code != 200:
            return False
        
        github_issues = r.json()
        open_issues = [x for x in github_issues if x["state"] != "closed"]

        issue_collections = []
        for i, issue in enumerate(self.issues):
            match = False
            issue_file_lineno = issue.file + ":" + str(issue.lineno)
            for collection in issue_collections:
                if issue.comment == collection.comment and issue.tag == collection.tag:
                    match = True
                    
                    for collection_file_lineno in collection.content:
                        found_line = False
                        if issue_file_lineno == collection_file_lineno:
                            found_line = True
                    if not found_line:
                        collection.content.append(issue_file_lineno)
                        
                    for issue_assignee in issue.assignees:
                        found_assignee = False
                        for collection_assignee in collection.assignees:
                            if issue_assignee == collection_assignee:
                                found_assignee = True
                        if not found_assignee:
                            collection.assignees.append(issue_assignee)

            if not match:
                collection = IssueCollection(issue.tag, [issue_file_lineno], issue.comment, issue.assignees)
                issue_collections.append(collection)

        for collection in issue_collections:
            string = ''
            for content in collection.content:
                string += content + "\n"
            match = False
            for i, github_issue in enumerate(github_issues):
                if github_issue["title"] == collection.comment and github_issue["labels"][0]["name"] == collection.tag:
                    match = True
                    url = "https://api.github.com/repos/" + self.repo_user + "/" + self.repo_name + "/issues/" + str(github_issue["number"])
                    r = self.session.patch(url, json = {"body":string, "assignees":collection.assignees})
                    if r.status_code < 200 or r.status_code > 299:
                        return False
                    github_issues.pop(i)
            if match == False:
                r = self.session.post("https://api.github.com/repos/" + self.repo_user + "/" + self.repo_name + "/issues", json = {"title":collection.comment, "body":string, "labels":[collection.tag], "assignees":collection.assignees})
                if r.status_code < 200 or r.status_code > 299:
                    print(r.text)
                    return False
        for github_issue in github_issues:
            url = "https://api.github.com/repos/" + self.repo_user + "/" + self.repo_name + "/issues/" + str(github_issue["number"])
            r = self.session.patch(url, json = {"state":"closed"})
            if r.status_code < 200 or r.status_code > 299:
                return False

        return True

