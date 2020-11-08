from django.db import models
from member.models import Member
from post.models import Post
from reply.models import Reply
# Create your models here.
class Report(models.Model):
    report_id = models.AutoField(primary_key=True)
    report_text = models.TextField(max_length = 300)
    process_text = models.TextField(max_length = 300, null=True,blank=True)
    report_date = models.DateTimeField(auto_now_add=True )
    process_date = models.DateTimeField(null=True, blank=True)
    report_writer = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='report_writer')
    process_writer = models.ForeignKey(Member, on_delete=models.CASCADE, null=True, related_name='process_writer', blank=True)
    is_processed = models.BooleanField(default=False)
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE, null=True, related_name='reply', blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, related_name='post', blank=True)

    def get_for_admin(self):
        return {
            'report_id' : self.report_id,
            'report_text' : self.report_text,
            'process_text' : self.process_text,
            'report_date' : self.report_date.strftime("%y.%m.%d %p %I:%M"),
            'process_date' : self.process_date.strftime("%y.%m.%d %p %I:%M") if self.process_date != None else "",
            'report_writer' : self.report_writer.id if self.report_writer != None else "",
            'process_writer' : self.process_writer.id if self.process_writer != None else "",
            'is_processed' : str(self.is_processed),
            'reply' : self.reply.reply_id if self.reply != None else "",
            'post' : self.post.post_id if self.post != None else ""
        }