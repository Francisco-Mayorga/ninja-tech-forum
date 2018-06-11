#!/usr/bin/env python
import webapp2

from crons.delete_topics import DeleteTopicsCron
from handlers.home import MainHandler
from handlers.cookie import CookieAlertHandler
from handlers.topic import TopicAddHandler, TopicDeleteHandler
from handlers.topic import TopicDetailsHandler
from handlers.comments import CommentAddHandler, ListCommentHandler
from workers.email_new_comment import EmailNewCommentWorker

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler, name="main-page"),
    webapp2.Route('/set-cookie', CookieAlertHandler, name="set-cookie"),
    webapp2.Route('/topic/add', TopicAddHandler, name="topic-add"),
    webapp2.Route('/topic/<topic_id:\d+>/details', TopicDetailsHandler, name="topic-details"),
    webapp2.Route('/topic/<topic_id:\d+>/comment', CommentAddHandler, name="comment-add"),
    webapp2.Route('/list_comment', ListCommentHandler, name="my-comments"),
    webapp2.Route('/task/email-new-comment', EmailNewCommentWorker, name="task-email-new-comment"),
    webapp2.Route('/topic/<topic_id:\d+>/delete', TopicDeleteHandler, name="topic-delete"),
    webapp2.Route("/cron/delete-topics", DeleteTopicsCron, name="cron-delete-topics"),

], debug=True)
