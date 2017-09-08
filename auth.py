import os
import requests

class GithubAuth:
    note = "Todos Authentication"
    base_url = "https://api.github.com/"

    def Authenticate(self, username, password):
        r = requests.get(self.base_url + "authorizations",
                         auth = (username, password))
        if r.status_code != 200:
            return None
        for auth in r.json():
            if auth["note"].lower() == self.note.lower():
                return auth["hashed_token"]            

        r = requests.post(self.base_url + "authorizations",
                          auth = (username, password),
                          json = {
                              "scopes": [
                                  "repo"
                              ],
                              "note": self.note
                          });
        if r.status_code == 201:
            return r.json()["hashed_token"]
        return None
