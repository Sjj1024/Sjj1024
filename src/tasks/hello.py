import requests
from src.utils.github.config import *


def login():
    headers = {"Authorization": "token %s" % token, 'Accept': 'application/vnd.github.v3+json',
               'Content-Type': 'application/json'}
    login = requests.get(f"{base_url}/user", headers=headers)
    print(login.json())


def get_progect(id):
    headers = {"Authorization": "token %s" % token, 'Accept': 'application/vnd.github.v3+json',
               'Content-Type': 'application/json'}
    login = requests.get(f"{base_url}/projects/{id}", headers=headers)
    print(login.json())


if __name__ == '__main__':
    get_progect()