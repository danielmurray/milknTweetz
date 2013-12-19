from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import *
import re


Base = declarative_base()
class Review(Base):
	__tablename__ = 'training_data'

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


def word_into_lexicon(word, ham_or_spam):
	db_word = session.query(ham_or_spam).filter_by(word=word).first()

	if db_word == None:
		#add to dictionary
		print word
		lexicon = ham_or_spam(
			word= word, 
			count=1
		)
		session.add(lexicon)
	else:
		#increment count
		print db_word.word, db_word.count
		db_word.count = db_word.count + 1


def review_into_lexicon(review_text, table):
	formatted_review_text = re.sub('[^a-zA-Z&\' ]+','', review_text)
	words = formatted_review_text.split()
	for word in words:
		word_key = format(word)
		word_into_lexicon(word_key, table)


def stickItInHamSpam(review):
	if review.known_score >= 4:
		#Positive review goes in Ham
		review_into_lexicon(review.comment, Ham)
	elif review.known_score <= 2:
		#Negative review goes in Spam
		review_into_lexicon(review.comment, Spam)


userName = 'ai_user'
passKey = 'letmein'
hostDomain = 'ec2-54-245-98-196.us-west-2.compute.amazonaws.com'
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

test = 0

while test < 2:
	review = session.query(Review).filter_by(viewed=0).first()

	print review.product_name
	
	if review is None:
		break
	else:
		stickItInHamSpam(review)

	review.viewed = 1
	session.commit()

	test= test+1
		