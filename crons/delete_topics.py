from handlers.base import BaseHandler
from models.topic import Topic
from datetime import datetime, timedelta


class DeleteTopicsCron(BaseHandler):
    def get(self):
        deleted_topics = Topic.query(Topic.deleted == True)

        overdue_topics = deleted_topics.filter(Topic.updated < (datetime.now() - timedelta(days=30)))
        topics_to_be_remove = overdue_topics.fetch()

        for topic in topics_to_be_remove:
            topic.key.delete()
