from handlers.base import BaseHandler
from models.topic import Topic
from datetime import datetime, timedelta


class SubscribeTopicsCron(BaseHandler):
    def get(self):
        subscribe_topics = Topic.query(Topic.created or Topic.updated == True)

        overdue_topics = subscribe_topics.filter(
            Topic.created or Topic.updated < (datetime.now() - timedelta(hours=24)))
        topics_to_be_subscribed = overdue_topics.fetch()

        for topic in topics_to_be_subscribed:
            topic.key.subscribe()
