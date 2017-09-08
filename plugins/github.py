import requests

from requests.auth import HTTPBasicAuth
from parser import Issue

issue1 = Issue('TODO', 'main.cpp', 10, 'Make method to parse strings')
issue2 = Issue('FIXME', 'box.cpp', 144, 'Redo this function', ['margaridaviterbo', 'joaosilva22'])
issue3 = Issue('NOTE', 'utils.cpp', 60, 'Is this necessary?', ['margaridaviterbo'])

issues = [issue1, issue2, issue3]

for issue in issues:
    content = issue.file + ':' + str(issue.lineno)
    requests.post('https://api.github.com/repos/portosummerofcode/break/issues',
        json = {'title':issue.comment, 'body':content, 'assignees':issue.assignees},
        auth=HTTPBasicAuth('margaridaviterbo', '23e00d57d8c0044429d8ff989f42dc0a9fad70e4'))
