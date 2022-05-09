import uuid

users = {
    "julian@gmail.com": {
        "email": "julian@gmail.com",
        "id": 4,
        "password": "example",
    },
    "clarissa@icloud.com": {
        "email": "clarissa@icloud.com",
        "id": 1,
        "password": "sweetpotato22",
    }
}

class DbLayer:
    def __init__(self):
        self.currentUsers = users

    def get_users(self):
        return self.currentUsers

    def user_exists(self, email):
        return email in self.currentUsers

    def register(self, email, password):
        account = {}
        account["email"] = email
        account["password"] = password
        account["id"] = str(uuid.uuid1())
        self.currentUsers[email] = account
        print(self.currentUsers)

