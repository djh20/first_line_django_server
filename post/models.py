from django.db import models
from member.models import Member
from keyword_.models import Keyword
from datetime import datetime
class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length = 20)
    text = models.TextField(max_length = 3000)
    like = models.IntegerField(default=0)
    tag = models.CharField(max_length = 100)
    num_reply = models.IntegerField(default = 0)
    writer = models.ForeignKey(Member, on_delete=models.CASCADE)
    writing_date = models.DateTimeField(auto_now_add=True)
    editing_date = models.DateTimeField(null=True)
    is_deleted = models.BooleanField(default=False)
    is_blinded = models.BooleanField(default=False)
    prob_p_dp = models.FloatField(default=0.0)
    prob_a_da = models.FloatField(default=0.0)
    temperature = models.FloatField(default=0.0)
    prob_is_slang = models.FloatField(default=0.0)
    keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE, null=True, blank=True)

    def get_dic_for_user(self):
        # gap  = dattime.now() - self.writing_date
        return {
            'post_id' : self.post_id,
            'title' : self.title,
            'text' : self.text,
            'like' : self.like,
            'num_reply' : self.num_reply,
            'tag' : self.tag,
            'writer' : self.writer.nickname,
            'writing_date' : self.writing_date.strftime("%y.%m.%d %p %H:%M"),
            'temperature' : self.temperature,
            'keyword' : (self.keyword.get_keyword() if self.keyword != None else "")
        }




    def __str__(self):
        """A string representation of the model."""
        return self.title

class LikeRecord(models.Model):
    like_record_id = models.AutoField(primary_key = True)
    member_id = models.ForeignKey(Member, on_delete=models.CASCADE)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    temperature = models.FloatField()
    is_like = models.BooleanField()

class LookupRecord(models.Model):
    lookup_record_id = models.AutoField(primary_key = True)
    member_id = models.ForeignKey(Member, on_delete=models.CASCADE)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    temperature = models.FloatField()
    is_like = models.BooleanField()