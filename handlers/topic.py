from handlers.base import BaseHandler
from google.appengine.api import memcache, users
from models.topic import Topic
from models.comment import Comment
from models.topic_subscription import TopicSubscription
from utils.decorators import validate_csrf


class TopicAddHandler(BaseHandler):
    def get(self):
        logged_user = users.get_current_user()
        if not logged_user:
            return self.write("Please login before you're allowed to post a topic.")

        return self.render_template_with_csrf("topic_add.html")

    @validate_csrf
    def post(self):
        logged_user = users.get_current_user()
        if not logged_user:
            return self.write("Please login before you're allowed to post a topic.")

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

        details = {"topic": topic, "comments": comments}

        return self.render_template_with_csrf("topic_details.html", params=details)


class TopicDeleteHandler(BaseHandler):
    def get(self, topic_id):

        topic = Topic.get_by_id(int(topic_id))

        context = {
            "topic": topic,
        }

        return self.render_template_with_csrf("topic_delete.html", params=context)


    @validate_csrf
    def post(self, topic_id):
        logged_user = users.get_current_user()

        topic = Topic.get_by_id(int(topic_id))
        if topic.author_email == logged_user.email() or users.is_current_user_admin():
            topic.deleted = True
        else:
            return self.response.write('only the topic author or Ninja Tech Forum admin can delete the topic!')

        topic.delete()

        comments = Comment.filter_by_topic(int(topic_id)).fetch()

        for comment in comments:
            comment.delete()

        return self.redirect_to("main-page")


class TopicSubscribeHandler(BaseHandler):
    def get(self, topic_id):
        topic = Topic.get_by_id(int(topic_id))

        context = {
            "topic": topic,
        }

        return self.render_template_with_csrf("topic_subscribe.html", params=context)

    @validate_csrf
    def post(self, topic_id):
        logged_user = users.get_current_user()

        if not logged_user:
            return self.write("Please login before you're allowed to subscribe to one topic.")

        topic = Topic.get_by_id(int(topic_id))

        is_subscribed = topic.author_email == logged_user.email()

        if not is_subscribed:
            # check if user asked to be subscribed
            is_subscribed = TopicSubscription.is_user_subscribed(logged_user, topic)

        if is_subscribed:
            return self.write("You are already subscribed")

        TopicSubscription.create(logged_user, topic)

        return self.redirect_to("topic-details", topic_id=topic.key.id())