from django.db import models

class MemberInfo(models.Model):
    id = models.CharField(max_length = 20, primary_key = True)
    pw = models.CharField(max_length = 16)

    def __str__(self):
        return self.id