#!/usr/bin/env python
from google.appengine.api import users
from handlers.base import BaseHandler
from models.comment import Comment
from models.topic import Topic


class ListCommentHandler(BaseHandler):
    def get(self):
        logged_user = users.get_current_user()
        if not logged_user:
            return self.write("Please login before you're allowed to post a topic.")

        return self.render_template_with_csrf("list_comment.html")
