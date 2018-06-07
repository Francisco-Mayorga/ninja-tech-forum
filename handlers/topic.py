import uuid
from handlers.base import BaseHandler
from google.appengine.api import users, memcache
from models.topic import Topic
from models.comment import Comment


class TopicAddHandler(BaseHandler):
    def get(self):
        logged_user = users.get_current_user()
        if not logged_user:
            return self.write("Please login before you're allowed to post a topic.")

        csrf_token = str(uuid.uuid4())
        memcache.add(key=csrf_token, value=logged_user.email(),
                     time=600)  # "time" means how many seconds will item be in memcache
        context = {
            "csrf_token": csrf_token,
        }

        return self.render_template("topic_add.html", params=context)

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

        new_topic = Topic.create(
            title_value=title_value,
            text_value=text_value,
            logged_user=logged_user,
        )

        return self.redirect_to("topic-details", topic_id=new_topic.key.id())


class TopicDetailsHandler(BaseHandler):
    def get(self, topic_id):
        logged_user = users.get_current_user()
        if not logged_user:
            return self.write("Please login before you're allowed to post a topic.")

        topic = Topic.get_by_id(int(topic_id))
        comments = Comment.query(Comment.topic_id == topic.key.id(), Comment.deleted == False).order(
            Comment.created).fetch()

        csrf_token = str(uuid.uuid4())
        memcache.add(key=csrf_token, value=logged_user.email(),
                     time=600)  # "time" means how many seconds will item be in memcache

        details = {"topic": topic, "comments": comments, "csrf_token": csrf_token}

        return self.render_template("topic_details.html", params=details)
