from django.db import models
from post.models import Post
from member.models import Member
class Reply(models.Model):
    reply_id = models.AutoField(primary_key=True)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField(max_length = 100)
    writer = models.ForeignKey(Member, on_delete=models.CASCADE)
    writing_date = models.DateTimeField(auto_now_add=True)
    edting_date = models.DateTimeField(null=True)
    is_deleted = models.BooleanField(default=False)
    is_blinded = models.BooleanField(default=False)
    prob_is_slang = models.FloatField(default=0.0)

    def get_dic_for_user(self):
        return {
                'reply_id' : self.reply_id,
                'text' : self.text,
                'writer' : self.writer.nickname,
                'writing_date' : self.writing_date
        }
    def get_dic_for_admin(self):
        return {
                'post_id' : self.reply_id,
                'reply_id' : self.post_id.post_id,
                'text' : self.text,
                'writer' : self.writer.nickname,
                'writing_date' : self.writing_date,
                'edting_date' : self.edting_date,
                'is_deleted' : self.is_deleted,
                'is_blinded' : self.is_blinded,
                'prob_is_slang' : self.prob_is_slang,
        }
# Create your models here.
