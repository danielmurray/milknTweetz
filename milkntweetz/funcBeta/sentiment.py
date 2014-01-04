from sqlalchemy import *

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

metadata = MetaData(db)

# The users table already exists, so no need to redefine it. Just
# load it from the database using the "autoload" feature.
users = Table('temp', metadata, autoload=True)


def run(stmt):
    rs = stmt.execute()
    for row in rs:
        print row

s = users.select()
run(s)