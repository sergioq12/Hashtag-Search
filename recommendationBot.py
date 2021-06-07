from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from time import sleep

PATH = "/Users/sergioquijano/chromedriver" # the path of the driver

#options = Options()
#options.add_argument("--haedless")
#options.binary_location = '/Applications/Google\ Chrome\   Canary.app/Contents/MacOS/Google\ Chrome\ Canary'

# Global Variables
instagram_hashtags_url = 'https://www.instagram.com/explore/tags'


number_of_posts_by_comment = 0

class RecommendationBot():
    def __init__(self, hashtag_to_search):
        self.hashtag_to_search = hashtag_to_search[1:]
        self.hashtag_url = f"{instagram_hashtags_url}/{self.hashtag_to_search}"
        self.driver = webdriver.Chrome(PATH) # the other argument could be chrome_options=options.  
        sleep(1)
        self.driver.get(self.hashtag_url)    
        sleep(2)


    def getHashtagPageSource(self):
        '''
            This function is going to return the source code from this the hashtag page.
        '''
        page_source = self.driver.page_source
        return page_source

    def getTopPostsLinks(self):
        '''
            This function is going to get all the links for the top posts.
        '''
        sleep(2)
        try:
            posts = WebDriverWait(self.driver,10).until(EC.presence_of_all_elements_located((By.TAG_NAME,"a")))
            top_posts = []
            for i in range(9):
                top_posts.append(posts[i])
            
            top_posts_links = [post.get_attribute("href") for post in top_posts]
            return top_posts_links
        except:
            print("Getting Top Posts not working. Driver quitting...")
            self.driver.quit()

    def singleTPHashtag(self, url, hashtag_list) -> list:
        '''
            This function is going to enter into one top post with its url.
            Then it is going to scrape the hashtags. It is going to enter the hashtags in the
            current list of hashtags that we have and then update it and return it.

            It is going to take the hashtags in the captions if there are, or if not it is going 
            to search for a while in the comments. Because some times the user put the hashtags
            in the comments.
        '''
        self.driver.get(url)
        username = str
        hashtags_inPost = []

        # this is going to get the hashtag in the caption
        # if the caption has more than 10 hashtags it is not going to search in the comments
        try:
            hashtags_caption = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "C4VMK")))
            hashtags_caption = hashtags_caption.find_elements_by_tag_name("a") # get all the <a> elements of the div that has all the hashtags
            username = hashtags_caption[0].text
            if len(hashtags_caption) > 1:
                for hashtag in hashtags_caption:
                    hashtag = hashtag.text
                    if hashtag[0] == "#":
                        hashtags_inPost.append(hashtag)

                for hashtag in hashtags_inPost:
                    hashtag_list.append(hashtag)
            
        except:
            print("Getting single top post hashtag -Caption not working. Driver quitting...")
            self.driver.quit()
        
        # if there are more than 10 hashtags in the caption
        if len(hashtags_inPost) >= 10: 
            # return the list and not include the comments.
            return hashtag_list 

        # this part is going to get the hashtags on the comments 
        try:
            sleep(1)
            # we have to keep clicking that button until it is not there
            flag = True
            # we can set a counter that if it gets more than 10 clicks it passes to the next post.
            counter = 0
            comment_already_done = False
            while flag:
                try:
                    more_icon = WebDriverWait(self.driver,1).until(EC.presence_of_element_located((By.XPATH,"/html/body/div[1]/section/main/div/div[1]/article/div[3]/div[1]/ul/li/div/button")))
                    more_icon.click()
                    # If the post has a lot of comments this going to skip the post when it had to perform more
                    # than 10 clicks on the more icon (+)
                    if counter >= 10:
                        hashtag_count_before = len(hashtag_list)
                        hashtag_list = self.getHashtagFromComments(hashtag_list,username)
                        flag = False
                        #print("exiting the while loop. By Counts")
                        #if hashtag_count_before != len(hashtag_list):
                            # if new hashtags were entered, then the post was obtained from comments
                            #number_of_posts_by_comment += 1
                        comment_already_done = True
                    counter += 1
                except:
                    flag = False
                    #print("exiting the while loop.")

            
            # After clicking the more button, it will get the comment of the user and
            # it will take the comments.
            # this code down here is getting the information about the first comment. 
    
            '''
            ---
            Este codigo funciona para cuando se necesite coger el primer comentario.
            --- 
            hashtags_comment_ul = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "Mr508"))) # get the first comment which is going to be the comment from the user with the hashtags
            hashtag_comment_As = hashtags_comment_ul.find_elements_by_tag_name("a")
            if hashtag_comment_As[0].text == username:
                for hashtag in hashtag_comment_As:
                    hashtag = hashtag.text
                    if hashtag[0] == "#":
                        hashtag_list.append(hashtag)
            
            '''
            if comment_already_done == False:
                hashtag_list = self.getHashtagFromComments(hashtag_list,username)
            '''
            # -- Temporal -- We need to try to search the user in all the comments.
            hashtag_ulElement = WebDriverWait(self.driver,5).until(EC.presence_of_all_elements_located((By.CLASS_NAME,"Mr508")))
            # hasta aqui vamos bien, coge todos los comments
            for hashtag_element in hashtag_ulElement:
                hashtag_title = hashtag_element.find_element_by_tag_name("a")
                if hashtag_title.text == username:
                    # Perfecto, encuentra el comment que hizo el usuario.
                    hashtags_inComment = hashtag_element.find_elements_by_tag_name("a")
                    for hashtag in hashtags_inComment:
                        hashtag = hashtag.text
                        if hashtag[0] == "#":
                            # Corre sin problemas por ahora. Encuentra todos los hashtags del comment y los mete a la lista.
                            hashtag_list.append(hashtag)
            '''

        except:
            print("Getting single top post hashtag -Comment not working. Driver quitting...")
            self.driver.quit()
        
        return hashtag_list

    def getHashtagFromComments(self,hashtag_list,username):

         # -- Temporal -- We need to try to search the user in all the comments.
        hashtag_ulElement = WebDriverWait(self.driver,5).until(EC.presence_of_all_elements_located((By.CLASS_NAME,"Mr508")))
        # hasta aqui vamos bien, coge todos los comments
        for hashtag_element in hashtag_ulElement:
            hashtag_title = hashtag_element.find_element_by_tag_name("a")
            if hashtag_title.text == username:
                # Perfecto, encuentra el comment que hizo el usuario.
                hashtags_inComment = hashtag_element.find_elements_by_tag_name("a")
                for hashtag in hashtags_inComment:
                    hashtag = hashtag.text
                    if hashtag[0] == "#":
                        # Corre sin problemas por ahora. Encuentra todos los hashtags del comment y los mete a la lista.
                        hashtag_list.append(hashtag)
        return hashtag_list

    def botStatistics(self):
        '''
            This function is going to return the bot statistics.
        '''
        print(f"The number of posts that their hashtags have been obtained\nfrom comments is {number_of_posts_by_comment}")

    def quit(self):
        sleep(1)
        self.driver.quit()
