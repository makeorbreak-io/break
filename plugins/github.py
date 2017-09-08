import requests

from requests.auth import HTTPBasicAuth
from parser import Parser

class IssueColection:
    def __init__(self, tag, content = None, comment = None, assignees = None):
        self.tag = tag
        self.comment = comment
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

'''metodo de usa variaveis de ambiente para inicializar password e username'''
'''SE VAIRAVEIS AMBIENTE NAO ESTAO SET PEDIR PARA CORRER SCRIPT
SE ESTIVEREM SET ATRIBUIR AO USERNAME E PASSWORD'''


session = requests.Session()
session.auth = (username, password)

parser = Parser('../test/intermediate.txt')
if (parser.Parse()):
    issues = session.get('https://api.github.com/repos/portosummerofcode/break/issues')
    githubIssues = issues.json()

    for i, gitIssue in enumerate(githubIssues):
        if githubIssues[i]['state'] == 'closed':
            githubIssues.pop(i)


    '''TODO collections nao estao a funcionar'''
    issuesCollections = []
    i = 0
    while (i <= len(parser.issues)):
        j = i + 1
        decrement = 0
        while (j <= len(parser.issues)):
            if parser.issues[i].comment == parser.issues[j].comment and parser.issues[i].tag == parser.issues[j].tag and parser.issues[i].assignees == parser.issues[j].assignees:
                decrement += 1
                match = False
                c1 = parser.issues[i].file + ':' + parser.issues[i].lineno
                for collection in issuesCollections:
                    if parser.issues[i].comment == collection.comment:
                        match = True
                        f1 = False
                        for content in collection.content:
                            if c1 == content:
                                f1 = True
                        if f1 == False:
                            content = content + '\n' + c1
                if match == False:
                    col = IssueColection(parser.issues[i].tag, c1, parser.issues[i].comment, parser.issues[i].assignees)
                    issuesCollections.append(col)
                parser.issues.pop(i)
            j += 1
        i += 1
        i -= decrement
        print(issuesCollections)


    for issue in parser.issues:
        match = False
        for i, gitIssue in enumerate(githubIssues):
            if githubIssues[i]['title'] == issue.comment:
                match = True
                url = 'https://api.github.com/repos/portosummerofcode/break/issues' + '/' + str(githubIssues[i]['number'])
                content = issue.file + ':' + str(issue.lineno)
                r = session.patch(url, json = {'body':content, 'labels':[issue.tag], 'assignees':issue.assignees})
                print(r.text)
                githubIssues.pop(i)
        if match == False:
            content = issue.file + ':' + str(issue.lineno)
            r = session.post('https://api.github.com/repos/portosummerofcode/break/issues',
                json = {'title':issue.comment, 'body':content, 'labels':[issue.tag], 'assignees':issue.assignees})
            print(r.text)

    for collection in issuesCollections:
        match = False
        for i, gitIssue in enumerate(githubIssues):
            if githubIssues[i]['title'] == collection.comment:
                match = True
                url = 'https://api.github.com/repos/portosummerofcode/break/issues' + '/' + str(githubIssues[i]['number'])
                r = session.patch(url, json = {'body':collection.content})
                print(r.text)
                githubIssues.pop(i)
        if match == False:
            r = session.post('https://api.github.com/repos/portosummerofcode/break/issues',
                json = {'title':collection.comment, 'body':collection.content, 'labels':[collection.tag], 'assignees':collection.assignees})
            print(r.text)


    for gitIssue in githubIssues:
        url = 'https://api.github.com/repos/portosummerofcode/break/issues' + '/' + str(gitIssue['number'])
        print(url)
        r = session.patch(url, json = {'state':'closed'})
        print(r.text)


else:
    print("Parse failed")




    '''Issue('TODO', 'main.cpp', 10, 'Make method to parse strings')'''
