from django.db import models
from member.models import Member
import datetime

class Keyword(models.Model):
    keyword = models.CharField(max_length = 10, primary_key=True)
    registrator = models.ForeignKey(Member, on_delete=models.CASCADE)
    registration_date = models.DateTimeField(auto_now_add=True)
    recent_used_date = models.DateField(null = True)                       # 최근 사용일
    suggest_date = models.DateField(default=datetime.date.today)           # 사용 예정일
    suggest_amount = models.IntegerField(default=0)                        # 키워드 사용 횟수  - 키워드를 사용해서 작성한 글의 갯수

    def get_keyword(self):
        return self.keyword

    def get_for_admin(self):
        return {
            'keyword' : self.keyword,
            'registrator' : self.registrator.id,
            'registration_date' : self.registration_date.strftime("%y.%m.%d %p %I:%M"),
            'recent_used_date' : self.recent_used_date.strftime("%y.%m.%d"),
            'suggest_date' : self.suggest_date.strftime("%y.%m.%d"),
            'suggest_amount' : self.suggest_amount
        }
# Create your models here.
