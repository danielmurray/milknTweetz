from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import *
import re
from math import log10, floor
from beta import Beta

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

print session
review_count = 100
reviews = session.query(TestReview).order_by(func.rand()).limit(review_count).all()
print len(reviews)

successes = {}
successes['simple'] = 0
successes['probability'] = 0
successes['naive_bayes'] = 0

for i,review in enumerate(reviews):
	sentiment = Beta(session, review.comment)
	given = review.known_score

	print review.product_name, given

	for test in ['simple', 'probability', 'naive_bayes']:
		calculated_score = sentiment.get_score(test)
		if given in [4,5] and calculated_score > 0:
			successes[test] = successes + 1
		elif given in [1,2] and calculated_score < 0:
			successes[test] = successes + 1
		print test, calculated_score, successes[test]/i



print successes / review_count


