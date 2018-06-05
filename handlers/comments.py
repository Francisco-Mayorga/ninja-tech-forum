from handlers.base import BaseHandler
from google.appengine.api import users, memcache
from models.comment import Comment
from models.topic import Topic


class CommentAddHandler(BaseHandler):
    def post(self, topic_id):
        logged_user = users.get_current_user()

        if not logged_user:
            return self.write("Please login before you're allowed to post a topic.")

        csrf_token = self.request.get("csrf-token")
        mem_token = memcache.get(key=csrf_token)

        if not mem_token or mem_token != logged_user.email():
            return self.write("You are evil attacker...")

        text_value = self.request.get("text")
        topic = Topic.get_by_id(int(topic_id))

        new_comment = Comment(
            content=text_value,
            author_email=logged_user.email(),
            topic_id=topic.key.id(),
            topic_title=topic.title,
        )

        new_comment.put()

        return self.redirect_to("topic-details", topic_id=new_comment.key.id())
