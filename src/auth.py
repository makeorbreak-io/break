import os
import requests

class GithubAuth:
    base_url = "https://api.github.com/"

    def Authenticate(self, username, password, fingerprint):
        r = requests.put(self.base_url + "authorizations/clients/be72b42d342d7fa292c8/" + fingerprint,
                         auth = (username, password),
                         json = {
                             "client_secret":"0448bc98a72d9db7f8d2362ce046bb8b46de646d",
                             "scopes": [
                                 "repo",
                             ]
                         })
        json = r.json()
        if r.status_code >= 200 and r.status_code < 300:
            if json["token"] != "":
                return json["token"]
