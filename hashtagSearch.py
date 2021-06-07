from recommendationBot import RecommendationBot
import time
from collections import Counter

class HashtagSearcher(): 

    def __init__(self, hashtag) -> None:
        # Version 2.0 --> This version is better than before.
        # It saves time because it does not have to login.
        # However, same process after getting to the hashtag website.
        #if the hashtag is miswritten, the program closes
        if hashtag[0] != "#":
            print("That was not a hashtag.")
            quit()
        start = time.time()
        bot = RecommendationBot(hashtag)
        top_posts_links = bot.getTopPostsLinks() #done
        hashtags = self.getAllHashtags(bot,top_posts_links)
        bot.quit()
        impressions = self.getHashtagImpressions(hashtags)
        end = time.time()
        self.recommendations = self.initialRecomendation(impressions)
        
        print(f"The time that took to perform all actions was: {round(end - start,2)} seconds")
        
    def getRecommendedHashtags(self):

        return self.recommendations

    def getAllHashtags(self,bot,top_posts_links) -> list:
        '''
            This function is going to iterate through all the top posts with its
            links and it is going to get all the hashtags into one big list.
        '''
        hashtag_list = []

        for top_post in top_posts_links:
            hashtag_list = bot.singleTPHashtag(top_post,hashtag_list)
        return hashtag_list

    def getHashtagImpressions(self,hashtag_list):
        '''
            This function is going to take the hashtag list and it is going to 
            count each hashtag and organize it in a dictionary from the one with most
            impressions, to the ones with less. 
        '''
        impressions = Counter(hashtag_list)
    
        return impressions

    def initialRecomendation(self,impressions):
        '''
            This function is going to take the impressions dictionary as argument
            and it will give the 10 hashtags that had the most impressions inside the 
            impressions dictionary. 
        '''
        most_common_hashtags = impressions.most_common(10)
        index = 0
        hashtags_toRecommend = []
        initial_hashtag = most_common_hashtags[0][0]
        for common in most_common_hashtags:
            if index == 12:
                break
            if common[0] != initial_hashtag:
                hashtags_toRecommend.append(common[0])
        
            index += 1
        return hashtags_toRecommend
        print("These are the hashtags we recommend for your next post: \n")
        for hashtag in hashtags_toRecommend:
            print(f"{hashtag} ",end=",")
        print()

        query = input("Do you want to get the copy & paste version? ")
        if query.lower() == "yes" or query.lower()[0] == "y":
            print(f"{initial_hashtag}", end="")
            for hashtag in hashtags_toRecommend:
                print(f"{hashtag}",end="")
            print()

        


