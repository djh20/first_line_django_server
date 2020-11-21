from django.db import models
from member.models import Member
class Notice(models.Model):
    notice_id = models.AutoField(primary_key = True)
    receiver_id = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='receiver_id')
    sender_id = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='sender_id')
    text = models.TextField(max_length=3000)
    source_url = models.TextField(max_length=100, null=True, blank=True)
    send_datetime = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default = False)
    
    def get_for_admin(self):
        return {
            'notice_id' : self.notice_id,
            'receiver_id' : self.receiver_id.id,
            'sender_id' : self.sender_id.id,
            'send_datetime' : self.send_datetime.strftime("%y.%m.%d %p %I:%M"),
            'text' : self.text,
            'is_read' : str(self.is_read),
            'source_url' : self.source_url
<<<<<<< HEAD
=======
        }

    def get_for_user(self):
        return {
            'notice_id' : self.notice_id,
            'send_datetime' : self.send_datetime.strftime("%y.%m.%d %p %I:%M"),
            'text' : self.text,
            'source_url' : self.source_url
>>>>>>> bfc330b7fbd7ce3a0f760162c62ea6c186e673b6
        }

    def get_for_user(self):
        return {
            'notice_id' : self.notice_id,
            'send_datetime' : self.send_datetime.strftime("%y.%m.%d %p %I:%M"),
            'text' : self.text,
            'source_url' : self.source_url
        }

