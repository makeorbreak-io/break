import requests

from requests.auth import HTTPBasicAuth
from parser import Issue

issue1 = Issue('TODO', 'main.cpp', 10, 'Make method to parse strings')
issue2 = Issue('FIXME', 'box.cpp', 144, 'Redo this function', ['margaridaviterbo', 'joaosilva22'])
issue3 = Issue('NOTE', 'utils.cpp', 60, 'Is this necessary?', ['margaridaviterbo'])
newIssues = [issue1, issue2, issue3]

oldIssues = []
githubIssues = requests.get('https://api.github.com/repos/portosummerofcode/break/issues')

print(githubIssues.text)



for issue in newIssues:
    content = issue.file + ':' + str(issue.lineno)
    r = requests.post('https://api.github.com/repos/portosummerofcode/break/issues',
        json = {'title':issue.comment, 'body':content, 'labels':[issue.tag], 'assignees':issue.assignees},
        auth=HTTPBasicAuth('margaridaviterbo', '1081e5b5659e1c0f637416517b050f1c4ca3fa24'))
    print(r.text)

'''
for gitIssue in githubIssues
    oldIssues.append()
'''
