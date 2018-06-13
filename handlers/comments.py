from handlers.base import BaseHandler
from google.appengine.api import users
from models.comment import Comment
from models.topic import Topic
from utils.decorators import validate_csrf


class CommentAddHandler(BaseHandler):
    @validate_csrf
    def post(self, topic_id):
        logged_user = users.get_current_user()

        if not logged_user:
            return self.write("Please login before you're allowed to post a topic.")

        text_value = self.request.get("text")

        topic = Topic.get_by_id(int(topic_id))

        Comment.create(
            text_value=text_value,
            logged_user=logged_user,
            topic=topic,
        )
        return self.redirect_to("topic-details", topic_id=topic.key.id())


class ListCommentHandler(BaseHandler):
    def get(self):
        logged_user = users.get_current_user()
        if not logged_user:
            return self.write("Please login before you're allowed to post a topic.")

        comments = Comment.filter_by_user(logged_user.email()).fetch()

        context = {
            "comments": comments,
        }

        return self.render_template("list_comment.html", params=context)


class CommentDeleteHandler(BaseHandler):
    def get(self, comment_id):

        comment = Comment.get_by_id(int(comment_id))

        context = {
            "comment": comment,
        }

        return self.render_template_with_csrf("comment_delete.html", params=context)

    @validate_csrf
    def post(self, comment_id):
        logged_user = users.get_current_user()

        comment = Comment.get_by_id(int(comment_id))
        if comment.author_email == logged_user.email() or users.is_current_user_admin():
            comment.deleted = True
        else:
            return self.response.write('only the topic author or Ninja Tech Forum admin can delete the comment!')

        comment.delete()

        comments = Comment.filter_by_topic(int(comment_id)).fetch()

        for comment in comments:
            comment.delete()

        return self.redirect_to("comment-delete", comment_id=comment.key.id())
