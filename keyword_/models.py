from django.db import models

class Keyword(models.Model):
    keyword = models.CharField(max_length = 10, primary_key=True)
    registration_date = models.DateTimeField(auto_now_add=True)
    recent_used_date = models.DateTimeField(null=True)
    suggest_amount = models.IntegerField(default=1)

    def get_keyword(self):
        return self.keyword

# Create your models here.
