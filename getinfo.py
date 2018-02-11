# -*- coding: utf-8 -*-

from shibboleth_login import ShibbolethClient

name = "your username"
password = "your password"


def main():
    with ShibbolethClient(name, password) as client:
        res = client.get('URL where you want to access')
        print(type(res))  # => <class 'requests.models.Response'>
        print(res.text)


if __name__ == "__main__":
    main()
