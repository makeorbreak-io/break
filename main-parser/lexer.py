import os

class Tokens:
    Tag, OpenParen, Word, Comma, CloseParen, Colon, EOL = range(7)

class Token:
    def __init__(self, image, id, file = None, lineno = None):
        self.image = image
        self.id = id
        self.file = file
        self.lineno = lineno

    def __str__(self):
        base = "(" + self.image + ", " + str(self.id) + ")"
        if self.file is not None and self.lineno is not None:
            base += " " + self.file + ":" + str(self.lineno)
        return base

class Lexer:    
    inline_comment = 1
    block_comment = 2

    lineno = 1
    
    def __init__(self, rootdir):
        self.tokens = []
        self.rootdir = rootdir

    def begin(self):
        self.tokenize_dir(self.rootdir)

    def tokenize_dir(self, rootdir):
        for root, subdirs, files in os.walk(rootdir):
            for file in files:
                filepath = os.path.join(root, file)
                self.file = file
                self.tokenize_file(filepath)
            for subdir in subdirs:
                self.tokenize_dir(subdir)

    def match_token(self, content, index, word):
        return content[index:index+len(word)] == word

    def match_tokens(self, content, index, words):
        results = [word for word in words if self.match_token(content, index, word)]
        if len(results) > 0:
            return results[0]

    def match_word(self, content, index):
        if content[index] == " ":
            return
        i = index
        while (i < len(content)):
            if self.match_tokens(content, i, ["(", ")", ",", ":", "\n", " "]):
                return content[index:i]
            i += 1

    def tokenize_file(self, filepath):
        self.lineno = 1
        f = open(filepath, "r")
        content = f.read()
        
        i = 0
        while (i < len(content)):
            if self.match_token(content, i, "//"):
                i = self.tokenize(content, i+2, self.inline_comment)
            elif self.match_token(content, i, "/*"):
                i = self.tokenize(content, i+2, self.block_comment)
            elif self.match_token(content, i, "#"):
                i = self.tokenize(content, i+1, self.inline_comment)
            elif self.match_token(content, i, "\n"):
                self.lineno += 1
            i += 1

    def tokenize(self, content, index, comment_type):
        i = index
        while (i < len(content)):
            tag = self.match_tokens(content, i, ["TODO", "FIXME", "NOTE"])
            if tag:
                self.tokens.append(Token(tag.strip(), Tokens.Tag, self.file, self.lineno))
                i += len(tag.strip())

            open_paren = self.match_tokens(content, i, ["("])
            if open_paren:
                self.tokens.append(Token(open_paren.strip(), Tokens.OpenParen))
                i += len(open_paren.strip()) - 1

            close_paren = self.match_tokens(content, i, [")"])
            if close_paren:
                self.tokens.append(Token(close_paren.strip(), Tokens.CloseParen))
                i += len(close_paren.strip()) - 1

            comma = self.match_tokens(content, i, [","])
            if comma:
                self.tokens.append(Token(comma.strip(), Tokens.Comma))
                i += len(comma.strip()) - 1

            colon = self.match_tokens(content, i, [":"])
            if colon:
                self.tokens.append(Token(colon.strip(), Tokens.Colon))
                i += len(colon.strip()) - 1

            eol = self.match_tokens(content, i, ["\n"])
            if eol or i == len(content) - 1:
                self.lineno += 1
                self.tokens.append(Token("EOL", Tokens.EOL))
                if comment_type == self.inline_comment:
                    return i

            close_block_comment = self.match_tokens(content, i, ["*/"])
            if close_block_comment and comment_type == self.block_comment:
                return i + 2

            word = self.match_word(content, i)
            if word:
                self.tokens.append(Token(word.strip(), Tokens.Word))
                i += len(word) - 1
                
            i += 1
