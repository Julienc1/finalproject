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
#print(shrek_info)





##Define a class Movie that accepts a dictionary as the constructor that represents an individual movie.
##It should have at least three instance variables and two methods. You must have this information either as instance variables or methods:
##Title, director, IMDB rating, list of actors, number of languages, and anything else interesting..
class Movie():
	def __init__(self, movie_dict ={}):
		self.title = movie_dict["Title"]
		self.director = movie_dict["Director"]
		self.rating = movie_dict["imdbRating"]
		self.language = movie_dict["Language"]
		self.actors = movie_dict["Actors"]
		self.plot = movie_dict["Plot"]
		self.id = movie_dict["imdbID"]
		self.release_date = movie_dict["Released"]

	def __str__(self):
		return "This movie has an imdb rating of {}, the primary language of the movie is {}, and the plot is: {}".format(self.rating, self.language, self.plot)

	def find_num_directors(self):
		return len(self.director)





##Create a list of the three movie names you wil search for on Twitter. Put these three movie names into the list movie_titles
movie_titles = ["Shrek", "Airplane", "21 Jump Street"]




##Now create a list of dictionaries of the tweets you will recieve back from looking up the movies
tweet_dictionary_list = []
for movie in movie_titles:
	tweet_dictionary_list.append(get_tweet_data(movie))

print(tweet_dictionary_list)










##Now, compile a list of three movie titles to use for your OMDB function. Compile these titles as strings for the list called movies_list.
movies_list = ["Shrek", "Airplane", "21 Jump Street"]


##Make a request to OMDB with each of the movie titles and compile the dictionaries you get back into a list called movie_dict_list. 

movie_dict_list = []
for movie in movies_list:
	movie_dict_list.append(get_movie_info(movie))
#print(movie_dict_list)

##With this list of dictionaries, create a list of Movie insatnces utilizing the Movie class.
movie_instances = []
for movie in movie_dict_list:
	movie_instances.append(Movie(movie))
#print(movie_instances[1])




##With your Twitter search function, look up the three titles of the movies you have chosen. Utilize your Twitter class to make this easier. Save your tweet instances in a list named tweet_list



##Then, with every Twitter user in the "neighborhood" of the above Tweets(tweet posters and users mentioned), compile a list of dictionaries for each user instance.







# You will be creating a database file: finalproject.db

conn = sqlite3.connect('finalproject.db')
cur = conn.cursor()


statement = 'DROP TABLE IF EXISTS Tweets'
cur.execute(statement)
statement = 'DROP TABLE IF EXISTS Users'
cur.execute(statement)
statement = 'DROP TABLE IF EXISTS Movies'
cur.execute(statement)




##Create a database file called Tweets and include:
#-tweet_id (primary key)
#-tweet_text
#-user_id
#-movie_id
#-num_favorites
#-num_retweets
statement = 'CREATE TABLE IF NOT EXISTS Tweets (tweet_id TEXT PRIMARY KEY, tweet_text TEXT, user_id REFERENCES Users(user_id), movie_id REFERENCES Movie(movie_id), num_favs INTEGER retweets INTEGER)'
cur.execute(statement)




##Create a database file called Users and include:
#-user_id (primary key)
#-screen_name
#-num_favourites
#-description
statement = 'CREATE TABLE IF NOT EXISTS Users (user_id TEXT PRIMARY KEY, screen_name TEXT, num_favs INTEGER, description TEXT)'
cur.execute(statement)



##Create a database file called Movies and include:
#-movie_id (primary key)
#-movie_title
#-director
#-languages
#-rating
#-top_actor
#-rated
#-released
statement = 'CREATE TABLE IF NOT EXISTS Movies (movie_id TEXT PRIMARY KEY, movie_title TEXT, director TEXT, num_languages INTEGER, imdb_rating TEXT, top_actor TEXT, release_date TEXT)'
cur.execute(statement)




mentions = []
for tweet1 in tweet_dictionary_list:
	for tweet in tweet1:
		mentions.append(tweet["user"]["screen_name"])
for tweet1 in tweet_dictionary_list:
	for tweet in tweet1:

		entities = tweet["entities"]["user_mentions"]
		for user_mention in entities:
			mentions.append(user_mention["screen_name"])

user_id = []
screen_name = []
num_favs = []
description = []


for person in mentions:
	user_information= get_user_info(person)
	for info in user_information:
		user_id.append(info["user"]["id_str"])
		screen_name.append(info["user"]["screen_name"])
		num_favs.append(info["user"]["favourites_count"])
		description.append(info["user"]["description"])

users_table_info = zip(user_id, screen_name, num_favs, description)

statement = 'INSERT OR IGNORE INTO USERS VALUES (?, ?, ?, ?)'
for user in users_table_info:
	cur.execute(statement, user)
conn.commit()






movie_id = []
movie_title = []
director = []
num_languages2 = []
num_languages = []
imdb_rating = []
actors = []
top_actor = []
release_date = []

for movie in movie_instances:
	movie_id.append(movie.id)
for movie in movie_instances:
	movie_title.append(movie.title)
for movie in movie_instances:
	director.append(movie.director)
for movie in movie_instances:
	num_languages2.append(movie.language)
num_languages1 = [languages.split(" ") for languages in num_languages2]
for language in num_languages1:
	num_languages.append(len(language))
for movie in movie_instances:
	imdb_rating.append(movie.rating)
for movie in movie_instances:
	actors.append(movie.actors)
top_actor1 = [x.split(',') for x in actors if x]
#print(top_actor1)
for actor in top_actor1:
	top_actor.append(actor[0])
for movie in movie_instances:
	release_date.append(movie.release_date)


movie_table_info = zip(movie_id, movie_title, director, num_languages, imdb_rating, top_actor, release_date)

statement = 'INSERT OR IGNORE INTO Movies VALUES (?, ?, ?, ?, ?, ?, ?)'
for movie in movie_table_info:
	cur.execute(statement, movie)
conn.commit()























### IMPORTANT: CLOSE YOUR DATABASE CONNECTION!
conn.close()



# Put your tests here, with any edits you now need from when you turned them in with your project plan.


# Remember to invoke your tests so they will run! (Recommend using the verbosity=2 argument.)