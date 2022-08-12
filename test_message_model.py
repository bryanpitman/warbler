import os
from unittest import TestCase

from models import db, User, Message, Follow, Like

import pdb

#from sqlalchemy.exc import NotNullViolation, IntegrityError

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


class MessageModelTestCase(TestCase):
    def setUp(self):
        Message.query.delete()
        User.query.delete()

        u1 = User.signup("u1", "u1@email.com", "password", None)
        u2 = User.signup("u2", "u2@email.com", "password", None)

        db.session.commit()
        self.u1_id = u1.id
        self.u2_id = u2.id

        m1 = Message(text = "message 1",
                            timestamp = None,
                            user_id = u1.id)
        m2 = Message(text = "message 2",
                            timestamp = None,
                            user_id = u2.id)

        db.session.add(m1)
        db.session.add(m2)
        db.session.commit()
        self.m1_id = m1.id
        self.m2_id = m2.id

        self.client = app.test_client()

    def tearDown(self):
        db.session.rollback()


    # liked_by work
    # liked_message work
    # do we get timestamp (like checking pw what exists in all timestamps)
    # do messages with no text fail
    # do users messages show

    def test_message_exists(self):
        """Tests message has correct data"""

        m1 = Message.query.get(self.m1_id)
        self.assertEqual(m1.text, "message 1")
        self.assertIsNotNone(m1.timestamp)
        self.assertEqual(m1.user_id, self.u1_id)

    def test_liked_relationship(self):
        """Test if liked by relationship works"""

        m1 = Message.query.get(self.m1_id)
        u1 = User.query.get(self.u1_id)
        u2 = User.query.get(self.u2_id)
        m1.users_liked.append(u1)

        liked_msg = Like.query.get((self.m1_id, self.u1_id))

        self.assertIsInstance(liked_msg, Like)
        self.assertEqual(len(u1.liked_messages), 1)


    def test_user_messages(self):
        """Test if user messages show on call"""

        m1 = Message.query.get(self.m1_id)
        u1 = User.query.get(self.u1_id)
        self.assertEqual(len(u1.messages), 1)
        self.assertEqual(m1.user, u1)

    def test_is_owner(self):
        """Test is_owner function works correctly"""

        m1 = Message.query.get(self.m1_id)
        u1 = User.query.get(self.u1_id)
        u2 = User.query.get(self.u2_id)

        self.assertTrue(m1.is_owner(u1))
        self.assertFalse(m1.is_owner(u2))