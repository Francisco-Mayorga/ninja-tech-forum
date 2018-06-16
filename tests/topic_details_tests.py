import os
import unittest
import webapp2 as webapp2
import webtest
from google.appengine.ext import testbed

from handlers.topic import TopicDetailsHandler
from models.comment import Comment
from models.topic import Topic


class TopicDetailsTests(unittest.TestCase):
    def setUp(self):
        app = webapp2.WSGIApplication(
            [
                webapp2.Route('/topic/<topic_id:\d+>/details', TopicDetailsHandler, name="topic-details"),
            ]
        )

        self.testapp = webtest.TestApp(app)
        self.testbed = testbed.Testbed()
        self.testbed.activate()

        """ Uncomment the stubs that you need to run tests. """
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        # self.testbed.init_mail_stub()
        # self.testbed.init_taskqueue_stub()
        self.testbed.init_user_stub()
        # ...

        """ Uncomment if you need user (Google Login) and if this user needs to be admin. """
        os.environ['USER_EMAIL'] = 'some.user@example.com'
        # os.environ['USER_IS_ADMIN'] = '1'

    def tearDown(self):
        self.testbed.deactivate()

    def test_get_topic_details_handler(self):
        # GET

        topic = Topic.get_by_id(int(topic_id))
        comments = Comment.query(Comment.topic_id == topic.key.id(), Comment.deleted == False).order(
            Comment.created).fetch()

        details = {"topic": topic, "comments": comments}

        response = self.testapp.get('/topic/5664248772427776/details', params=details)
        self.assertEqual(response.status_in, 200)




