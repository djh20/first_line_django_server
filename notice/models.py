from django.db import models
from member.models import Member
class Notice(models.Model):
    notice_id = models.AutoField(primary_key = True)
    receiver_id = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='receiver_id')
    sender_id = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='sender_id')
    text = models.TextField(max_length=3000)
    send_datetime = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default = False)
# Create your models here.
