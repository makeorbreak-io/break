import requests

class IssueCollection:
    def __init__(self, tag, content = None, comment = None, assignees = None):
        self.tag = tag
        self.comment = comment
        if content is None:
            self.content = []
        else:
            self.content = content
        if assignees is None:
            self.assignees = []
        else:
            self.assignees = assignees

class Plugin:
    def __init__(self, token, key, issues, board, task_list, done_list, tags):
        self.token = token
        self.key = key
        self.issues = issues
        self.board = board
        self.task_list = task_list
        self.done_list = done_list
        self.tags = tags

    def run(self):
        issue_collections = []
        for i, issue in enumerate(self.issues):
            match = False
            issue_file_lineno = issue.file + ":" + str(issue.lineno)
            for collection in issue_collections:
                if issue.comment == collection.comment and issue.tag == collection.tag:
                    match = True
                    
                    for collection_file_lineno in collection.content:
                        found_line = False
                        if issue_file_lineno == collection_file_lineno:
                            found_line = True
                    if not found_line:
                        collection.content.append(issue_file_lineno)
                        
                    for issue_assignee in issue.assignees:
                        found_assignee = False
                        for collection_assignee in collection.assignees:
                            if issue_assignee == collection_assignee:
                                found_assignee = True
                        if not found_assignee:
                            collection.assignees.append(issue_assignee)

            if not match:
                collection = IssueCollection(issue.tag, [issue_file_lineno], issue.comment, issue.assignees)
                issue_collections.append(collection)

        r = requests.get("https://api.trello.com/1/lists/" + self.task_list + "/cards?key=" + self.key + "&token=" + self.token);
        if r.status_code < 200 or r.status_code > 299:
            return False
        task_cards = r.json()

        r = requests.get("https://api.trello.com/1/lists/" + self.done_list + "/cards?key=" + self.key + "&token=" + self.token);
        if r.status_code < 200 or r.status_code > 299:
            return False
        done_cards = r.json()

        to_add = [collection for collection in issue_collections if not any(collection.comment == card["name"] and collection.tag == card["labels"][0]["name"] for card in task_cards) and not any(collection.comment == card["name"] and collection.tag == card["labels"][0]["name"] for card in done_cards)]
        to_update = [collection for collection in issue_collections if collection not in to_add]
        to_delete = [card for card in task_cards if not any(card["name"] == collection.comment and card["labels"][0]["name"] == collection.tag for collection in issue_collections)]

        for collection in to_add:
            r = requests.post("https://api.trello.com/1/cards", json = {"key":self.key, "token":self.token, "idList":self.task_list, "name":collection.comment})
            if r.status_code < 200 or r.status_code > 299:
                return False
            card_id = r.json()["id"]
            color = self.tags[collection.tag]
            r = requests.post("https://api.trello.com/1/cards/" + card_id + "/labels", json = {"key":self.key, "token":self.token, "color":color, "name":collection.tag})
        
        return True

        
