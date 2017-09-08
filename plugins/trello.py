import requests

from parser import Issue

issue1 = Issue('TODO', 'main.cpp', 10, 'Make method to parse strings')
issue2 = Issue('FIXME', 'box.cpp', 144, 'Redo this function', ['margaridaviterbo', 'joaosilva22'])
issue3 = Issue('NOTE', 'utils.cpp', 60, 'Is this necessary?', ['margaridaviterbo'])

issues = [issue1, issue2, issue3]

for issue in issues:
    content = issue.file + ':' + str(issue.lineno)
    requests.post()
