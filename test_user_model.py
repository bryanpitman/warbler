"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, Follow

from sqlalchemy.exc import NotNullViolation, IntegrityError

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler_test"

# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    def setUp(self):
        User.query.delete()

        u1 = User.signup("u1", "u1@email.com", "password", None)
        u2 = User.signup("u2", "u2@email.com", "password", None)


        db.session.commit()
        self.u1_id = u1.id
        self.u2_id = u2.id

        self.client = app.test_client()

    def tearDown(self):
        db.session.rollback()

    def test_user_model(self):
        u1 = User.query.get(self.u1_id)

        # User should have no messages & no followers
        self.assertEqual(len(u1.messages), 0)
        self.assertEqual(len(u1.followers), 0)


    def test_repr(self):
        """test if a user and username are returned """
        #need a user
        u1 = User.query.get(self.u1_id)

        """In [3]: user = User.query.get(1)
        Out[4]: <User #1: tuckerdiane, ronald38@yahoo.com>"""

        # when we call the user get back f"<User #{self.id}: {self.username}, {self.email}>"
        self.assertEqual(f"{u1}", f"<User #{self.u1_id}: u1, u1@email.com>")



# Does is_following successfully detect when user1 is following user2?
# get 2 users provided in the setup based on the id
# append to the following user1 .append.
#what does the list have? following and follows will be a list.
# 2 assert statments user one follows user two, user two does not follow user 1

    def test_is_following(self):

        u1 = User.query.get(self.u1_id)
        u2 = User.query.get(self.u2_id)
        u1.following.append(u2)

        self.assertTrue(u1.is_following(u2))
        self.assertFalse(u2.is_following(u1))

    def test_is_followed_by(self):

        u1 = User.query.get(self.u1_id)
        u2 = User.query.get(self.u2_id)
        u1.following.append(u2)

        self.assertTrue(u2.is_followed_by(u1) )
        self.assertFalse(u1.is_followed_by(u2))

    # Does User.signup successfully create a new user given valid credentials?
    def test_user_signup(self):



    #     # TODO: friday research assert raises(NotNullViolation)
    # def test_user_signup_not_valid(self):

    #     u3 = User.signup("u3", None, "password", None)
    #     db.session.commit()
    #     # operater with how to handle an error

