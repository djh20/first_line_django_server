from django.db import models

class Member(models.Model):
    id = models.CharField(max_length = 20, primary_key = True)
    pw = models.CharField(max_length = 64)
    name = models.CharField(max_length = 11)
    nickname = models.CharField(max_length = 10)
    age = models.IntegerField()
    gender = models.BooleanField() 
    authority = models.IntegerField() 
    phonenumber = models.CharField(max_length=15)
    email = models.CharField(max_length=45)

    def get_id(self):
        return self.id

class SementicRecord(models.Model):
    sementic_record_id = models.AutoField(primary_key = True)
    member_id = models.ForeignKey(Member, on_delete=models.CASCADE)
    date = models.DateField()