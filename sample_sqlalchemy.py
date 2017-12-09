# -----------------------------------------SqlAlchemy----------------------------------------------
# SqlAlchemy is an ORM for talking to any number of databases such as sqlite, mysql and postgresql.
# The Engine is the starting point of any SqlAlchemy application. Its the home base for the actual application and
# its DBAPI, delivered to the SqlAlchemy application through a connection Pool and a Dialect which describes how to
# talk to a specific type of database.
# from sqlalchemy import create_engine
# engine = create_engine('postgresql://scott:tiger@localhost:5432/mydatabase')
# The above engine creates a Dialect object tailored towards PostgreSQL, as well as a Pool object which will establish a DBAPI connection at
# localhost:5432 when a connection request is first received. Note that the Engine and its underlying Pool do not establish the first actual DBAPI connection until the
# Engine.connect() method is called, or an operation which is dependent on this method such as Engine.execute() is invoked. In this way, Engine and Pool can be said to have a lazy
# initialization behavior.

# Database Urls: The create_engine() function creates an engine object based on a URL called database url. the format
#  of the url generally follows the following pattern: dialect+driver://username:password@host:port/database. There
# can be other configurations in this url also. The dialect is the type of database for instance mysql, sqlite,
# postgresql and so on. Driver is the DBAPI driver. If nothing is mentioned it uses the default driver.

import sqlalchemy
from sqlalchemy import create_engine
engine = create_engine('mysql://root:root@localhost/helloworld')

# Here root is the name of the user
# root is the password of the user root
# localhost is the host name
# helloworld is the name of the database
# mysql is the name of the sqlalchemy dialect

# Declare a mapping
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


# Here comes the fun part of ORMs
class User(Base):
    """
    A model class should have a minimum of one data member __tablename__ and one attribute, the column representing
    the primary key
    """
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    # here 20 is the length
    full_name = Column(String(20))

    def __repr__(self):
        """
        this method is totally optional and is used for the purpose of representing the User object
        :return:
        """
        return "<User (name: {}, full_name: {}>".format(self.name, self.full_name)


# When we declared our class, Declarative used a Python metaclass in order to perform additional activities once the class declaration was complete; within this phase, it then
# created a Table object according to our specifications, and associated it with the class by constructing a Mapper object. This object is a behind-the-scenes object we normally
#  don’t need to deal with directly (though it can provide plenty of information about our mapping when we need it).
# The Table object is a member of a larger collection known as MetaData. When using Declarative, this object is available using the .metadata attribute of our declarative base class.
# The MetaData is a registry which includes the ability to emit a limited set of schema generation commands to the database. As our SQLite database does not actually have a users
# table present, we can use MetaData to issue CREATE TABLE statements to the database for all tables that don’t yet exist. Below, we call the MetaData.create_all() method, passing
#  in our Engine as a source of database connectivity. We will see that special commands are first emitted to check for the presence of the users table, and following that the
#  actual CREATE TABLE statement

# For instance Base.metadata.create_all(engine)

print "model defined"
import ipdb
ipdb.set_trace()

# Creating instances of the mapped class
print "creating instances of the mapped class"
ed_user = User(name="Rajdeep", full_name="Rajdeep Mukherjee")

print "ed_user.name: {}".format(ed_user.name)
print "ed_user.full_name: {}".format(ed_user.full_name)

# Accessing the id field of the model actually returns a None value at this point, this is because the id is not
# valid yet because all the data has not actually gone to database, all the data is still actually part of the
# session and will be committed to the database using the commit method of the Session class.

# Creating a session
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)

session = Session()

# Simply creating a User obect does not actually add the user to the database by firing any query. First we add the
# model objects to the session and make any changes that we require. After all changes the commit method of Session
# class actually fires the query. Just like the add method there is also an add_all() method that takes in a list of
# User objects or model objects.

# Also for already added model objects if we change any attribute of the

session.add(ed_user)
session.commit()

# Sessions have a rollback feature, if a session is already in play and we want to roll back all current session changes
# to the last commit we simply use the rollback method

session.rollback()

# Querying data from the database
# There are ample number of ways we can query from the database
for instance in session.query(User).order_by(User.id):
    print "instance now: ({}, {})".format(instance.name, instance.full_name)

# As instance is actually a User type object.

#  Any time multiple class entities or column-based entities are expressed as arguments to the query() function, the return result is expressed as tuples
for name, full_name in session.query(User.name, User.full_name):
    print name, full_name

# Deleting can be simply performed using the delete() method of Session class and the passing the model object as
# parameter

# Closing the session can be simply performed using the close method of the Session class.


