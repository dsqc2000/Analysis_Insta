from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
import time
from datetime import datetime
import pickle
import os
from config import settings

options = webdriver.ChromeOptions()
options.binary_location = '/usr/bin/google-chrome'
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(options=options)


class CollectUtil:
    def __init__(self):

        # creating an instane of our webdriver and applying options
        self._driver = driver
        self._cookies_path = settings.SELENIUM_COOKIE_PATH
        self._driver.get('https://www.instagram.com')
        time.sleep(5)
        self._logged_in = False

    def _get_post(self, link):
        link.click()
        time.sleep(5)
        post_link = link.get_attribute('href')
        post_caption = self._driver.find_element(
            By.XPATH, '/html/body/div[2]/div/div/div[3]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/div[1]/ul/div/li/div/div/div[2]/div[1]/h1').text

        likes_count = self._driver.find_element(
            By.XPATH, '/html/body/div[2]/div/div/div[3]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/section[2]/div/div/span/a/span/span').text
        likes_count = int(likes_count)
        return post_link, post_caption, likes_count
    
    def collect_post(self, row, column):
        post_entry = {}
        try:
            link = self._driver.find_element(
                By.XPATH, f'/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/div[3]/article/div[1]/div/div[{row}]/div[{column}]/a')
           
            post_link, post_caption, likes_count = self._get_post(link)
            comments = []
            comments_count = 0
            i = 1
            while True:
                try:
                    comment = self._get_comment(i)
                    comments.append(comment.text)
                    comments_count += 1
                    i += 1
                    try:
                        load_more = self._driver.find_element(
                            By.XPATH, '/html/body/div[2]/div/div/div[3]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/div[1]/ul/li/div/button')
                        load_more.click()
                    except:
                        continue
                except:
                    print("didn't find comment element")
                    break
            self._close_post()

        except:
            return
        scrapes = []
        scrape = {}
        scrape['scrape_date'] = datetime.now().strftime(
            "%d/%m/%Y, %H:%M:%S")
        scrape['comments_count'] = comments_count
        scrape['likes_count'] = likes_count
        scrapes.append(scrape)
        post_entry['added_date'] = datetime.now().strftime(
            "%d/%m/%Y, %H:%M:%S")
        post_entry['post_link'] = post_link
        post_entry['post_caption'] = post_caption
        post_entry['likes_count'] = likes_count
        post_entry['comments'] = comments
        post_entry['comments_count'] = comments_count
        post_entry['scrapes'] = scrapes
        return post_entry


    def collect_data(self, row, column):
        print("start collecting")
        #if self._logged_in == False:
            #self._login()
        #time.sleep(3)
        self._driver.get('https://www.instagram.com/tickticktrader/')
        time.sleep(3)
        post_entry  = self.collect_post(row, column)
        return post_entry

    def posts_count(self):
        if not self._logged_in:
            time.sleep(5)
            self._login()
            time.sleep(5)
        self._driver.get('https://www.instagram.com/tickticktrader/')
        time.sleep(3)
        posts_counts = self._driver.find_element(
                By.XPATH, f'/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[1]/span/span').text
        posts_counts = int(posts_counts)
        return posts_counts

    def _close_post(self):
        close_post = self._driver.find_element(
            By.XPATH, '/html/body/div[2]/div/div/div[3]/div/div/div[1]/div/div[2]/div')
        close_post.click()

    def _get_comment(self,  i):
        comment = self._driver.find_element(
            By.XPATH, f'/html/body/div[2]/div/div/div[3]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/div[1]/ul/ul[{i}]/div/li/div/div/div[2]/div[1]/span')
        return comment

    def _login(self):
        print("Loging in ...")
        if os.path.isfile(self._cookies_path):
            print("Using cookies to login ...")
            cookies = pickle.load(open(self._cookies_path, "rb"))
            for cookie in cookies:
                self._driver.add_cookie(cookie)
            self._driver.get('https://www.instagram.com')
            self._logged_in = True 

        else:
            print("Manual login and saving cookies ...")
            self._driver.find_element(
                By.XPATH, '//*[@id="loginForm"]/div/div[1]/div/label/input').send_keys("bellouchelhassan")
            time.sleep(10)
            self._driver.find_element(
                By.XPATH, '//*[@id="loginForm"]/div/div[2]/div/label/input').send_keys("jLq8ySCQ3tX5d7s")
            time.sleep(10)
            self._driver.find_element(
                By.XPATH, '//*[@id="loginForm"]/div/div[3]').click()
            self._logged_in = True
            time.sleep(10)
            pickle.dump(self._driver.get_cookies(),
                        open(self._cookies_path + "/cookies.pkl", "wb"))
            print("Logged in and cookie saved ...")


collect_util = CollectUtil()
