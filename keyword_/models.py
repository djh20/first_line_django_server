from django.db import models
from member.models import Member

class Keyword(models.Model):
    keyword = models.CharField(max_length = 10, primary_key=True)
    registrator = models.ForeignKey(Member, on_delete=models.CASCADE)
    registration_date = models.DateTimeField(auto_now_add=True)
    recent_used_date = models.DateField(auto_now_add=True)
    suggest_amount = models.IntegerField(default=1)

    def get_keyword(self):
        return self.keyword

    def get_for_admin(self):
        return {
            'keyword' : self.keyword,
            'registrator' : self.registrator.id,
            'registration_date' : self.registration_date.strftime("%y.%m.%d %p %I:%M"),
            'recent_used_date' : self.recent_used_date.strftime("%y.%m.%d"),
            'suggest_amount' : self.suggest_amount
        }
# Create your models here.
