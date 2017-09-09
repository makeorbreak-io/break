import requests

from requests.auth import HTTPBasicAuth
from parser import Parser

class IssueColection:
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


'''TODO este metodo de pedir sempre as credenciais VAI SER ALTERADO pelo que está comentado abaixo?????'''
print("TODOS is asking for your GitHub credentials to update your issues.\n")
data = input('Username: ')
username = str(data)
data = input('Password: ')
password = str(data)
print('\n')

session = requests.Session()
session.auth = (username, password)

parser = Parser('../test/intermediate.txt')
if (parser.Parse()):
    issues = session.get('https://api.github.com/repos/portosummerofcode/break/issues')
    githubIssues = issues.json()

    if issues.status_code != 200:
        print("ERROR!")
        exit(1)

    i = 0
    while (i < len(githubIssues)):
        if githubIssues[i]['state'] == 'closed':
            githubIssues.pop(i)
        else:
            i += 1

    issuesCollections = []
    for i, issue1 in enumerate(parser.issues):
        match = False
        c1 = issue1.file + ':' + issue1.lineno
        for collection in issuesCollections:
            if issue1.comment == collection.comment and issue1.tag == collection.tag:
                match = True
                f1 = False
                for cont in collection.content:
                    if c1 == cont:
                        f1 = True
                if f1 == False:
                    collection.content.append(c1)
                f1 = False
                for ass in  issue1.assignees:
                    for ass2 in collection.assignees:
                        if ass == ass2:
                            f1 = True
                    if f1 == False:
                        collection.assignees.append(ass)
                    f1 = False
        if match == False:
            col = IssueColection(issue1.tag, [c1], issue1.comment, issue1.assignees)
            issuesCollections.append(col)





    for collection in issuesCollections:
        string = ''
        for content in collection.content:
            string += content + '\n'
        match = False
        for i, gitIssue in enumerate(githubIssues):
            if githubIssues[i]['title'] == collection.comment and githubIssues[i]['labels'][0]['name'] == collection.tag:
                match = True
                url = 'https://api.github.com/repos/portosummerofcode/break/issues' + '/' + str(githubIssues[i]['number'])
                r = session.patch(url, json = {'body':string, 'assignees':collection.assignees})
                githubIssues.pop(i)
        if match == False:
            r = session.post('https://api.github.com/repos/portosummerofcode/break/issues',
                json = {'title':collection.comment, 'body':string, 'labels':[collection.tag], 'assignees':collection.assignees})


    for gitIssue in githubIssues:
        url = 'https://api.github.com/repos/portosummerofcode/break/issues' + '/' + str(gitIssue['number'])
        r = session.patch(url, json = {'state':'closed'})


else:
    print("Parse failed")
