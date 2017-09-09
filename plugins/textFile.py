import requests

from parser import Parser

def print_issues(issues, text_file):
    for issue in issues:
        text_file.write("[" + issue.file + ":" + str(issue.lineno) + "]" + " " + issue.comment)
        if len(issue.assignees) > 0:
            text_file.write(" (" + ", ".join(issue.assignees) + ")\n")
        else:
            text_file.write("\n")
    text_file.write("\n")
    return


parser = Parser('../test/intermediate.txt')
parser.Parse()

todos = []
fixmes = []
notes = []
for issue in parser.issues:
    if issue.tag == 'TODO':
        todos.append(issue)
    elif issue.tag == 'FIXME':
        fixmes.append(issue)
    elif issue.tag == 'NOTE':
        notes.append(issue)

text_file = open("../Tasks.txt", "w")
text_file.write("TODO:\n")
print_issues(todos, text_file)
text_file.write("FIXME:\n")
print_issues(fixmes, text_file)
text_file.write("NOTE:\n")
print_issues(notes, text_file)
text_file.close()
