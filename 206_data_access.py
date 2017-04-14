###### INSTRUCTIONS ###### 

# An outline for preparing your final project assignment is in this file.

# Below, throughout this file, you should put comments that explain exactly what you should do for each step of your project. You should specify variable names and processes to use. For example, "Use dictionary accumulation with the list you just created to create a dictionary called tag_counts, where the keys represent tags on flickr photos and the values represent frequency of times those tags occur in the list."

# You can use second person ("You should...") or first person ("I will...") or whatever is comfortable for you, as long as you are clear about what should be done.

# Some parts of the code should already be filled in when you turn this in:
# - At least 1 function which gets and caches data from 1 of your data sources, and an invocation of each of those functions to show that they work 
# - Tests at the end of your file that accord with those instructions (will test that you completed those instructions correctly!)
# - Code that creates a database file and tables as your project plan explains, such that your program can be run over and over again without error and without duplicate rows in your tables.
# - At least enough code to load data into 1 of your dtabase tables (this should accord with your instructions/tests)

######### END INSTRUCTIONS #########

#Name: Julien Childress
#Section: Thursday 3-4 P.M.

# Put all import statements you need here.
import unittest
import itertools
import collections
from collections import Counter
from collections import defaultdict
import tweepy
import twitter_info 
import json
import sqlite3
import requests
import omdb
# Begin filling in instructions....

##### TWEEPY SETUP CODE:
consumer_key = twitter_info.consumer_key
consumer_secret = twitter_info.consumer_secret
access_token = twitter_info.access_token
access_token_secret = twitter_info.access_token_secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

CACHE_FNAME = '206finalproject_caching.json' # String for your file. We want the JSON file type, because that way, we can easily get the information into a Python dictionary!
try:
    cache_file = open(CACHE_FNAME, 'r') 
    cache_contents = cache_file.read() 
    CACHE_DICTION = json.loads(cache_contents) 
    cache_file.close() 
except:
    CACHE_DICTION = {}




## Define a function called get_user_tweets that gets Tweets based on a specific search term to do with the movies you will choose, and use caching.
def get_tweet_data(phrase):
        unique_identifier = "twitter_{}".format(phrase)
        if unique_identifier in CACHE_DICTION:
                 twitter_results = CACHE_DICTION[unique_identifier]
                 
                 
        else:
                 twitter_results = api.search(phrase)
                 CACHE_DICTION[unique_identifier] = twitter_results
                 f = open(CACHE_FNAME,'w')
                 f.write(json.dumps(CACHE_DICTION))
                 f.close()
        tweet_data = []
        for i in range(20):
        	for tweet in twitter_results["statuses"]:
        	
        		tweet_data.append(tweet)
        		
        return tweet_data

##Invoke the function(get_user_tweets) with the movie Shrek below to check if it works and save it in the variable shrek_tweets:

shrek_tweets = get_tweet_data("Shrek")
#print(shrek_tweets)


## Define a function called get_user_info that gets data from a particular Twitter user and caches the data.
def get_user_info(handle):
        unique_identifier = "twitter_{}".format(handle)
        if unique_identifier in CACHE_DICTION:
                 twitter_results = CACHE_DICTION[unique_identifier]
                 
                 
        else:
                 twitter_results = api.user_timeline(handle)
                 print(type(twitter_results))
                 CACHE_DICTION[unique_identifier] = twitter_results
                 f = open(CACHE_FNAME,'w')
                 f.write(json.dumps(CACHE_DICTION))
                 f.close()
                 
                 
               
        tweet_data = []
        for i in range(20):
        	for tweet in twitter_results:
        	
        		tweet_data.append(tweet)
        return tweet_data




##Invoke the function(get_user_info) below to check if it works:
umsi_tweets = get_user_info("umsi")
#print(umsi_tweets)



## Define a function called get_movie_info that gets, caches, and returns movie information based on a movie title search with the OMDB database.
def get_movie_info(movie_title):
	unique_identifier = "movie_{}".format(movie_title)
	if unique_identifier in CACHE_DICTION:
		movie_results = CACHE_DICTION[unique_identifier]
                 
                 
	else:
		base_url = "http://www.omdbapi.com/?t=" + str(movie_title)
		r = requests.get(base_url)
		print(r.url)
		movie_results = json.loads(r.text)

                 
		CACHE_DICTION[unique_identifier] = movie_results
		f = open(CACHE_FNAME,'w')
		f.write(json.dumps(CACHE_DICTION))
		f.close()

	return movie_results
                 
                 
               
       


##Now invoke get_movie_info to check if it gets the correct information back in the variable shrek_info:
shrek_info = get_movie_info("Shrek")
print(shrek_info)





##Define a class Movie that accepts a dictionary as the constructor that represents an individual movie.
##It should have at least three insatnce variables and two methods. You must have this information either as instance variables or methods:
##Title, director, IMDB rating, list of actors, number of languages, and anything else interesting..







##Define a class Tweet to handle the data I have recieved above from my functions. It should accept a dictionary representing a tweet 
##as the constructor. This class should allow me to fill in the Tweet database with the information I need.



##Now, compile a list of three movie titles to use for your OMDB function. Compile these titles as strings for the list.



##Make a request to OMDB with each of the movie titles and compile the dictionaries you get back into a list. 



##With this list of dictionaries, create a list of Movie insatnces utilizing the Movie class.




##With your Twitter search function, look up the three titles of the movies you have chosen. Utilize your Twitter class to make this easier. Save your tweet instances in a list named tweet_list



##Then, with every Twitter user in the "neighborhood" of the above Tweets(tweet posters and users mentioned), compile a list of dictionaries for each user instance.




##Create a database file called Tweets and include:
#-tweet_id (primary key)
#-tweet_text
#-user_id
#-movie_id
#-num_favorites
#-num_retweets





##Create a database file called Users and include:
#-user_id (primary key)
#-screen_name
#-num_favourites
#-description




##Create a database file called Movies and include:
#-movie_id (primary key)
#-movie_title
#-director
#-languages
#-rating
#-top_actor
#-rated
#-released
































# Put your tests here, with any edits you now need from when you turned them in with your project plan.


# Remember to invoke your tests so they will run! (Recommend using the verbosity=2 argument.)