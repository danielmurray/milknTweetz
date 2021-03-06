import re
import math
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import *

Base = declarative_base()
class Ham(Base):
	__tablename__ = 'ham'

	id = Column(Integer, primary_key=True)
	word = Column(String)
	count = Column(Integer)


class Spam(Base):
	__tablename__ = 'spam'

	id = Column(Integer, primary_key=True)
	word = Column(String)
	count = Column(Integer)

class Beta():

	def __init__(self, db , tweet_text ):
		self.session = db
		self.laplace_k = 1
		self.tweet = self.format_tweet(tweet_text)
		self.total_ham_count = self.session.query(func.sum(Ham.count)).scalar()
		self.total_spam_count = self.session.query(func.sum(Spam.count)).scalar()
		self.total_count = self.total_ham_count + self.total_spam_count
		self.ham_chance = self.total_ham_count/self.total_count
		self.spam_chance = self.total_spam_count/self.total_count
		self.words = []
		self.score = 0
		for word in self.tweet:
			ham_count = self.get_word_count(word, Ham)
			spam_count = self.get_word_count(word, Spam)
			word_score = self.naive_bayes(ham_count, spam_count)
			self.score = self.score + word_score
			print word, self.score, word_score		
			self.words.append((word, ham_count, spam_count))

	def simple_bayes(self, ham_count, spam_count):
		ham = ham_count /self.total_ham_count
		spam = spam_count /self.total_spam_count
		score = ham - spam
		return float(score)

	def probability(self, ham_count, spam_count):
		ham_smoothed = ham_count + self.laplace_k
		spam_smoothed = spam_count + self.laplace_k
		ham_probability = ham_smoothed/self.total_ham_count
		spam_probability = spam_smoothed/self.total_spam_count
		how_hammy = ham_probability/spam_probability - 1
		return how_hammy

	def naive_bayes(self, ham_count, spam_count):
		ham_smoothed = ham_count + self.laplace_k * self.ham_chance
		spam_smoothed = spam_count + self.laplace_k * self.spam_chance
		ham = ham_smoothed /self.total_ham_count
		spam = spam_smoothed /self.total_spam_count
		score = ham / ( ham+spam )
		return float(score)-0.5

	def format(self, word):
		lowercase = word.lower()
		return lowercase

	def format_tweet(self, review_text):
		formatted_review_text = re.sub('[^a-zA-Z&\' ]+','', review_text)
		words = formatted_review_text.split()
		formatted_words = []
		for word in words:
			word_key = format(word)
			formatted_words.append(word_key)
		return formatted_words

	def get_word_count(self, word, lexicon):
		lexicon_word = self.session.query(lexicon).filter_by(word=word).first()
		if lexicon_word is None:
			return 0
		else:
			return lexicon_word.count

	def get_score(self, function):
		if function is "simple_bayes":
			score_function = self.simple_bayes
		elif function is "naive_bayes":
			score_function = self.naive_bayes
		else:
			score_function = self.probability
		score = 0
		for word, ham_count, spam_count in self.words:
			word_score = score_function(ham_count, spam_count)
			score = score + word_score
		return score

	def get_words(self):
		return self.words


if __name__ == "__main__":
	userName = 'ai_user'
	passKey = 'letmein'
	hostDomain = 'ec2-54-245-98-196.us-west-2.compute.amazonaws.com'
	# hostDomain = 'localhost'
	portNumber = 3306
	dbName = 'milkntweetz'

	db = create_engine('mysql://' 
		+ userName + ':' 
		+ passKey + '@' 
		+ hostDomain + ':' 
		+ str(portNumber) + '/'
		+ dbName
	)

	db.echo = False  # Try changing this to True and see what happens

	SessionClass = sessionmaker(bind=db)
	session = SessionClass()
	# review = Beta(session, "good bad love hate the")
	good = Beta(session, "These are, overall amazing headphones. They sound great, are comfortable, and easily driven by portable players. However, when I first bought them, and eagerly unwrapped the packaging and tried them out, I was bitterly dissapointed. Where had my money gone, I wondered. They sounded tin canny, and the bass had no punch. I nearly returned them. But, taking the advice of many reviewers, I plugged them into my computer and left the music playing loudly for nearly a week straight. And it paid off. After nearly a month's use, these headphones sound GREAT. I have fallen in love witht eh tight, clear treble and amazingly accurate bass that the HD-280s provide. Jazz and classical fans (and rockers too but to a lesser extent) will love these headphones. I could go on and on and on about the sound quality, but you would find your self reading needless repition of the words \"great,\" \"amazing,\" etcetc. The design is a little big, but very comfy. I can wear these for several hours at a time and my ears will feel fine. The way that they fold up is also very useful for the frequent traveler, and the stretchy wire design is also very handy, keeping the wire out of the way yet providing you nearly 3 meters worth of wire (if stretched to the max). I would also just like to note that, after several airplane trips, the noise reduction in these headphones is also wonderful, and the HD-280 Pros make airplane flights that much more enjoyable. In conclusion, wait at LEAST two weeks, preferably more before judging these headphones, because the more you use them, the better they sound. And after a month's worth of use, they sound great. And they also fit great, and are extremely comfortable. The price too, isn't too bad, and I found them at ... for [$$$], including shipping from the states to taiwan. Do your ears a favor, and buy a pair of HD 280s.")
	


