from bs4 import BeautifulSoup
from sqlalchemy import *
import sys
import glob
import re

class TrainingDatabase():

    def __init__(self ):
        user_name = 'ai_user'
        pass_key = 'letmein'
        host_domain = 'ec2-54-245-98-196.us-west-2.compute.amazonaws.com'
        # host_domain = 'localhost'
        port_number = 3306
        db_name = 'milkntweetz'

        self.db = create_engine('mysql://' 
            + user_name + ':' 
            + pass_key + '@' 
            + host_domain + ':' 
            + str(port_number) + '/'
            + db_name
        )

        self.db.echo = False  # Try changing this to True and see what happens

        self.metadata = MetaData(self.db)

    def log(self, soup):
        reviews = soup.find_all('review')
        for i, review in enumerate(reviews):
            if i%10 == 0:
                self.insert('test_training_data', review)
            elif i%10 == 1:
                self.insert('cv_data', review)
            else:
                self.insert('training_data', review)


    def insert(self, table_name, review_soup):
        
        comment = self.fetch_n_format(review_soup, 'review_text')
        rating = self.fetch_n_format(review_soup, 'rating')
        reviewer = self.fetch_n_format(review_soup, 'reviewer')
        asin = self.fetch_n_format(review_soup, 'asin')
        product_type = self.fetch_n_format(review_soup, 'product_type')
        product_name = self.fetch_n_format(review_soup, 'product_name')

        table = Table(table_name, self.metadata, autoload=True)

        stmt = table.insert().values({
            "comment" : comment,
            "known_score" : int(float(rating)),
            "created_by" : reviewer,
            "asin" : asin,
            "product_type" : product_type,
            "product_name" : product_name
        })
        try:
            stmt.execute()
        except:
            print sys.exc_info()[0]

    def fetch_n_format(self, soup, tag):
        fetch_text = soup.find(tag)
        format_text = unicode(re.sub('\n','',fetch_text.contents[0]))
        return format_text

if __name__ == "__main__":
    db = TrainingDatabase()
    fileNames = glob.glob("../reviewTrainingData/review_data/*/all.review")
    for fileName in fileNames:
        with open(fileName) as f:
            soup = BeautifulSoup(f)
            print fileName, len(soup)
            db.log(soup)
            soup.decompose
 
