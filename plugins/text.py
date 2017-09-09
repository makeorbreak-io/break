import requests

class Plugin:
    def __init__(self, filepath, issues, tags):
        self.filepath = filepath
        self.issues = issues
        self.tags = tags

    def print_issues(self, issues, text_file):
        for issue in issues:
            text_file.write("[" + issue.file + ":" + str(issue.lineno) + "]" + " " + issue.comment)
            if len(issue.assignees) > 0:
                text_file.write(" (" + ", ".join(issue.assignees) + ")\n")
            else:
                text_file.write("\n")
        text_file.write("\n")
        return

    def groupIssues(self, tag, text_file):
        issuesGroup = []
        for issue in self.issues:
            if issue.tag == tag:
                issuesGroup.append(issue)
        if len(issuesGroup) > 0:
            text_file.write(tag + ":\n")
            self.print_issues(issuesGroup, text_file)
        return

    def run(self):
        try:
            text_file = open(self.filepath, "w")
        except IOError:
            return False
        with text_file:
            for tag in self.tags:
                self.groupIssues(tag, text_file)
        text_file.close()
        return True
