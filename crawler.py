# -*- coding: utf-8 -*-

from shibboleth_login import ShibbolethClient

name = "your username"
password = "your password"


def main():
    with ShibbolethClient(name, password) as client:
        res = client.get('URL where you want to access')

    soup = BeautifulSoup(res.text, "lxml")

    dates = soup.select('dd.nl_notice_date')
    charges = soup.select('dd.nl_div_in_charge')
    categories = soup.select('dd.nl_category')
    notices = soup.select('dd.nl_notice')

    for date, charge, category, notice in zip(dates, charges, categories, notices):
        print(date.get_text())
        print(charge.get_text())
        print(category.get_text())
        print(notice.get_text().replace("\t", ""))


if __name__ == "__main__":
    main()
