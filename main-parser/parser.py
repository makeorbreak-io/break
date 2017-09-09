from lexer import Lexer, Tokens

class Issue:
    def __init__(self, tag, file, lineno):
        self.tag = tag
        self.file = file
        self.lineno = lineno
        self.assignees = []
        self.comment = ""

    def __str__(self):
        base = ":tag " + self.tag + "\n:file " + self.file + "\n:lineno " + str(self.lineno) + "\n:"
        for assignee in self.assignees:
            base += "assignee " + assignee + "\n:"
        if self.comment != "":
            processed_comment = self.comment.strip().replace("( ", "(").replace(" )", ")").replace(" ,", ",")
            base += "comment " + processed_comment
        return base + "\n"
        

class Parser:
    def __init__(self, rootdir):
        self.index = 0
        lexer = Lexer(rootdir)
        lexer.begin()
        self.tokens = lexer.tokens
        self.issues = []
        self.current_issue = None

    def next_token(self):
        if self.index < len(self.tokens):
            token = self.tokens[self.index]
            self.index += 1
            return token
        return None

    def start(self):
        # make sure that the token is not None
        token = self.next_token()
        if token is not None:
            return self.issue(token)

    def issue(self, token):
        if token.id == Tokens.Tag:
            self.current_issue = Issue(token.image, token.file, token.lineno)
            token = self.next_token()
            if token.id == Tokens.OpenParen:
                token = self.next_token()
                return self.assignee(token)
            elif token.id == Tokens.Colon:
                token = self.next_token()
                return self.comment(token)
            return self.start()
        return self.start()

    def assignee(self, token):
        if token.id == Tokens.Word:
            self.current_issue.assignees.append(token.image)
            token = self.next_token()
            if token.id == Tokens.CloseParen:
                token = self.next_token()
                if token.id == Tokens.Colon:
                    token = self.next_token()
                    return self.comment(token)
                return self.start()
            elif token.id == Tokens.Comma:
                token = self.next_token()
                return self.assignee(token)
            return self.start()
        return self.start()

    def comment(self, token):
        if token.id == Tokens.EOL:
            self.issues.append(self.current_issue)
            return self.start()
        self.current_issue.comment += " " + token.image
        token = self.next_token()
        return self.comment(token)

    def parse(self):
        self.start()
        with open(".todos", "w") as f:
            for issue in self.issues:
                f.write(str(issue) + "\n")
            f.close()

parser = Parser("../test")
parser.parse()
            
            
