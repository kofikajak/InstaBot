from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pickle

class InstagramBot:

    def __init__ (self, username, password):
        self.browserProfile = webdriver.ChromeOptions()
        self.username = username
        self.password = password
        self.driver = webdriver.Chrome()

    def closeBrowser(self):
        self.driver.close()

    def login(self):
        driver = self.driver
        driver.get("https://www.instagram.com/accounts/login/")
        time.sleep(10)
        user_name_element = self.driver.find_elements_by_css_selector('form input')[0]
        user_name_element.clear()
        user_name_element.send_keys(self.username)
        time.sleep(3)
        password_element = self.driver.find_elements_by_css_selector('form input')[1]
        password_element.clear()
        password_element.send_keys(self.password)
        password_element.send_keys(Keys.RETURN)
        time.sleep(15)


    def unfollow(self, unfollowList):

        driver = self.driver
        for follower in unfollowList:
            driver.get(follower)
            time.sleep(5)
            try:
                followButton = driver.find_element_by_css_selector('button')
                if (followButton.text == 'Following') or (followButton.text == 'Obserwowanie'):
                    followButton.click()
                    time.sleep(5)
                    confirmButton = driver.find_element_by_class_name("-Cab_")
                    confirmButton.click()
                    time.sleep(5)
                else:
                    print("You are not following this user", follower)
            except Exception:
                time.sleep(2)
                continue
        time.sleep(5)

filename = r"C:\Users\Kajet\PycharmProjects\testPyCharm\UnfollowLists\unfollowListGit.txt"

with open(filename, 'rb') as fp:
    unfollowList = pickle.load(fp)

bot = InstagramBot('username', 'password')
bot.login()
bot.unfollow(unfollowList)
open(filename, 'w').close()
bot.closeBrowser()

