###### INSTRUCTIONS ###### 

# An outline for preparing your final project assignment is in this file.

# Below, throughout this file, you should put comments that explain exactly what you should do for each step of your project. You should specify variable names and processes to use. For example, "Use dictionary accumulation with the list you just created to create a dictionary called tag_counts, where the keys represent tags on flickr photos and the values represent frequency of times those tags occur in the list."

# You can use second person ("You should...") or first person ("I will...") or whatever is comfortable for you, as long as you are clear about what should be done.

# Some parts of the code should already be filled in when you turn this in:
# - At least 1 function which gets and caches data from 1 of your data sources, and an invocation of each of those functions to show that they work 
# - Tests at the end of your file that accord with those instructions (will test that you completed those instructions correctly!)
# - Code that creates a database file and tables as your project plan explains, such that your program can be run over and over again without error and without duplicate rows in your tables.
# - At least enough code to load data into 1 of your database tables (this should accord with your instructions/tests)

######### END INSTRUCTIONS #########

#Name: Julien Childress
#Section: Thursday 3-4 P.M.


##NOTE##

##Code utilized to cache my data has been inspired from previous assignments but altered to fit this assignment.
##All methods relating to databases and data manipulation has also been inspired from past assignments but has also been tweaked for this assignment.
##All the code present in this project is my own.

##END NOTE##


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
import datetime 
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




##Define a function to attain the movie titles from every tweet, so you can classify the tweet by movie title in your database later on.
def get_movie_titles(phrase):
	movie_titles_list = []
	twitter_results = api.search(phrase)
	for i in range(20):
		for tweet in twitter_results["statuses"]:
			movie_titles_list.append(phrase)
	return movie_titles_list

get_shrek_title = get_movie_titles("Shrek")
#print(get_shrek_title)




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
		#print(r.url)
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
		return len(self.director.split(","))

##Now define a class Tweet that accepts a dictionary as the constructor and where it represents an individual movie.
##The instance variables should include id, text, user_id, favorites, and retweets so you can fill in the Tweets table later on
class Tweet():
	
	def __init__(self, tweet_dict ={}):

		self.id = tweet_dict["id_str"]
		self.text = tweet_dict["text"]
		self.user_id = tweet_dict["user"]["id_str"]
		self.favs = tweet_dict["favorite_count"]
		self.retweets = tweet_dict["retweet_count"]



		






##Create a list of the three movie names you wil search for on Twitter. Put these three movie names into the list movie_titles
movie_titles = ["Shrek", "Braveheart", "21 Jump Street"]










##Now create a list of dictionaries of the tweets you will recieve back from looking up the movies
tweet_dictionary_list = []
tweet_movie_list = []
for movie in movie_titles:
	tweet_dictionary_list.append(get_tweet_data(movie))
	tweet_movie_list.append(get_movie_titles(movie))

#print(tweet_movie_list)




##With each Tweet dictionary you have in the list, make each of them an insatnce of class Tweet. Put all of these instances in a list, tweet_instances.
tweet_instances = []
for tweet1 in tweet_dictionary_list:
	for tweet in tweet1:
		tweet_instances.append(Tweet(tweet))








##Now, compile a list of three movie titles to use for your OMDB function. Compile these titles as strings for the list called movies_list.
movies_list = ["Shrek", "Braveheart", "21 Jump Street"]


##Make a request to OMDB with each of the movie titles and compile the dictionaries you get back into a list called movie_dict_list. 

movie_dict_list = []
for movie in movies_list:
	movie_dict_list.append(get_movie_info(movie))
#print(movie_dict_list)

##With this list of dictionaries, create a list of Movie instances utilizing the Movie class and call this lsit movie_instances.
movie_instances = []
for movie in movie_dict_list:
	movie_instances.append(Movie(movie))
#print(movie_instances[1])















# You will be creating a database file: finalproject.db
##Create, three tables, Tweets, Users, and Movies

conn = sqlite3.connect('finalproject.db')
cur = conn.cursor()


statement = 'DROP TABLE IF EXISTS Tweets'
cur.execute(statement)
statement = 'DROP TABLE IF EXISTS Users'
cur.execute(statement)
statement = 'DROP TABLE IF EXISTS Movies'
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


##Create a database file called Tweets and include:
#-tweet_id (primary key)
#-tweet_text
#-user_id
#-movie_id
#-num_favorites
#-num_retweets
statement = 'CREATE TABLE IF NOT EXISTS Tweets (tweet_id TEXT PRIMARY KEY, tweet_text TEXT, user_id REFERENCES Users(user_id), movie_title1 REFERENCES Movie(movie_title), num_favs1 INTEGER, retweets INTEGER)'
cur.execute(statement)







##For the users table, you must find all the neighborhood users from the tweets you have compiled, Compile all the neighborhood users in a list called mentions. 
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

##Now invoke the function get_user_info with each user in the mentions list. Attain the appropriate information to fill out the Users table for later
##Using the zip function, put the lists together and put that into the variable users_table_info
for person in mentions:
	user_information= get_user_info(person)
	for info in user_information:
		user_id.append(info["user"]["id_str"])
		screen_name.append(info["user"]["screen_name"])
		num_favs.append(info["user"]["favourites_count"])
		description.append(info["user"]["description"])




users_table_info = zip(user_id, screen_name, num_favs, description)


##Insert the information into the users table:
statement = 'INSERT OR IGNORE INTO USERS VALUES (?, ?, ?, ?)'
for user in users_table_info:
	cur.execute(statement, user)
conn.commit()





##With the list of tweet instances, fill in the lists required to fill out the Tweets table later. 
##Zip the lists together much like the Users table and put the data into the variable tweet_table_info


tweet_id = []
tweet_text = []
tweet_user_id = []
movie_title1 = []
num_favs1 = []
retweets = []





for tweet in tweet_instances:
	tweet_id.append(tweet.id)
for tweet in tweet_instances:
	tweet_text.append(tweet.text)
for tweet in tweet_instances:
	tweet_user_id.append(tweet.user_id)
for movie in tweet_movie_list:
	for movie1 in movie:
		movie_title1.append(movie1)
for tweet in tweet_instances:
	num_favs1.append(tweet.favs)
for tweet in tweet_instances:
	retweets.append(tweet.retweets)


#print(len(movie_title1))
#print(len(tweet_id))
#print(len(tweet_text))


tweet_table_info = zip(tweet_id, tweet_text, tweet_user_id, movie_title1, num_favs1, retweets)

#print(tweet_table_info)



##Load the required information into the Tweets table:
statement = 'INSERT OR IGNORE INTO Tweets VALUES (?, ?, ?, ?, ?, ?)'
for tweet in tweet_table_info:
	cur.execute(statement, tweet)
conn.commit()







##Do the same thing for the Movies table and zip the required information into the variable movie_table_info:




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
#print(type(movie_table_info))

statement = 'INSERT OR IGNORE INTO Movies VALUES (?, ?, ?, ?, ?, ?, ?)'
for movie in movie_table_info:
	cur.execute(statement, movie)
conn.commit()


##Now I am going to make queries to my database to find cool intersections of data!




query = 'SELECT * FROM Tweets WHERE num_favs1 > 1'
cur.execute(query)
more_than_2_favs = cur.fetchall()





query = 'SELECT * FROM Movies WHERE imdb_rating > 7 '
cur.execute(query)
high_imdb_rating = cur.fetchall()




query = 'SELECT description FROM Users WHERE num_favs > 15'
cur.execute(query)
descriptions_fav_users1 = cur.fetchall()
descriptions_fav_users = [" ".join(x) for x in descriptions_fav_users1]




query = 'SELECT screen_name, tweet_text FROM Tweets INNER JOIN Users on Tweets.user_id=Users.user_id WHERE Tweets.retweets > 5'
cur.execute(query)
user_and_text = cur.fetchall()


query = 'SELECT movie_title, retweets FROM Movies INNER JOIN Tweets'
cur.execute(query)
movies_tweeted = cur.fetchall()


query = 'SELECT screen_name, num_favs FROM Users'
cur.execute(query)
screen_names = cur.fetchall()

##Now you are going to find the most common number present in usernames of users who have a number included in their screen_name as well as the most common character overall found in the usernames you have collected.
##To make this work, use filters, list comprehensions and dictionary accumulation to achieve a final dictionary where the keys are the numbers 0-9
##and their values are the number of times they are seen throughout all the usernames.





twitter_info_diction2 = defaultdict(list)
for k, v in screen_names:
	twitter_info_diction2[k].append(v)
twitter_info_diction2 = dict(twitter_info_diction2)

#print(twitter_info_diction2)

user_name_count_list = []
for key in twitter_info_diction2:
	for letter in key:
		user_name_count_list.append(letter.upper())

c = Counter(user_name_count_list)
most_common_char1 = c.most_common(5)
#print(most_common_char1)
most_common_char2 = most_common_char1[3]



#3Find the most common character overall here:

for tup in most_common_char1:
	if tup[1] > most_common_char2[1]:
		most_common_char2 = tup
#print(most_common_char2)





##Below, use filtering to get only the usernames with numbers in them!


filter = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]

filter_set = set(filter)


many_favs_filter = [tup for tup in screen_names for item in filter if item in tup[0]]

many_favs_filter_list = list(many_favs_filter)


twitter_info_diction1 = defaultdict(list)
for k, v in many_favs_filter_list:
	twitter_info_diction1[k].append(v)
twitter_info_diction = dict(twitter_info_diction1)










most_common_num = {}

for tup in many_favs_filter:
	for number in filter:
		if number in tup[0]:
			if number not in most_common_num:
				most_common_num[number] = 0
			else: 
				most_common_num[number] += 1



final_most_common_number = max(most_common_num, key=most_common_num.get)




print("The most common character in a username is:  " + most_common_char2[0] + " and the number of times it occurred is: " + str(most_common_char2[1]))


print("The most common number found in usernames that include numbers is: " + str(final_most_common_number))





today = datetime.date.today()

output_txt = "output.txt"

f = open(output_txt, "w")

f.write('This is my summary output page:')
f.write('\n')
f.write('\n')
f.write('My three movie titles are:' + str(movie_titles))
f.write('\n')
f.write('\n')
f.write("I have looked up Tweets on Twitter that have these movie titles in their content.")
f.write('\n')
f.write('\n')
f.write('The current date is:')
f.write(str(today))
f.write('\n')
f.write('\n')
f.write("The most common character in a username is:  " + most_common_char2[0] + " and the number of times it occurred is: " + str(most_common_char2[1]))
f.write('\n')
f.write('\n')
f.write("The most common number found in usernames that include numbers is: " + str(final_most_common_number))











































### IMPORTANT: CLOSE YOUR DATABASE CONNECTION!
conn.close()



# Put your tests here, with any edits you now need from when you turned them in with your project plan.
print("\n\nBELOW THIS LINE IS OUTPUT FROM TESTS:\n")

class TestCache(unittest.TestCase):
	def test_omdb_caching(self):
		file1 = open("206finalproject_caching.json","r").read()
		self.assertTrue("movie_" in file1)

class Task2(unittest.TestCase):
	def test_users_1(self):
		conn = sqlite3.connect('finalproject.db')
		cur = conn.cursor()
		cur.execute('SELECT * FROM Users');
		result = cur.fetchall()
		self.assertTrue(len(result)>=10, "Testing to see if there are at least 10 records in the Users database")
		conn.close()
	def test_tweets_1(self):
		conn = sqlite3.connect('finalproject.db')
		cur = conn.cursor()
		cur.execute('SELECT * FROM Tweets');
		result = cur.fetchall()
		self.assertTrue(len(result)>=20, "Testing to see if there are at least 20 records in the Tweets database")
		conn.close()
	def test_tweets_2(self):
		conn = sqlite3.connect('finalproject.db')
		cur = conn.cursor()
		cur.execute('SELECT * FROM Tweets');
		result = cur.fetchall()
		self.assertTrue(len(result[1])==6,"Testing that there are 6 columns in the Tweets table")
		conn.close()
	def test_movies_1(self):
		conn = sqlite3.connect('finalproject.db')
		cur = conn.cursor()
		cur.execute('SELECT * FROM Movies');
		result = cur.fetchall()
		self.assertTrue(len(result)==3, "Testing to see if there are 3 movies in the Database")
		conn.close()


	def test_movies_1(self):
		conn = sqlite3.connect('finalproject.db')
		cur = conn.cursor()
		cur.execute('SELECT tweet_text FROM Tweets WHERE num_favs1 > 0');
		tweet_text1 = cur.fetchall()
		tweet_text = [" ".join(x) for x in tweet_text1]
		print(tweet_text)
		self.assertEqual(type(tweet_text), type([]), "Testing to see if tweet_text is a list of strings")
		self.assertEqual(type(tweet_text[0]), type(""), "Testing to see if it is a string")
		conn.close()

class TestOMDB(unittest.TestCase):
	def test_omdb_search(self):
		self.assertEqual(type(movie_titles), type([]), "Testing to see if omdb_list is a list of strings")
	def test_omdb_search_1(self):
		self.assertEqual(type(movie_titles[0]), type(""), "Testing to see if omdb_list[0] is a string")


class TestZipFiles(unittest.TestCase):
	def test_user_zip(self):
		list1 = ["2"]
		list2 = ["1"]
		list3 = ["3"]
		zip_var = zip(list1, list2, list3)

		self.assertEqual(type(users_table_info), type(zip_var), "Testing to see if users_table_info is of type zip")
	def test_tweet_zip(self):
		list1 = ["2"]
		list2 = ["1"]
		list3 = ["3"]
		zip_var = zip(list1, list2, list3)

		self.assertEqual(type(tweet_table_info), type(zip_var), "Testing to see if tweet_table_info is of type zip")
	def test_movies_zip(self):
		list1 = ["2"]
		list2 = ["1"]
		list3 = ["3"]
		zip_var = zip(list1, list2, list3)

		self.assertEqual(type(movie_table_info), type(zip_var), "Testing to see if movie_table_info is of type zip")

class TestMovieStr(unittest.TestCase):
	def test_str_method(self):
		shrek_info = get_movie_info("Shrek")
		ps = Movie(shrek_info)
		self.assertEqual(ps.__str__(), "This movie has an imdb rating of 7.9, the primary language of the movie is English, and the plot is: After his swamp is filled with magical creatures, Shrek agrees to rescue Princess Fiona for a villainous lord in order to get his land back.", "Testing to see if the number of directors for Shrek is 2")


class TestDirectors(unittest.TestCase):
	def test_str_method(self):
		shrek_info = get_movie_info("Shrek")
		ps = Movie(shrek_info)
		self.assertEqual(ps.find_num_directors(), 2, "Testing to see if number of directors is 2 for Shrek")


class TestMovieDictList(unittest.TestCase):
	def test_type(self):
		self.assertEqual(type(movie_dict_list), type([]), "Testing to see if movie_dict_list is of type list")
	def test_contents(self):
		self.assertEqual(type(movie_dict_list[0]), type({}), "Testing to see if contents of movie_dict_list are dictionaries")


class TestTweetInstances(unittest.TestCase):
	def test_type(self):
		self.assertEqual(type(tweet_instances), type([]), "Testing to see if tweet_instances is of type list")
	#def test_contents(self):
		#pa = get_tweet_data("Shrek")
		#ps = Tweet(pa)
		#self.assertEqual(type(tweet_instances[0]), pa, "Testing to see if contents of movie_dict_list are Tweet objects")

class TestGetUserInfo(unittest.TestCase):
	def test_type(self):
		self.assertEqual(type(umsi_tweets), type([]), "Testing to see if umsi_tweets is of type list")
		def test_contents(self):
			self.assertEqual(type(umsi_tweets[0]), type({}), "Testing to see if contents of umsi_tweets are dictionaries")


class TestGetTweetData(unittest.TestCase):
	def test_get_tweet_data(self):
		data1 = get_tweet_data("Shrek")
		self.assertEqual(type(data1),type(["Shrek",3]))

class TestGetMovieTitles(unittest.TestCase):
	def test_get_movie_titles(self):
		data1 = get_movie_titles("Shrek")
		self.assertEqual(type(data1),type(["Shrek",3]))
	def test_get_movie_titles1(self):
		data1 = get_movie_titles("Shrek")
		self.assertEqual(type(data1[0]),type("Shrek"))

class TestGetUserInfo(unittest.TestCase):
	def test_get_user_info(self):
		data1 = get_user_info("UMSI")
		self.assertEqual(type(data1),type(["Shrek",3]))
	def test_get_user_info1(self):
		self.assertEqual(type(umsi_tweets),type([]))
	def test_get_user_info2(self):
		self.assertEqual(type(umsi_tweets[5]),type({}))


class TestGetMovieInfo(unittest.TestCase):
	def test_get_movie_info(self):
		data1 = get_movie_info("Shrek")
		self.assertEqual(type(data1),type({}))
	def test_get_movie_info1(self):
		self.assertEqual(type(shrek_info),type({}))


class TestClassTweet(unittest.TestCase):
	def test_tweet(self):
		tweet_instances = []
		for tweet1 in tweet_dictionary_list:
			for tweet in tweet1:
				tweet_instances.append(Tweet(tweet))
		self.assertEqual(type(tweet_instances[0].text),type(""))





#class Test_Get_Movie_Titles(unittest.TestCase):
	#def test_function(self):
		#movie_titles = ["Shrek", "Braveheart", "21 Jump Street"]
		#tweet_movie_list = []
		#for movie in movie_titles:
			#tweet_movie_list.append(get_movie_titles(movie))
			#self.assertEqual(('Shrek' in tweet_movie_list), True)




#class TestSummary(unittest.TestCase):
	#def test_summary_file(self):
		#file1 = open("summary.txt","r")
		#s = file1.read()
		#file1.close()
		#self.assertEqual(type(s),type(""),"Doesn't look like there is a summary file with the right name or content in it")






if __name__ == "__main__":
	unittest.main(verbosity=2)

# Remember to invoke your tests so they will run! (Recommend using the verbosity=2 argument.)