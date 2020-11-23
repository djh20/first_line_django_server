from django.db import models
from post.models import Post
from member.models import Member


class Reply(models.Model):
    reply_id = models.AutoField(primary_key=True)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField(max_length=100)
    writer = models.ForeignKey(Member, on_delete=models.CASCADE)
    writing_date = models.DateTimeField(auto_now_add=True)
    editing_date = models.DateTimeField(null=True)
    is_deleted = models.BooleanField(default=False)
    is_blinded = models.BooleanField(default=False)
    prob_is_slang = models.FloatField(default=0.0)

    def get_dic(self, isAdmin):
        if isAdmin:
            return self.get_dic_for_admin()
        else:
            return self.get_dic_for_user()

    def get_dic_for_user(self):
        if self.is_blinded == True:
            return {
            'reply_id': self.reply_id,
            'post_id': self.post_id.post_id,
            'text': '블라인드 처리된 댓글입니다.',
            'writer': self.writer.nickname,
            'writing_date': (self.writing_date if self.editing_date == None else self.editing_date)
            }
        else:
            return {
                'reply_id': self.reply_id,
                'post_id': self.post_id.post_id,
                'text': self.text,
                'writer': self.writer.nickname,
                'writing_date': (self.writing_date if self.editing_date == None else self.editing_date)
            }

    def get_dic_for_admin(self):
        return {
            'reply_id': self.reply_id,
            'post_id': self.post_id.post_id,
            'text': self.text,
            'writer': self.writer.nickname,
            'writing_date': self.writing_date,
            'editing_date': (self.editing_date if self.editing_date != None else ""),
            'is_deleted': "Y" if self.is_deleted else "N",
            'is_blinded': "Y" if self.is_blinded else "N",
            'prob_is_slang': self.prob_is_slang,
        }