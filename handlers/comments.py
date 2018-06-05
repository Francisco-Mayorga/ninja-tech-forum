import uuid

from handlers.base import BaseHandler
from google.appengine.api import users, memcache
from models.comment import Comment

class CommentAddHandler(BaseHandler):
    def post(self):
        logged_user = users.get_current_user()

        if not logged_user:
            return self.write("Please login before you're allowed to post a topic.")

        csrf_token = self.request.get("csrf-token")
        mem_token = memcache.get(key=csrf_token)

        if not mem_token or mem_token != logged_user.email():
            return self.write("You are evil attacker...")

        title_value = self.request.get("title")
        text_value = self.request.get("text")

        if not title_value:
            return self.write("Title field is required")

        if not text_value:
            return self.write("Text field is required")

        new_comment = Comment(
            title=title_value,
            content=text_value,
            author_email=logged_user.email(),
        )

        new_comment.put()

        return self.redirect_to("topic-details", topic_id=new_comment.key.id())