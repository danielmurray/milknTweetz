import re
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

	def __init__(self, tweet_text ):
		self.laplace_k = 1
		self.tweet = self.format_tweet(tweet_text)
		self.total_ham_count = session.query(func.sum(Ham.count)).scalar()
		self.total_spam_count = session.query(func.sum(Spam.count)).scalar()
		self.total_count = self.total_ham_count + self.total_spam_count
		self.ham_chance = self.total_ham_count / self.total_count
		# print "ham_chance", self.ham_chance
		self.spam_chance = self.total_spam_count / self.total_count
		# print "spam_chance", self.spam_chance
		self.words = []
		self.score = 0
		for word in self.tweet:
			word_score = self.naive_bayes(word)
			self.words.append((word, word_score))
			self.score = self.score + word_score
			print self.score, '++Positive++' if self.score > 0 else '--Negative--', word

	def naive_bayes(self, word):
		ham_count = self.get_word_count(word, Ham)
		spam_count = self.get_word_count(word, Spam)
		ham_smoothed = ham_count + self.laplace_k * self.ham_chance
		spam_smoothed = spam_count + self.laplace_k * self.spam_chance
		ham = ham_smoothed /self.total_ham_count
		spam = spam_smoothed /self.total_spam_count
		score = ham / ( ham+spam )
		return 2*float(score) - 1

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
		lexicon_word = session.query(lexicon).filter_by(word=word).first()
		if lexicon_word is None:
			return 0
		else:
			return lexicon_word.count

	def get_score(self):
		return self.score

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
	# tweet = Beta("So.... after some very long time of getting used to and playing around. The switch to Windows 8.1 is kind of on track now. Even though not very intuitive, the tablet interface is actually quite nice. I mean, not necessary the most useful, but swiping between apps is pretty cool. I'm still not sure if the tablet/PC interface hybrid is a good idea. It's quite confusing to have a \"dorpbox application\" and a \"dropbox app\" in my opinion. Not feasible at the moment, but making a whole switch to just tablet interface at once might be better (as in no more traditional interface, just the new one). Kind of look forward to the day that happens. Shop needs to load faster, and is still lacking quite some official apps, but its fine. I have to give it to facebook for always doing a \"quick support\" on things now a days though. Lots more bugs and glitches to be fix, but all major functions usable? Not sure about the all-in-one-Windows approach but it could be a good solution, at least I've been searching for such solution for quite some time. So far, I think the only company that has sucessfully provide a all-in-one solution is Apple (though, never tried). Microsoft could be alright as long as they \"DO SUPPORT OFFLINE MODE\". Been trying to integrate google, faceboook, microsoft all together, not quite possible yet.")
	tweet = Beta("This is a great product but I can\'t fit it in my asshole so therefore I think it is a bad product, you should not buy it.")	
	print tweet.get_score()


