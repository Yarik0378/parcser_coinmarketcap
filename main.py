import requests
from bs4 import BeautifulSoup
import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()


def scroll():
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(2)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        print(new_height, last_height)
        if new_height == last_height:
            try:
                button = driver.find_element(By.XPATH, '//button[text()="460 weitere Treffer anzeigen"]')
                button.click()
            except:
                break
        last_height = new_height


def write_csv(data):
    with open('cmc.csv', 'a', encoding="utf-8") as f:
         writer = csv.writer(f)
         writer.writerow((data['position'],
                          data['name'],
                          data['href']
                          ))


def html_from_driver(url):
    driver.get(url)
    scroll()
    return driver.page_source


def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    div = soup.select('div', class_='entrycontainer clearfix ')
    element = 0
    while element < 505:
        element += 1
        entry = soup.find('div', {'id': f'entry_{element}'})
        name = entry.find('a').text
        href = entry.find('a').get('href')
        print(name.strip())
        print(href)
        data = {'position': element,
                'name': name.strip(),
                'href': href
                }
        write_csv(data)

def main():
    url = 'https://www.dastelefonbuch.de/Suche/Call%20Center'
    print(get_page_data(html_from_driver(url)))


if __name__ == '__main__':
    main()
