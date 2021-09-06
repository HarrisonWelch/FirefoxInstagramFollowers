from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import html_to_json
import os
import re
import json

class FirefoxInstagramFollowers:

    DIR_LOGIN = 'login'
    FILE_LOGIN = 'login.json'
    DIR_TMP = 'tmp'
    FILE_TMP_FOLLOWER = 'tmp_follower.txt'
    FILE_TMP_FOLLOWING = 'tmp_following.txt'
    email = None
    username = None
    password = None
    browser = None
    following_accounts = None
    follower_accounts = None
    accts = {}
    loginSet = False

    def __init__(self) -> None:
        self.createDirectories()
        self.createFiles()
        self.loginSet = self.readLoginJSON()
        if not self.loginSet:
            raise Exception('The file was not found or your login information was incomplete. Try running install.py and place in your login information into it.')

    def readLoginJSON(self):
        # Open the file
        try:
            f = open(self.DIR_LOGIN + self.getFilepathDelimiter() + self.FILE_LOGIN)
        except FileNotFoundError as fnfe:
            print("The file " + str(self.DIR_LOGIN) + self.getFilepathDelimiter() + str(self.FILE_LOGIN) + " does not exit. Try running install.py.")

            # Leave function if exception thrown
            return False

        # Read and make JSON
        login = json.loads(f.read())

        # Pull info from JSON and put into object fields
        self.email = login["email"]
        self.username = login["username"]
        self.password = login["password"]

        if self.email == '' or self.username == '' or self.password == '':
            return False

        # Guard, close the file
        if f:
            f.close()

        return True
    
    def createDirectories(self):
        # If the the login folder does not yet exist, make it exist.
        if not os.path.exists(self.DIR_LOGIN):
            os.mkdir(self.DIR_LOGIN)
        # If the the tmp folder does not yet exist, make it exist.
        if not os.path.exists(self.DIR_TMP):
            os.mkdir(self.DIR_TMP)

    def createFiles(self):
        f = open(self.DIR_TMP + self.getFilepathDelimiter() + self.FILE_TMP_FOLLOWER, 'w+')
        f.close()
        f = open(self.DIR_TMP + self.getFilepathDelimiter() + self.FILE_TMP_FOLLOWING, 'w+')
        f.close()

    def openBrowser(self):
        if not self.loginSet:
            # Log issue
            print("Problem with login information")
            return
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(5)
        self.browser.get('https://www.instagram.com/')
    
    def close(self):
        if self.browser:
            self.browser.close()

    def execute(self):
        self.createDirectories()
        self.createFiles()
        self.readLoginJSON()
        if not self.loginSet:
            # Log issue
            print("Problem with login information")
            return
        self.openBrowser()
        sleep(3)
        self.loginToInstagram()
        sleep(3)
        self.goToInstagramAccount()
        sleep(3)
        self.getFollowingList()
        sleep(3)
        self.getFollowerList()
        sleep(3)
        self.parseAccounts()
        self.print()

    def loginToInstagram(self):
        if not self.loginSet:
            # Log issue
            print("Problem with login information")
            return
        username_input = self.browser.find_element_by_css_selector("input[name='username']")
        password_input = self.browser.find_element_by_css_selector("input[name='password']")
        username_input.send_keys(self.username)
        password_input.send_keys(self.password)
        login_button = self.browser.find_element_by_xpath("//button[@type='submit']")
        login_button.click()

    def goToInstagramAccount(self):
        if not self.loginSet:
            # Log issue
            print("Problem with login information")
            return
        try:
            avatar_button = self.browser.find_element_by_xpath('//*[@alt="'+str(self.username)+'\'s profile picture"]')
            avatar_button.click()
            print('Clicked "Avatar" Button')
        except NoSuchElementException as nsee:
            print('Didn\'t find the Avatar Button.')

        try:
            profile_menu_option = self.browser.find_element_by_xpath('//a[@href="/'+str(self.username)+'/"]')
            profile_menu_option.click()
            print('Clicked "Profile menu option" Button')
        except NoSuchElementException as nsee:
            print('Didn\'t find the "Profile menu option" Button.')

    def openFollowingListFromProfile(self):
        if not self.loginSet:
            # Log issue
            print("Problem with login information")
            return
        try:
            following_button = self.browser.find_element_by_xpath('//a[@href="/'+str(self.username)+'/following/"]')
            following_button.click()
            print('Clicked "Following" Button')
        except NoSuchElementException as nsee:
            print('Didn\'t find the Following Button.')
        sleep(2)
    
    def openFollowerListFromProfile(self):
        if not self.loginSet:
            # Log issue
            print("Problem with login information")
            return
        try:
            followers_button = self.browser.find_element_by_xpath('//a[@href="/'+str(self.username)+'/followers/"]')
            followers_button.click()
            print('Clicked "Followers" Button')
        except NoSuchElementException as nsee:
            print('Didn\'t find the "Followers" Button.')
        sleep(2)
    
    def closeFollowingOrFollowerView(self):
        try:
            close_button = self.browser.find_element_by_xpath('//*[@aria-label="Close"]')
            close_button.click()
            print('Clicked Close Button')
        except NoSuchElementException as nsee:
            print('Didn\'t find the Close Button.')
        sleep(2)
    
    ######################
    # GET FOLLOWING LIST #
    ######################
    def getFollowingList(self):
        if not self.loginSet:
            # Log issue
            print("Problem with login information")
            return
        self.openFollowingListFromProfile()
        try:
            # Aquire the HTML object for the following users
            following_list = self.browser.find_element_by_xpath('//*[@class="isgrP"]')

            # Get length of the list
            len_fl = len(following_list.get_attribute('innerHTML'))

            # Save an old verison for comparison later
            old_len_fl = len_fl
            print(str(len_fl))
            
            # Scroll the list down
            following_list.send_keys(Keys.END)
            sleep(2)

            # Length of the list again
            len_fl = len(following_list.get_attribute('innerHTML'))

            # Loop to get to the bottom
            while old_len_fl != len_fl:
                # Log that app needs to scroll
                print('Not yet at the bottom, scrolling...')

                # Adjust the old length before changing the new one
                old_len_fl = len_fl

                # Scroll
                following_list.send_keys(Keys.END)

                # Wait for it to get to the end
                sleep(2)

                # Get new length
                len_fl = len(following_list.get_attribute('innerHTML'))

            print('Scrolled to bottom')
        except NoSuchElementException as nsee:
            print('Didn\'t find the Following List.')
        
        following_list_inner = str(self.browser.find_element_by_xpath('//*[@class="PZuss"]').get_attribute('innerHTML'))
        # print(following_list_inner)
        self.closeFollowingOrFollowerView()

        f = open(self.DIR_TMP + self.getFilepathDelimiter() + self.FILE_TMP_FOLLOWING, 'w', encoding="utf-8")
            
        f.write(str(following_list_inner) + '\n')
        f.close()
    
    def parseFollowingAccountsDict(self):
        if not self.loginSet:
            # Log issue
            print("Problem with login information")
            return
        f = open(self.DIR_TMP + self.getFilepathDelimiter() + self.FILE_TMP_FOLLOWING, encoding="utf-8")
        following_json = html_to_json.convert(f.read())
        f.close()

        self.following_accounts = []
        for li2 in following_json['li']:
            # print('li2 = ' + str(li2))
            try:
                insta_at = li2['div'][0]['div'][0]['div'][1]['div'][0]['span'][0]['a'][0]['_value']
            except KeyError as ke:
                # print('KeyError found')
                insta_at = ''
            try:
                name = li2['div'][0]['div'][0]['div'][1]['div'][1]['_value']
            except KeyError as ke:
                # print('KeyError found')
                name = ''
            # x = x['div']

            self.following_accounts.append((insta_at, name))
        return

    #####################
    # GET FOLLOWER LIST #
    #####################
    def getFollowerList(self):
        if not self.loginSet:
            # Log issue
            print("Problem with login information")
            return
        self.openFollowerListFromProfile()
        try:
            follower_list = self.browser.find_element_by_xpath('//*[@class="isgrP"]')

            len_fl = len(follower_list.get_attribute('innerHTML'))
            
            old_len_fl = len_fl
            
            follower_list.send_keys(Keys.END)
            sleep(2)

            len_fl = len(follower_list.get_attribute('innerHTML'))

            while old_len_fl != len_fl:

                print('Not yet at the bottom, scrolling...')
                old_len_fl = len_fl

                follower_list.send_keys(Keys.END)
                
                sleep(2)

                len_fl = len(follower_list.get_attribute('innerHTML'))
            print('Scrolled to bottom')
        except NoSuchElementException as nsee:
            print('Didn\'t find the follower List.')
        
        follower_list_inner = str(self.browser.find_element_by_xpath('//*[@class="PZuss"]').get_attribute('innerHTML'))
        self.closeFollowingOrFollowerView()

        # Open follower html
        f = open(self.DIR_TMP + self.getFilepathDelimiter() + self.FILE_TMP_FOLLOWER, 'w', encoding="utf-8")

        f.write(str(follower_list_inner) + '\n')
        f.close()

    def parseFollowerAccountsDict(self):
        if not self.loginSet:
            # Log issue
            print("Problem with login information")
            return
        f = open(self.DIR_TMP + self.getFilepathDelimiter() + self.FILE_TMP_FOLLOWER, encoding="utf-8")
        follower_json = html_to_json.convert(f.read())
        f.close()

        self.follower_accounts = []
        for li2 in follower_json['li']:
            # print('li2 = ' + str(li2))
            try:
                insta_at = li2['div'][0]['div'][0]['div'][1]['div'][0]['span'][0]['a'][0]['_value']
            except KeyError as ke:
                # print('KeyError found')
                insta_at = ''
            try:
                name = li2['div'][0]['div'][0]['div'][1]['div'][1]['_value']
            except KeyError as ke:
                # print('KeyError found')
                name = ''
            # x = x['div']

            self.follower_accounts.append((insta_at, name))
        return
    
    def parseAccounts(self):
        if not self.loginSet:
            # Log issue
            print("Problem with login information")
            return
        self.parseFollowingAccountsDict()
        self.parseFollowerAccountsDict()
        accts = {}
        for acct in self.follower_accounts:
            accts.update({
                str(acct[0]):{
                    "name": acct[1], 
                    "follower": 'YES', 
                    "following": 'NO'
                    }
                })

        for acct in self.following_accounts:
            if acct[0] in accts:
                accts.update({
                    str(acct[0]):{
                        "name": acct[1], 
                        "follower": 'YES', 
                        "following": 'YES'
                        }
                    })
            else:
                accts.update({
                    str(acct[0]):{
                        "name": acct[1], 
                        "follower": 'NO', 
                        "following": 'YES'
                        }
                    })
        
        self.accts = accts
    
    def clickCloseButton(self):
        if not self.loginSet:
            # Log issue
            print("Problem with login information")
            return
        # Click the close button
        try:
            close_button = self.browser.find_element_by_xpath('//*[@aria-label="Close"]')
            close_button.click()
            print('Clicked Close Button')
        except NoSuchElementException as nsee:
            print('Didn\'t find the Close Button.')
    
    def print(self):
        if not self.loginSet:
            # Log issue
            print("Problem with login information")
            return
        REGEX_ONLY_ALNUM = r'[^a-zA-Z0-9]'
                
        print("+{:27s}+{:32s}+{:12s}+{:12s}+".format('-'*27,'-'*32,'-'*12,'-'*12))
        print("| {:<25s} | {:<30s} | {:^10s} | {:^10s} |".format('Account', 'Name', 'Follower', 'Following'))
        print("+{:27s}+{:32s}+{:12s}+{:12s}+".format('-'*27,'-'*32,'-'*12,'-'*12))
        for i in list(self.accts):
            # print(str(accts[i]["name"]))
            print("| {:<25s} | {:<30s} | {:^10s} | {:^10s} |".format(
                str(re.sub(REGEX_ONLY_ALNUM, '', str(i))),
                str(re.sub(REGEX_ONLY_ALNUM, '', str(self.accts[i]["name"]))),
                str(self.accts[i]["follower"]),
                str(self.accts[i]["following"])))
        print("+{:27s}+{:32s}+{:12s}+{:12s}+".format('-'*27,'-'*32,'-'*12,'-'*12))

    def getFilepathDelimiter(self):
        if os.name == 'nt':
            return "\\"
        else:
            return "/"

