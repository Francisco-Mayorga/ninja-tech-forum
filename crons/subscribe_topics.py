from handlers.base import BaseHandler
from models.topic import Topic
from datetime import datetime, timedelta
from google.appengine.ext import ndb


class SubscribeTopicsCron(BaseHandler):
    def get(self):
        subscribe_topics = Topic.query(Topic.deleted == False)
        overdue_topics = subscribe_topics.filter(
            ndb.OR(
                ((Topic.created < (datetime.now() - timedelta(hours=24))),
                 (Topic.updated < (datetime.now() - timedelta(hours=24)))
                  )))
        topics_to_be_subscribed = overdue_topics.fetch()

        for TopicSubscription in topics_to_be_subscribed:
            TopicSubscription.key.create()




