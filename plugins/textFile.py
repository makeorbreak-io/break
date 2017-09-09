import requests

from parser import Parser

class Plugin:
    def __init__(self, filepath, issues):
        self.filepath = filepath
        self.issues = issues

    def print_issues(self, issues, text_file):
        for issue in issues:
            text_file.write("[" + issue.file + ":" + str(issue.lineno) + "]" + " " + issue.comment)
            if len(issue.assignees) > 0:
                text_file.write(" (" + ", ".join(issue.assignees) + ")\n")
            else:
                text_file.write("\n")
        text_file.write("\n")
        return

    def run(self):
        todos = []
        fixmes = []
        notes = []
        for issue in self.issues:
            if issue.tag == 'TODO':
                todos.append(issue)
            elif issue.tag == 'FIXME':
                fixmes.append(issue)
            elif issue.tag == 'NOTE':
                notes.append(issue)

        try:
            text_file = open(self.filepath, "w")
        except IOError:
            return False
        with text_file:
            if len(todos) > 0:
                text_file.write("TODO:\n")
                self.print_issues(todos, text_file)
            if len(fixmes) > 0:
                text_file.write("FIXME:\n")
                self.print_issues(fixmes, text_file)
            if len(notes) > 0:
                text_file.write("NOTE:\n")
                self.print_issues(notes, text_file)
            text_file.close()
        return True

'''
test here
parser = Parser('../test/intermediate2.txt')
parser.Parse()
t = Plugin("../Tasks.txt", parser.issues)
t.run()
'''
