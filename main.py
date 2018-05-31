#!/usr/bin/env python
import webapp2
from handlers.home import MainHandler
from handlers.cookie import CookieAlertHandler
from handlers.topic import TopicAddHandler
from handlers.topic_details import TopicDetailsHandler


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler, name="main-page"),
    webapp2.Route('/set-cookie', CookieAlertHandler, name="set-cookie"),
    webapp2.Route('/topic/add', TopicAddHandler, name="topic-add"),
    webapp2.Route('/topic/<topic_id:\d+>/details', TopicDetailsHandler, name="topic-details"),

], debug=True)
