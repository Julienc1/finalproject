Final Project README- Julien Childress

TABLE OF CONTENTS:
1. Option Chosen
2. What does this program do?
3. How do you run this program?
4. What is this program dependent upon to run? 
5. What files are included in this project submission and what files are created when this program is run?
6. Function Descriptions
7. Class Descriptions
8. Database Creation
9. Data Manipulation Code
10. Project Reasoning
11. Line Numbers













1. Option 2

2. My project takes in any list of movie titles found in the code and simultaneously looks up Tweets related to the movie titles, as well as gathering information of all the users involved in the tweets themselves. This information is then filled into one of the three appropriate data tables utilizing SQLite. Finally, I have created code to output both the most common letter in all the usernames from the tweets and its number of occurrences, as well as the most common number found in usernames that contain numbers.


3. You run this program by opening terminal and going to the appropriate file folder will the finalproject.py is contained. Then, you run the program by typing in “python finalproject.py”.


4. To run this file, you should have tweepy, and sqlite3 downloaded with pip and you should also have a file in your finalproject.py folder with your appropriate twitter information. My file is called twitter_info.py.


5. The files included are as follows:
	1. finalproject.py: This file is the main file and allows the program to run.
	2. 206finalproject_caching.json: This is the json file that collects and caches the information  from making requests to both the Twitter and OMDB databases.
	3. finalproject.db: This is the database file that includes the three tables, Tweets, Users, and Movies. These three tables include many bits of information from Twitter and OMDB.
	4. README.txt: This file that explains the project.
	5. An output file called "output.txt" that gives some information on the movie_titles and output presented in the code.


6. Functions
	1. get_tweet_data
		1. Required: Takes in an input each of the movie titles to look up relevant tweets on Twitter
		2. No optional parameters
		3. I returns a list of  dictionary objects of all the tweets found with the movie title given as input.
		4. This function will cache new data if it has not been seen before and if the movie title has been searched previously, it will grab the relevant data from the 			cache file.
	2. get_movie_titles
		1. Required: This takes in the relevant movie title.
		2. No optional parameters
		3. It returns a list of all the movie titles that the tweets are associated with. I created this function to more easily fill in the Movies database later on. 
		4. No other behaviors
	3. get_user_info
		1. Required: takes in a particular twitter handle of a user on Twitter.
		2. No optional parameters
		3. It returns a list of relevant dictionaries of all the users’ Twitter information. This function is necessary when filling out the Users table for the database.
		4. This function will cache new data if it has not been seen before and if the movie title has been searched previously, it will grab the relevant data from the 			cache file.
	4. get_movie_info
		1. Required: takes in an appropriate movie title to search on the OMDB database using its API.
		2. No optional Parameters
		3. Returns a dictionary for a particular movie filled with information about the movie from the OMDB database.
		4. This function will cache new data if it has not been seen before and if the movie title has been searched previously, it will grab the relevant data from the cache file.

7. Classes
	1. Movie
		1. One instance of this class will represent a single movie that is on the OMDB database.
		2. The Movie Class will take in a dictionary representing a single movie as a constructor.
		3. Methods:
			1. __str__
				1. no other input besides self.
				2. This function does not change or add instance variables, just displays a few of them.
				3. Returns a string that says the movies’ imdb rating, primary language, and plot.
			2. find_num_directors
				1. no other input besides self.
				2. This function just displays how many directors there are based on the self.director list 
				3. returns the number of directors that created the particular movie.
	2. Tweet
		1. One instance of the class will represent an individual Tweet based on the movie title submitted as input.
		2. This class accepts a dictionary as input that has information about a Tweet. The dictionary then builds the tweet instance so data can be pulled later on 	easily.
		3. No Methods included

8. Database Creation
	The Database created includes 3 tables: Tweets, Users, and Movies.
	1. Tweets:
	-tweet_id (primary key) : Unique ID associated with Tweet
	-tweet_text: Actual text of the tweet
	-user_id : Unique ID of user who tweeted the tweet, references Users table
	-movie_title1: references from Movie table the title of the movie represented by tweet
	-num_favs1: number of favorites the tweet received
	-retweets: the number of retweets the tweet received
	2. Users:
	-user_id (primary key): Unique ID of user who tweeted the tweet
	-screen_name: Screen name of user who posted Tweet
	-num_favs: Number of favorites User has gotten
	-description: Description the user has created for themselves on Twitter
	3. Movies:
	-movie_id (primary key): unique ID given to particular movie on IMDB
	-movie_title: Title of the movie
	-director: names of the directors for the movie
	-num_languages: number of languages the movie is in
	-rating: rating given to the movie on IMDB
	-top_actor: The top-billed actor of the movie
	-release_date: Date the movie was released
9. Data Manipulation Code
	1. I have created code to output both the most common letter in all the usernames from the tweets and its number of occurrences, as well as the most common number found in usernames that contain numbers.
	2. This is useful and neat because it can show the user of the program what numbers and characters are most prevalent in usernames who tweet about particular movies. It is something interesting to see!
	3. It will show you the most common character and its number of occurrences as well as the most common number found in usernames.
	4. It is outputted in a text-friendly way in the terminal window when the program is run.
10. Reasoning
	I chose to do this project based on the fact that we were given options to complete the final project in my SI 206 class. This option looked interesting to me and I felt capable of completing all the tasks required. It also allowed me to do a unique data manipulation process at the end with the different methods we have learned such as filtering and list comprehension.

11. Specific things to note for SI 206 -- ok to put this in a section -- copy this right into a .txt file and fill in the correct line numbers
Line(s) on which each of your data gathering functions begin(s): 57, 87, 102, 134
Line(s) on which your class definition(s) begin(s): 170, 189
Line(s) where your database is created in the program: 279
Line(s) of code that load data into your database: 368, 419, 471
Line(s) of code (approx) where your data processing code occurs — where in the file can we see all the processing techniques you used?: 479-514, 528, 557
Line(s) of code that generate the output. : 598, 601
OK to be approximate here — ok if it ends up off by 1 or 2. Make it easy for us to find!
	

Nothing else to report for the project!
