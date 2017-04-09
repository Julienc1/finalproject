## Your name: Julien Childress
## The option you've chosen: Option 2

# Put import statements you expect to need here!
import unittest
import itertools
import collections
from collections import Counter
from collections import defaultdict
import tweepy
import twitter_info 
import json
import sqlite3
















# Write your test cases here.
print("\n\nBELOW THIS LINE IS OUTPUT FROM TESTS:\n")

class TestCache(unittest.TestCase):
	def test_omdb_caching(self):
		file1 = open("finalprojectmovie.json","r").read()
		self.assertTrue("movie_" in file1)
	def test_twitter_caching(self):
		file1 = open("finalprojecttweet.json","r").read()
		self.assertTrue("tweet_" in file1)


class Task2(unittest.TestCase):
	def test_users_1(self):
		conn = sqlite3.connect('finalproject_tweets.db')
		cur = conn.cursor()
		cur.execute('SELECT * FROM Users');
		result = cur.fetchall()
		self.assertTrue(len(result)>=10, "Testing to see if there are at least 10 records in the Users database")
		conn.close()
	def test_tweets_1(self):
		conn = sqlite3.connect('finalproject_tweets.db')
		cur = conn.cursor()
		cur.execute('SELECT * FROM Tweets');
		result = cur.fetchall()
		self.assertTrue(len(result)>=20, "Testing to see if there are at least 20 records in the Tweets database")
		conn.close()
	def test_movies_1(self):
		conn = sqlite3.connect('finalproject_tweets.db')
		cur = conn.cursor()
		cur.execute('SELECT * FROM Movies');
		result = cur.fetchall()
		self.assertTrue(len(result)=3, "Testing to see if there are 3 movies in the Database")
		conn.close()

	def test_movies_1(self):
		conn = sqlite3.connect('finalproject_tweets.db')
		cur = conn.cursor()
		cur.execute('SELECT tweet_text FROM Tweets WHERE num_favorites > 5');
		tweet_text1 = cur.fetchall()
		tweet_text = [" ".join(x) for x in result1]
		self.assertEqual(type(result), type([]), "Testing to see if result is a list of strings")
		self.assertEqual(type(result[0]), type(""), "Testing to see if result[0] is a string")
		conn.close()

class TestOMDB(unittest.TestCase):
	def test_omdb_search(self):
		self.assertEqual(type(omdb_list), type([]), "Testing to see if omdb_list is a list of strings")
		self.assertEqual(type(omdb_list[0]), type(""), "Testing to see if omdb_list[0] is a string")


class TestSummary(unittest.TestCase):
	def test_summary_file(self):
		file1 = open("summary.txt","r")
		s = file1.read()
		file1.close()
		self.assertEqual(type(s),type(""),"Doesn't look like there is a summary file with the right name or content in it")






if __name__ == "__main__":
	unittest.main(verbosity=2)

## Remember to invoke all your tests...