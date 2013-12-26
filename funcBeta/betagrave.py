from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import *
import re
from math import log10, floor

def sigfig(x):
	return round(x, -int(floor(log10(x))))

Base = declarative_base()
class TestReview(Base):
	__tablename__ = 'cv_data'

	id = Column(Integer, primary_key=True)
	asin = Column(String)
	product_type = Column(String)
	product_name = Column(String)
	created_by = Column(String)
	comment = Column(String)
	known_score = Column(Integer)
	viewed = Column(Integer)

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

def format(word):
	lowercase = word.lower()
	return lowercase

def format_tweet(review_text):
	formatted_review_text = re.sub('[^a-zA-Z&\' ]+','', review_text)
	words = formatted_review_text.split()
	formatted_words = []
	for word in words:
		word_key = format(word)
		formatted_words.append(word_key)
	return formatted_words

def beta(word, lexicon, lexicon_count):
	lexicon_word = session.query(lexicon).filter_by(word=word).first()
	if lexicon_word is None:
		word_count = 0
	else:
		word_count = lexicon_word.count
	return word_count/lexicon_count

def beta_tweet(tweet_text):
	ham_count = session.query(func.sum(Ham.count)).scalar()
	spam_count = session.query(func.sum(Spam.count)).scalar()
	tweet = format_tweet(tweet_text)
	tweet_ham = 0
	tweet_spam = 0
	words = []
	for word in tweet:
		ham_score = beta(word, Ham, ham_count)
		spam_score = beta(word, Spam, spam_count)
		tweet_ham = tweet_ham + ham_score
		tweet_spam = tweet_spam + spam_score
		score = ham_score - spam_score
		obj = {
			"word": word,
			"score": score
		}
		words.append(obj)
	return words


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

# metadata = MetaData(db)

SessionClass = sessionmaker(bind=db)
session = SessionClass()

#random review
# random_review = session.query(TestReview).order_by(func.random())
# print random_review.all()

# review = beta_tweet("I think that the new iphone is a fairly reasonably priced product with some very interesting attributes")
review = beta_tweet("love hate good bad okay")


review.sort()

for word in review:
	print word['word'], word['score']

