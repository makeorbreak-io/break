class Issue:
    def __init__(self, tag, file, lineno, comment, assignees = None):
        self.tag = tag
        self.file = file
        self.lineno = lineno
        self.comment = comment
        if assignees is None:
            self.assignees = []
        else:
            self.assignees = assignees

        
        

