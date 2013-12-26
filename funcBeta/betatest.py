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

review_count = 100
reviews = session.query(TestReview).limit(review_count).all()

successes = 0
for review in reviews:
	print review.product_name
	sentiment = Beta(review.comment, session)
	given = review.known_score
	calculated = sentiment.getscore()
	print given, calculated
	if given in [4,5] and calculated > 0:
		successes = successes + 1
	elif given in [1,2] and calculated < 0:
		successes = successes + 1

print successes / review_count


