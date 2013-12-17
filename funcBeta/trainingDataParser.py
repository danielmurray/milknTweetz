import xml.sax
import xml.sax.handler
from xml.sax.saxutils import escape
from unidecode import unidecode
import re
from sqlalchemy import *
import sys
import glob


class PseudoReviews(object):

    def __init__(self, sourceFileName):
        self.ri = self.read_iterator()
        self.fileName = sourceFileName
        self.file = open(self.fileName)


    def read_iterator(self):
        yield '<xml>'
        for line in self.file:
            #Dealing with all the bull shit that is text formats
            noForeignCharacters = unidecode(line)
            noAmpersands = re.sub('&', '&amp;', noForeignCharacters)
            cleanText = re.sub("", "", noAmpersands)
            yield cleanText
        yield '</xml>'

    def read(self, *foo):
        try:
            return self.ri.next()
        except StopIteration:
            return ''

class ReviewDict():

    def __init__(self):
        self.review = {}

    def add(self, name, content):
        self.review[name] = content
        
    def printReview(self):
        for key in  self.review.keys():
            print key, '-', self.review[key]
            
class Reviews():

    def __init__(self):
        self.reviews = []

    def add(self, review):
        self.reviews.append(review)
        
    def printReviews(self):
        for review in  self.reviews:
            print review.printReview()

    def howMany(self):
        return len(self.reviews)

    def getReviews(self):
        return self.reviews

class SAXHandler(xml.sax.handler.ContentHandler):

    def __init__(self, reviews):
        xml.sax.ContentHandler.__init__(self)
        self.xmlStack = []
        self.currReview = ReviewDict()
        self.reviews = reviews

    def startElement(self, name, attrs):
        self.xmlStack.append(name)

    def endElement(self, name):
        if name == 'review':
            self.reviews.add(self.currReview)
            self.currReview = ReviewDict()
        self.xmlStack.pop()

    def characters(self, content):
        topOfStack = self.xmlStack.pop()
        if len(content) > 2:
            self.currReview.add(topOfStack,content)
        topOfStack = self.xmlStack.append(topOfStack)

class reviewDB():

    def __init__(self ):
        userName = 'ai_user'
        passKey = 'letmein'
        # hostDomain = 'ec2-54-245-98-196.us-west-2.compute.amazonaws.com'
        hostDomain = 'localhost'
        portNumber = 3306
        dbName = 'milkntweetz'

        self.db = create_engine('mysql://' 
            + userName + ':' 
            + passKey + '@' 
            + hostDomain + ':' 
            + str(portNumber) + '/'
            + dbName
        )

        self.db.echo = False  # Try changing this to True and see what happens

        self.metadata = MetaData(self.db)

    def log(self, reviews):
        for i, review in enumerate(reviews):
            if i%10 == 0:
                self.insert('test_training_data', review)
            elif i%10 == 1:
                self.insert('cv_data', review)
            else:
                self.insert('training_data', review)

    def insert(self, tableName, reviewObj):
        table = Table(tableName, self.metadata, autoload=True)
        review = reviewObj.review 
        stmt = table.insert().values({
            "comment" : review.get('review_text'),
            "known_score" : int(float(review.get('rating'))),
            "created_by" : review.get('reviewer'),
            "asin" : review.get('asin'),
            "product_type" : review.get('product_type'),
            "product_name" : review.get('product_name')
        })
        try:
            stmt.execute()
        except:
            print sys.exc_info()[0]

def main(sourceFileName):
    fileNames = glob.glob(sourceFileName+'video/all.review')
    for fileName in fileNames:
        reviews = Reviews()
        xml.sax.parse(PseudoReviews(fileName), SAXHandler(reviews))
        rL = reviewDB()
        rL.log(reviews.getReviews())

if __name__ == "__main__":
  main("../reviewTrainingData/review_data/")
 
