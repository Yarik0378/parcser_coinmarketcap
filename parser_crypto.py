import requests
from bs4 import BeautifulSoup
import csv
import time
from selenium import webdriver

driver = webdriver.Chrome()


def scroll():
    last_height = driver.execute_script("return document.body.scrollHeight")

    current_height = 0
    while last_height > current_height:
        # Scroll down to bottom
        current_height += 1000
        driver.execute_script(f"window.scrollTo(0, {current_height});")

        # Wait to load page
        time.sleep(0.06)

        # Calculate new scroll height and compare with last scroll height


def html_from_driver(url):
    driver.get(url)
    scroll()
    return driver.page_source


def get_html(url):
    r = requests.get(url)
    return r.text


def write_csv(data):
    with open('cmc.csv', 'a') as f:
         writer = csv.writer(f)
         writer.writerow((data['position'],
                         data['name'],
                          data['prise'],
                          data['change_percent_24'],
                          data['change_percent_7']
                          ))


def plus_minus(value, serch_element):
    if serch_element is None:
        value = f'-{value}'
    else:
        value = f'+{value}'
    return value


def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')

    trs = soup.find('table', class_='cmc-table cmc-table___11lFC cmc-table-homepage___2_guh').\
        find('tbody').select('tr')

    for tr in trs:
        t = tr.select('td')

        if len(t) != 1:
            tds = tr.find_all('td')
            position = tds[1].find('p').text
            name = tds[2].find('p').text
            prise = tds[3].find('a').text
            change_percent_24 = tds[4].text
            change_percent_7 = tds[5].text
            up_24_hs = tds[4].find('span', class_='icon-Caret-up')
            up_7_ds = tds[5].find('span', class_='icon-Caret-up')
            value_24_hs = plus_minus(change_percent_24, up_24_hs)
            value_7_ds = plus_minus(change_percent_7, up_7_ds)

        data = {'name': name,
                'position': position,
                'prise': prise,
                'change_percent_24': value_24_hs,
                'change_percent_7': value_7_ds
                }
        print(data)
        write_csv(data)


def main():
    for page in range(0,41):
        url = f'https://coinmarketcap.com/?page={page}'
        print(get_page_data(html_from_driver(url)))
    driver.quit()


if __name__ == '__main__':
    main()
