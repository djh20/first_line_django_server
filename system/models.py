from django.db import models
from member.models import Member
class Log(models.Model):
    log_id = models.AutoField(primary_key=True)
    response_time = models.DateTimeField(auto_now_add = True)
    request_url = models.CharField(max_length=20)
    request_method = models.CharField(max_length=10)
    response_code = models.IntegerField()
    keyword = models.ForeignKey(Member, on_delete=models.CASCADE, null=True)
