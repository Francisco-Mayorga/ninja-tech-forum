from google.appengine.ext import ndb

class Topic(ndb.Model):
    title = ndb.StringProperty()
    content = ndb.TextProperty()
    author_email = ndb.StringProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)
    deleted = ndb.BooleanProperty(default=False)


    @classmethod
    def create(cls, title_value, text_value, logged_user, topic):
        new_topic = cls(
            content=text_value,
            title=title_value,
            author_email=logged_user.email(),
            topic_id=topic.key.id(),
            topic_title=topic.title,
            )
        new_topic.put()

        return new_topic