from django.db import models
from django.conf import settings

class Member(models.Model):
    id = models.CharField(max_length = 20, primary_key = True)
    pw = models.CharField(max_length = 512)
    name = models.CharField(max_length = 11)
    nickname = models.CharField(max_length = 10)
    age = models.IntegerField()
    gender = models.BooleanField() 
    authority = models.IntegerField() 
    phonenumber = models.CharField(max_length=15)
    email = models.CharField(max_length=45)

    def get_id(self):
        return self.id

    def get_dic(self):
        return {
            'id':self.id,
            'name' : self.name,
            'nickname' : self.nickname,
            'age' : self.age,
            'gender' : '남성' if self.gender == True else '여성',
            'phonenumber' : self.phonenumber,
            'email' : self.email,
            'authority' : ('회원' if self.authority == settings.AUTHORITY['회원'] else '관리자')
        }

class SementicRecord(models.Model):
    sementic_record_id = models.AutoField(primary_key = True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    date = models.DateField()
    initial_value = models.FloatField(default = 36.5)
    current_temperature = models.FloatField(default = 36.5)
    reflected_number = models.PositiveIntegerField(default = 1)

    def get_dic(self):
        return {
            'year' : self.date.year, 
            'month' : self.date.month, 
            'date' : self.date.day, 
            'temperature' : format(self.current_temperature,".1f")
        }