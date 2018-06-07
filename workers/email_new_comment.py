from handlers.base import BaseHandler
from google.appengine.api import mail


class EmailNewCommentWorker(BaseHandler):
    def post(self):
        topic_author_email = self.request.get("topic-author-email")
        topic_title = self.request.get("topic-title")
        topic_id = self.request.get("topic-id")

        mail.send_mail(sender="fffmayorga@gmail.com",  # add here YOUR email address (the owner of Ninja Tech Forum)
                       to=topic_author_email,  # receiver is the person who created the topic
                       subject="New comment on your topic",
                       body="""Your topic {} received a new comment.

                       Click <a href="https://my-project-ninja-tech.appspot.com/topic/{}/details">on this link</a> to see it""".format(topic_title,
                                                                                                             topic_id))