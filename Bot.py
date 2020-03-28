from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep, strftime
from random import randint
import pandas as pd
import os, configparser, pywin32_system32, keyring, random 
from datetime import datetime

destFolder = os.path.dirname(os.path.abspath(__file__))
config = configparser.ConfigParser(interpolation = None)
config.read(destFolder + '\\config.ini')

class Bot(object):

    def __init__(self, hstg):
        self.hashtags = str(config['DEFAULT'][hstg]).replace(' ', '')
        self.hashtags = self.hashtags.split(',')
        self.hashtags = random.sample(self.hashtags, randint(5,10))
        self.user = str(config['DEFAULT']['user'])
        #self.password = str(config['DEFAULT']['password'])
        self.webdriver = webdriver.Chrome(executable_path=r'C:\Users\User\Desktop\or\wherever\you\choose\chromedriver.exe')

    def connection(self, pswd=None):
        
        if pswd is None:
            # keyring is going to get the credential needed from the windows credentials manager, if you want to use this you need to add the credential to the credentials manager of your computer.
            pswd = keyring.get_password("https://www.instagram.com/accounts/login/?source=auth_switcher",self.user) # introduce your Instagram username in the config file !
        
        wd = self.webdriver
        wd.get('https://www.instagram.com/accounts/login/?source=auth_switcher')
        wd.maximize_window()

        username = wd.find_element_by_name('username')
        password = wd.find_element_by_name('password')
        button_login = wd.find_element_by_xpath('/html/body/div[1]/section/main/div/article/div/div[1]/div/form/div[4]/button')

        username.send_keys(self.user)
        password.send_keys(pswd)
        button_login.click()
        wd.implicitly_wait(20)
        notnow = wd.find_element_by_xpath('/html/body/div[4]/div/div/div[3]/button[2]')
        notnow.click()                      # comment these last 2 lines out, if you don't get a pop up asking about notifications

    def launch(self, nb=7, option=None, hashtags=None):
        
        startTime = datetime.now()
        wd = self.webdriver
        self.connection()                   # add your password here if you're not using the credentials manager
        self.previous_users = []           # uncomment this line if it's the first time you use the bot   # comment this line once you already launched the bot once, and uncomment the following two lines 
        # self.previous_users = pd.read_csv(destFolder + '\\users_followed_list.csv', delimiter=',').iloc[:,1:2]     # useful to build a user log
        # self.previous_users = list(self.previous_users['0'])
        self.dict = {
            'new_followed_users': [],
            'followed': 0,
            'likes': 0,
            'comments': 0
        }
        if hashtags is None:
            hashtags = self.hashtags

        for i in range(0, len(hashtags)):
            wd.get('https://www.instagram.com/explore/tags/'+ hashtags[i] + '/')
            wd.implicitly_wait(10)
            firstline_thumbnail = wd.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div/div[1]/div['+ str(randint(1,3)) +']/a/div/div[2]')
            sleep(randint(2,5))
            try:
                firstline_thumbnail.click()
            except:
                wd.implicitly_wait(10)
                firstline_thumbnail = wd.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div/div[1]/div[1]/a/div/div[2]')
                firstline_thumbnail.click()

            for n in range(1, randint(nb-3,nb+3)):
                print(hashtags[i])
                print('n = ' + str(n))
                sleep(randint(2,4))
                try:
                    username = wd.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/header/div[2]/div[1]/div[1]/a').text
                except:
                    print('error with ' + str(n))
                    # wd.find_element_by_link_text('Siguiente').click()    # Next picture
                    wd.find_element_by_link_text('Next').click()    # Next picture
                    sleep(randint(3,5))
                    username = wd.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/header/div[2]/div[1]/div[1]/a').text
                
                print(username)

                if option == 'f' or option == None:

                    if username not in self.previous_users:     # If we already follow, do not unfollow
                        seguir = wd.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/header/div[2]/div[1]/div[2]/button')
                        prob = randint(1,1000)
                        if prob >= 900:
                            # if seguir.text == 'Seguir':
                            if seguir.text == 'Next':
                                seguir.click()
                                self.dict['new_followed_users'].append(username)
                                self.dict['followed'] += 1
                                print(self.dict['new_followed_users'])
                 
                if option == 'l' or option == None:                                     # Liking the picture
                    sleep(randint(3,6))
                    prob = randint(1,1000)

                    if prob <= 627:
                        button_like = wd.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/div[2]/section[1]/span[1]/button')
                        button_like.click()
                        self.dict['likes'] += 1
                        sleep(randint(1,4))

                # wd.find_element_by_link_text('Siguiente').click()    # Next picture
                wd.find_element_by_link_text('Next').click()    # Next picture
                sleep(randint(2,4))

        for x in range(0,len(self.dict['new_followed_users'])):
            self.previous_users.append(self.dict['new_followed_users'][x])

        updated_user_df = pd.DataFrame(self.previous_users)
        updated_user_df.to_csv(destFolder + '\\users_followed_list.csv')
        print('')
        print('Bot launched for around ' + str(nb) + ' hashtags.')
        print('Liked {} photos.'.format(self.dict['likes']))
        print('Followed {} new people.'.format(self.dict['followed']))

        print('Execution time : ' + str(datetime.now() - startTime).split('.')[0] + '.')
        print('Finished at : ' + str(datetime.now()).split('.')[0])


Bot('hashtags_popular_travel').launch(10)
Bot('hashtags_popular_travel').launch(8, 'l')
Bot('hashtags_popular_travel').launch(13, 'f')
