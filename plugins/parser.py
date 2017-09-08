class Issue:
    def __init__(self, tag, file = None, lineno = None, comment = None, assignees = None):
        self.tag = tag
        self.file = file
        self.lineno = lineno
        self.comment = comment
        if assignees is None:
            self.assignees = []
        else:
            self.assignees = assignees

class Parser:   
    def __init__(self, filepath):
        self.tokens = open(filepath, 'r').read().split()
        self.index = 0
        self.issues = []

    def NextToken(self):
        if self.index < len(self.tokens):
            token = self.tokens[self.index]            
            self.index += 1
            return token
        return None

    def Parse(self):
        token = self.NextToken()
        return self.Tag(token)

    def Tag(self, token):
        if token == ":tag":
            token = self.NextToken()
            if token is not None:
                issue = Issue(token)
                token = self.NextToken()
                return self.Parameter(token, issue)
            else:
                return False
        elif token == None:
            return True

    def Parameter(self, token, issue):
        if token == ":file":
            token = self.NextToken()
            if token is not None:
                issue.file = token
                token = self.NextToken()
                return self.Parameter(token, issue)
            else:
                return False
        elif token == ":lineno":
            token = self.NextToken()
            if token is not None:
                issue.lineno = token
                token = self.NextToken()
                return self.Parameter(token, issue)
            else:
                return False
        elif token == ":assignee":
            token = self.NextToken()
            assignee = ""
            while token != None and not token.startswith(":"):
                assignee += " " + token
                token = self.NextToken()
            if assignee == "":
                return False
            else:
                issue.assignees.append(assignee.strip())
                return self.Parameter(token, issue)
        elif token == ":comment":
            token = self.NextToken()
            comment = ""
            while token != None and not token.startswith(":"):
                comment += " " + token
                token = self.NextToken()
            if comment == "":
                return False
            else:
                issue.comment = comment.strip()
                return self.Parameter(token, issue)
        else:            
            if issue.comment is not None:
                self.issues.append(issue)                
                return self.Tag(token)
            else:
                return False

"""
Example usage:

parser = Parser('../test/intermediate.txt')
if (parser.Parse()):
    print("Parse was successful; Created " + str(len(parser.issues)) + " issues.")
    for issue in parser.issues:
        print(issue.tag,
              issue.file,
              issue.lineno,
              issue.assignees,
              issue.comment)
else:
    print("Parse failed")
"""     
        

