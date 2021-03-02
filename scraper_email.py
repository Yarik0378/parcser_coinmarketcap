import requests
from bs4 import BeautifulSoup
import csv
import time
from selenium import webdriver
from itertools import islice


def write_csv(data):
    if not data['email']:
        return None
    with open('email.csv', 'a') as f:
         writer = csv.writer(f, delimiter=',')
         writer.writerow([data['email']])


def get_html(url):
    r = requests.get(url)
    return r.text


# def refined(email):
#     r = email.split()[0]
#     return r.replace(',', '')


def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    uls = soup.find('div', class_='subsegment morecontact').select('ul')
    try:
        lis = uls[1].find_all('li')
        email = lis[0].find('a').contents[2]
        email = str(email)
        print(email.strip())
        data = {'email': email.strip()}
        write_csv(data)
    except IndexError:
        print('None')



def main():
    current = 0
    while current < 505:
        current += 1
        with open('cmc.csv') as file:
            order = ['position', 'name', 'link']
            reader = csv.DictReader(file, fieldnames=order)
            for row in reader:
                url = row['link']
                print(url)
                print(get_page_data(get_html(url)))



if __name__ == '__main__':
    main()