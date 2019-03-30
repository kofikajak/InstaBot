from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pickle
import os

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


    def followList(self, accounts, limit):
        driver = self.driver
        followList = ['https://www.instagram.com/instagram/']
        for account in accounts:
            if len(followList) < limit:
                driver.get('https://www.instagram.com/' + account + '/')
                time.sleep(2)
                following = driver.find_elements_by_css_selector('ul li a')[0]
                following.click()
                time.sleep(3)
                followingList = self.driver.find_element_by_css_selector('div[role=\'dialog\'] ul')
                qtyFollowers = len(followingList.find_elements_by_css_selector('li'))

                followingList.click()
                actionChain = webdriver.ActionChains(self.driver)

                while (qtyFollowers < 20):
                    time.sleep(2)
                    followersZone = self.driver.find_element_by_class_name("isgrP")
                    followersZone.click()
                    actionChain.key_down(Keys.ARROW_DOWN).perform()
                    actionChain.key_up(Keys.ARROW_DOWN).perform()
                    qtyFollowers = len(followingList.find_elements_by_css_selector('li'))

                for user in followingList.find_elements_by_css_selector('li'):

                    userLink = user.find_element_by_css_selector('a').get_attribute('href')
                    print(userLink)
                    followList.append(userLink)
            else:
                break


        return followList


    def follow(self, followList):
        driver = self.driver
        unfollowList= []
        for follower in followList:
            driver.get(follower)
            time.sleep(5)
            try:
                followButton = driver.find_element_by_css_selector('button')
                if (followButton.text == 'Follow') or (followButton.text == 'Obserwuj'):
                    followButton.click()
                    unfollowList.append(follower)
                    time.sleep(3)
                else:
                    print("You are already following user", follower)
            except Exception as e:
                time.sleep(2)
                print('Error')
                continue
        return unfollowList

bot=InstagramBot('username','password')

kontaUS=['instagram', 'asaprocky', 'therock', 'camerondallas', 'champagnepapi', 'mileycyrus', 'peggygou_',
         'stephencurry30', 'maddieziegler', 'dior', 'kingjames']

bot.login()

followList = bot.followList(kontaUS, 100)
unfollowList = bot.follow(followList)
filename = r"C:\Users\Kajet\PycharmProjects\testPyCharm\UnfollowLists\unfollowListGit.txt"
if os.path.getsize(filename) > 0:
    with open(filename, 'rb') as fp:
        pickleList = pickle.load(fp)
    unfollowList = pickleList + unfollowList

with open(filename, 'wb') as fp:
    pickle.dump(unfollowList, fp)

bot.closeBrowser()

