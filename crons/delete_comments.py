from handlers.base import BaseHandler
from models.comment import Comment
from datetime import datetime, timedelta


class DeleteCommentsCron(BaseHandler):
    def get(self):
        deleted_comments = Comment.query(Comment.deleted == True)

        overdue_topics = deleted_comments.filter(Comment.updated < (datetime.now() - timedelta(days=30)))
        comments_to_be_remove = overdue_topics.fetch()

        for comment in comments_to_be_remove:
            comment.key.delete()