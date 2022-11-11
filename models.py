import csv
from flask_login import UserMixin


class User(UserMixin):
    id = 0
    email = ""
    password = ""
    name = "" 
    def __init__(self, id, email, name, password):
        self.id = id
        self.email =  email
        self.isAdmin = email in ["mario@gmail.nl","luigi@gmail.nl"]
        self.name = name
        self.password = password
        
    def get(email = False, id = False):
        with open("data.csv", "r") as file:
            for user in csv.DictReader(file):
                if email == user["email"]:
                    return User(user["id"], user["email"], user["name"], user["password"])
                if id == user["id"]:
                    return User(user["id"], user["email"], user["name"], user["password"])

    def create(value):
        with open("data.csv","a", newline="") as csvfile:
            writer = csv.writer(csvfile, delimiter=",", quoting=csv.QUOTE_ALL)
            writer.writerow(value)
