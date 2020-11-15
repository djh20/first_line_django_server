from django.db import models
from member.models import Member
from keyword_.models import Keyword
from datetime import datetime
from django.conf import settings
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
    num_lookup = models.IntegerField(default = 0)
    num_good = models.IntegerField(default = 0)

    def get_dic(self,isAdmin):
        if isAdmin:
            return self.get_dic_for_admin()
        else:
            return self.get_dic_for_user()


    def get_dic_for_user(self):
        tag = []
        tmp = self.tag.split(settings.TAG_SEPERATOR)
        for x in tmp:
            if x!="":
                tag.append(x)
        return {
            'post_id' : self.post_id,
            'title' : self.title,
            'text' : self.text,
            'like' : self.like,
            'num_reply' : self.num_reply,
            'tag' : tag,
            'writer' : self.writer.nickname,
            'writing_date' : self.writing_date.strftime("%y.%m.%d %p %I:%M"),
            'temperature' : format(self.temperature,".2f"),
            'keyword' : (self.keyword.get_keyword() if self.keyword != None else ""),
            'num_lookup':self.num_lookup,
            'num_good':self.num_good,
        }
  
        
    def get_dic_for_admin(self):
        
        return {
            'post_id' : self.post_id,
            'title' : self.title,
            'text' : self.text,
            'like' : self.like,
            'num_reply' : self.num_reply,
            'tag' : self.tag,
            'writer' : self.writer.nickname,
            'writing_date' : self.writing_date.strftime("%y.%m.%d %p %I:%M"),
            'editing_date' : (self.editing_date if self.editing_date != None else ""),
            'temperature' : self.temperature,
            'keyword' : (self.keyword.get_keyword() if self.keyword != None else ""),
            'is_deleted' : str(self.is_deleted),
            'is_blinded' : str(self.is_blinded),
            'prob_p_dp' : self.prob_p_dp,
            'prob_a_da' : self.prob_a_da,
            'prob_is_slang' : self.prob_is_slang,
            'num_lookup':self.num_lookup,
            'num_good':self.num_good,
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

    def get_dic(self):
        return {
            'like_record_id': self.like_record_id,
            'member' : self.member_id,
            'post' : self.post_id,
            'date' : self.date,
            'temperature' : self.temperature,
        }

class LookupRecord(models.Model):
    lookup_record_id = models.AutoField(primary_key = True)
    member_id = models.ForeignKey(Member, on_delete=models.CASCADE)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    temperature = models.FloatField()
    is_like = models.BooleanField()

    def get_dic(self):
        return {
            'lookup_record_id' : self.lookup_record_id,
            'member' : self.member_id,
            'post': self.post_id,
            'date':self.date,
            'temperature':self.temperature,
            'is_like':self.is_like
        }